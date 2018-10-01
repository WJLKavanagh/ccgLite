import sys, os, filecmp
import prefix, suffix, free_strat, seed_strat, educate

"""
USAGE GUIDE:
    prefix.run(deck1, deck2, model, multiple_initial_states)    [int, int, str, int(bool)]
    free_strat.run(deck1, deck2, team)                          [int, int, int]
    seed_strat.run(deck1, deck2, team)                          [int, int, int]
    educate.run(deck1, deck2, file, team)                       [int, int, str, int]
    suffix.run(deck1, deck2, multiple_initial_states)           [int, int, int(bool)]
"""

# Reads log.txt and returns last found p(win)
def find_prev_result():
    info = open("log.txt", "r").readlines()
    l = len(info)
    res = ""
    prop = ""
    # find prop & result
    for i in range(1,l):
        if info[l-i][:8] == "Result: " and res == "":
            res = info[l-i][8:20]
        if "Model checking: " in info[l-i] and prop == "":
            prop = info[l-i].split("Model checking: ")[1][:-1]
            break;
    if " " in res:
        return float(res.split(" ")[0])
    return float(res)

# Takes 4 characters and returns opt(win) for either team as two floats
def optimality(deck1, deck2):
    # Generate a prism file to represent SMG of game between both teams
    sys.stdout=open("smg.prism","w")
    prefix.run(deck1, deck2, "smg", 0)
    free_strat.run(deck1, deck2, 1)
    free_strat.run(deck1, deck2, 2)
    suffix.run(deck1, deck2, 0)
    sys.stdout=sys.__stdout__
    # run prism-games with lots of memory, hardcoded prism-games location on SAND
    os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -nopre -cuddmaxmem 300g -javamaxmem 300g smg.prism smg_props.props -prop 1 -s > log.txt")
    p1_opt = find_prev_result()
    if deck1 != deck2:                  # Don't calculate the same optimality twice, there's no need.
        os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -nopre -cuddmaxmem 300g -javamaxmem 300g smg.prism smg_props.props -prop 2 -s > log.txt")
        p2_opt = find_prev_result()
        return p1_opt, p2_opt
    return p1_opt

# Generates grid of opt(win) for all permutations of G
def generate_opt_grid():
    # First pair (CAPS) is team for whom probOpt is calculated
    global d1vd1, d1vd2, d1vd3, d2vd1m, d2vd2, d2vd3, d3vd1, d3vd2, d3vd3
    print "Calculating optimalities, this may take some time...",
    d1vd2, d2vd1 = optimality(1,2)
    d1vd3, d3vd1 = optimality(1,3)
    d2vd3, d3vd2 = optimality(2,3)
    d1vd1 = optimality(1,1)
    d2vd2 = optimality(2,2)
    d3vd3 = optimality(3,3)
    # Display results
    print "win\\vs\t|1\t\t|2\t\t|3"
    print "1\t|"+str(d1vd1)+"\t|"+str(d1vd2)+"\t|"+str(d1vd3)
    print "2\t|"+str(d2vd1)+"\t|"+str(d2vd2)+"\t|"+str(d2vd3)
    print "3\t|"+str(d3vd1)+"\t|"+str(d3vd2)+"\t|"+str(d3vd3)

def adversary_is_unique(it):
    f1 = "adv_strat_" + str(it+1) + ".txt"
    if it > 3:
        for comp in range(it-2, -1, -1):
            f2 = "adv_strat_" + str(comp) + ".txt"
            if filecmp.cmp(f1, f2, shallow=False):
                print "adversary " + str(it-1) + " is equivalent to " + str(comp)
                return False
        print "adversary is unique, continuing.."
    else:
        print "too early for duplicates, continuing.."
    return True

