import sys
# Reads from info.txt and sets global values on players
def read_player_info(deck1, deck2):
    global p1_damage, p1_health, p1_deck, p2_damage, p2_health, p2_deck, info
    p1_damage = None
    p1_health = None
    p1_deck = None
    p2_damage = None
    p2_health = None
    p2_deck = None
    info = file("info.txt","r").readlines()
    deck1_string = "Deck_" + str(deck1)
    deck2_string = "Deck_" + str(deck2)
    for i in range(len(info)):
        if deck1_string + "=[" in info[i]:
            p1_deck = info[i].split("[")[1].split("]")[0]
            p1_health = int(info[i+1].split("=")[1])
            p1_damage = int(info[i+2].split("=")[1])
        if deck2_string + "=[" in info[i]:
            p2_deck = info[i].split("[")[1].split("]")[0]
            p2_health = int(info[i+1].split("=")[1])
            p2_damage = int(info[i+2].split("=")[1])

# Takes card and i and writes constants to file header
def read_card_info(card, player, index):
    index = str(index+1)
    player = str(player)
    print "\t//Card " + index + ":",
    for i in range(len(info)):
        if info[i][0:2] == "!"+card.upper():
            print info[i][1:-1]                                             # finish comment & strip \n
            print "const int p"+player+"c"+index+"_hea =",                  # print health
            print info[i+1].split("=")[1][:-1]+";"                              # print val & strip \n
            print "const int p"+player+"c"+index+"_dmg =",                  # print damage
            print info[i+2].split("=")[1][:-1]+";"
            print "const double p"+player+"c"+index+"_acc =",                # print accuracy
            print info[i+3].split("=")[1][:-1]+";"

# Print constant values in file header
def display_header(deck1, deck2):
    print "\n//Player 1:"
    print "const int p1_hea =", str(p1_health) + ";"
    print "const int p1_dmg =", str(p1_damage) + ";"
    print
    for i in range(len(p1_deck)):
        read_card_info(p1_deck[i], 1, i)
    print "//Player 2:"
    print "const int p2_hea =", str(p2_health) + ";"
    print "const int p2_dmg =", str(p2_damage) + ";"
    print
    for i in range(len(p2_deck)):
        read_card_info(p2_deck[i], 2, i)

# find highest card health
def find_max_card_health():
    max_health = 0
    for i in range(len(info)):
        if info[i][:4]=="hea=":
            if int(info[i][4]) > max_health:
                max_health = int(info[i][4])
    return max_health

# Print local variables in module header
def display_local_variables_with_init(deck1, deck2):
    max_card_health = find_max_card_health()
    print "\t//Single initial state (init calls included)"
    print "\tp1 : [0..p1_hea] init p1_hea;\t//player 1 hero health"
    print "\tp2 : [0..p2_hea] init p2_hea;\t//player 2 hero health"
    for card in ["p1c1","p1c2","p1c3","p2c1","p2c2","p2c3"]:
        print "\t" + card + " : [-1.." + str(max_card_health) + "] init -1;",
        if card == "p1c1":
            print "\t//card status/health, -1 = card in hand, 0 = card dead."
        else:
            print
    print "\tturn_clock : [0..2] init 0;\t//Whose turn is it, 0 = flip coin"
    print "\taction : [0..39] init 0;\t//What action has been chosen, 0 = action decision"
    print

# For models with multiple initial states
def display_local_variables_no_init(deck1, deck2):
    max_card_health = find_max_card_health()
    print "\t//Multiple initial states (init calls omitted)"
    print "\tp1 : [0..p1_hea];\t//player 1 hero health"
    print "\tp2 : [0..p2_hea];\t//player 2 hero health"
    for card in ["p1c1","p1c2","p1c3","p2c1","p2c2","p2c3"]:
        print "\t" + card + " : [-1.." + str(max_card_health) + "];",
        if card == "p1c1":
            print "\t//card status/health, -1 = card in hand, 0 = card dead."
        else:
            print
    print "\tturn_clock : [0..2];\t//Whose turn is it, 0 = flip coin"
    print "\taction : [0..39];\t//What action has been chosen, 0 = action decision"
    print

def create_action_list(deck1, deck2):
    global action_list
    p1 = [p1_deck[0], p1_deck[1], p1_deck[2]]
    p2 = [p2_deck[0], p2_deck[1], p2_deck[2]]
    action_list = []
    action_list += ["none"]
    for player in range(1,3):
        for card in range(1,4):
            action_list += ["p"+str(player)+"_draw_p"+str(player)+"c"+str(card)]
    for player in [("p1","p2"), ("p2","p1")]:
        for target in ["", "c1", "c2", "c3"]:
            action_list += [player[0]+"_hero_attack_" + player[1] + target]
    cards = p1+p2
    for i in range(len(cards)):
        card_string = "p1"
        opponent = "p2"
        if i > 2:
            card_string = "p2"
            opponent = "p1"
        card_string += "c" + str(i%3 + 1)
        if cards[i] in ["G", "K", "R"]:
            for target in ["", "c1", "c2", "c3"]:
                action_list += [card_string + "_attack_" + opponent + target]
        elif cards[i] == "P":
            for target in ["_"+card_string[:2], "_c1", "_c2", "_c3"]:
                action_list += [card_string + "_heal" + target]
        elif cards[i] == "A":
            action_list += [card_string + "_attacks_all","not_used","not_used","not_used"]
    action_list += ["next_turn"]

def display_smg_player_descriptions():
    print "\nplayer p1\n\t[player_1_turn]\nendplayer\n"
    print "player p2\n\t[player_2_turn]\nendplayer\n"
    print "player system"
    printed = 0
    action_list[0] = "flip_coin"
    for i in range(len(action_list)):
        if action_list[i] == "not_used":
            continue
        if printed%5 == 0:
            print "\t",
        print "[" + action_list[i] + "],",
        if (printed+1)%5 == 0:
            print "\n",
        printed += 1
    print "\nendplayer"


# Main run method. Takes 2 ints for deck numbers of P1 and P2 then model name ("mdp"/"smg" etc)
def run(deck1, deck2, model, multiple_initial_states):
    print model
    read_player_info(deck1, deck2)
    display_header(deck1, deck2)
    if model == "smg":
        create_action_list(deck1, deck2)
        display_smg_player_descriptions()
    if multiple_initial_states == 1 or multiple_initial_states == "1":
        print "\nmodule game\n"
        display_local_variables_no_init(deck1, deck2)
        print "\t[flip_coin] turn_clock = 0 ->\n\t\t0.5 : (turn_clock' = 1) + 0.5 : (turn_clock' = 2);"
    else:
        print "\nmodule game\n"
        display_local_variables_with_init(deck1, deck2)
        print "\t[flip_coin] turn_clock = 0 ->\n\t\t0.5 : (turn_clock' = 1) + 0.5 : (turn_clock' = 2);"
