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

generate_opt_grid()




"""
sys.stdout = open("test_model_2.prism","w")
prefix.run(1,3,"mdp",0)
sys.stdout = sys.__stdout__
os.system("cat test_adversary.txt >> test_model_2.prism")
sys.stdout = open("test_model_2.prism","a")
free_strat.run(1,3,2)
suffix.run(1,3,0)
sys.stdout = sys.__stdout__
"""