# Takes last adversarial opponents and finds new best opponents and greatest probAdv
def flip_and_run(it, opponent):
    print "Iteration:", str(it) + ", opponent is using deck " + str(opponent) + ", -- calculating adversaries.."
    best_deck = None
    best_score = 0.0
    # build model for each opponent
    for i in range(1,4):
        sys.stdout=open("it"+str(it)+"vs"+str(i)+".prism","w")
        if it % 2 == 1:                                 # Find a strategy for the first team
            prefix.run(i, opponent, "mdp", False)           # False as |I| = 1
            free_strat.run(i, opponent, 1)
            sys.stdout=sys.__stdout__
            os.system("cat adv_strat_"+str(it-1)+".txt >> it"+str(it)+"vs"+str(i)+".prism")
            sys.stdout=open("it"+str(it)+"vs"+str(i)+".prism","a")
            suffix.run(i, opponent, False)                      # False as |I| = 1
        else:                                           # Find a strategy for the second team
            prefix.run(opponent, i, "mdp", False)
            sys.stdout=sys.__stdout__
            os.system("cat adv_strat_"+str(it-1)+".txt >> it"+str(it)+"vs"+str(i)+".prism")
            sys.stdout=open("it"+str(it)+"vs"+str(i)+".prism","a")
            free_strat.run(opponent, i, 2)
            suffix.run(opponent, i, False)                      # False as |I| = 1
        # Model built, now find the greatest adversarial value
        sys.stdout=sys.__stdout__
        os.system("prism -javamaxmem 100g -s it"+str(it)+"vs"+str(i)+".prism props.props -prop "+str(2-it%2)+" > log.txt")
        pair_result = find_prev_result()
        if it % 2 == 1:
            print "ProbAdv_"+str(2-(it%2))+"(" + str(i) + ",", str(opponent) + ") = " + str(pair_result)
        else:
            print "ProbAdv_"+str(2-(it%2))+"(" + str(opponent) + ",", str(i) + ") = " + str(pair_result)
        if pair_result > best_score:
            best_score = pair_result
            best_deck = i
    print "deck " + str(best_deck), "found as adversarial team, calculating adversarial strategy...",
    # Write old_adv VS best_opp to file with multiple i in I for adversary calculation
    sys.stdout = open("it"+str(it)+"_adv.prism", "w")
    if it % 2 == 1:
        prefix.run(best_deck, opponent, "mdp", True)                # True as |I| > 1
        free_strat.run(best_deck, opponent, 1)
        sys.stdout=sys.__stdout__
        os.system("cat adv_strat_"+str(it-1)+".txt >> it"+str(it)+"_adv.prism")
        sys.stdout=open("it"+str(it)+"_adv.prism","a")
        suffix.run(best_deck, opponent, True)                       # True as |I| > 1
    else:
        prefix.run(opponent, best_deck, "mdp", True)
        sys.stdout=sys.__stdout__
        os.system("cat adv_strat_"+str(it-1)+".txt >> it"+str(it)+"_adv.prism")
        sys.stdout=open("it"+str(it)+"_adv.prism","a")
        free_strat.run(opponent, best_deck, 2)
        suffix.run(opponent, best_deck, True)
    sys.stdout=sys.__stdout__
    os.system("prism -s -javamaxmem 100g it"+str(it)+"_adv.prism props.props -prop "+str(2-it%2)+" -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
    print "Strategy calculated, generating PRISM code.."
    sys.stdout = open("adv_strat_"+str(it)+".txt", "w")
    # Write adversary to file ( adv_strat_[it] )
    if it % 2 == 1:
        educate.run(best_deck, opponent, "tmp", 2-(it%2))
    else:
        educate.run(opponent, best_deck, "tmp", 2-(it%2))
    sys.stdout=sys.__stdout__
    return best_pair, best_score


#generate_opt_grid()

best_score = 0.0
best_deck = None
chosen_seed_deck = 1
print "Seed deck chosen as deck", chosen_seed_deck, "-- generating seed strategy."

# Find adversarial opponents of seed strategy
for opposing_team in range(1,4):
    sys.stdout = open("seed"+str(opposing_team)+".prism","w")
    prefix.run(chosen_seed_deck, opposing_team, "mdp", False)
    seed_strat.run(chosen_seed_deck, opposing_team, 1)
    free_strat.run(chosen_seed_deck, opposing_team, 2)
    suffix.run(chosen_seed_deck, opposing_team, False)
    sys.stdout = sys.__stdout__
    os.system("prism -s -nopre -javamaxmem 100g seed"+str(opposing_team)+".prism props.props -prop 2 > log.txt")
    result = find_prev_result()
    print "ProbAdv_2("+str(chosen_seed_deck) + ", " + str(opposing_team) + ") = ", str(result)
    if result > best_score:
        best_score = result
        best_deck = opposing_team

# Generate first adversarial strategy
print "best deck found to be:", best_deck, " generating first adversarial strategy.."
print "deck:", str(chosen_seed_deck) ,"vs deck:", str(best_deck)
sys.stdout = open("best_seed.prism", "w")
prefix.run(chosen_seed_deck, best_deck, "mdp", True)
seed_strat.run(chosen_seed_deck, best_deck, 1)
free_strat.run(chosen_seed_deck, best_deck, 2)
suffix.run(chosen_seed_deck, best_deck, True)
sys.stdout = sys.__stdout__
os.system("prism -s -nopre -javamaxmem 100g best_seed.prism props.props -prop 2 -exportstates tmp.sta -exportadvmdp tmp.tra > log.txt")
print "strategy generated, codifying.."
sys.stdout = open("adv_strat_0.txt","w")
educate.run(chosen_seed_deck, best_deck, "tmp", 2)
sys.stdout = sys.__stdout__
print "strategy codified, beginning core loop: ..."
iteration = 1
while adversary_is_unique(iteration):
    best_deck, best_score = flip_and_run(iteration, best_deck)
    iteration+=1

#end
print "Loop found, run terminated."
