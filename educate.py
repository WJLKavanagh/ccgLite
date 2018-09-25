import collections

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

# Takes an action string, returns string of actions ID (it's index in the action list)
def find_action_id(action):
    for i in range(len(action_list)):
        if action == action_list[i]:
            return str(i)

# Take a transition file and adds all relevant transitions into a dictionary, returns ordered dictionary
def populate_transitions(file):
    transitions = {}
    for line in open(file+".tra","r").readlines()[1:]:           # First line desribes columns - ignore.
        detail = line.split()
        if "player_" + str(t) + "_turn" == detail[4]:
            transitions[detail[0]] = [detail[2],detail[4]]
        elif detail[4][:2] == "p"+str(t):
            transitions[detail[0]] = [detail[2],detail[4]]

    return transitions

# Take a state file and adds all relevant states into a dictionary, returns dictionary
def populate_states(file):
    states = {}
    for line in open(file+".sta","r").readlines()[1:]:
        state_value_pair = line.split(":")
        values = state_value_pair[1][1:-2].split(",")
        if values[-1] == "0" and values[-2] == str(t):
            states[state_value_pair[0]] = values
    return collections.OrderedDict(sorted(states.items(), key=lambda t: t[1]))

# Takes in a list describing local state and prints corresponding guard
def print_guard(values):
    print "\t[player_" + str(t) + "_turn]\taction = 0 & turn_clock = " + str(t) + " &",
    variables = ["p1", "p2", "p1c1", "p1c2", "p1c3", "p2c1", "p2c2", "p2c3"]
    for i in range(len(variables)):
        print variables[i] + " = " + values[i],
        if i < 7 and i != 3:
            print "&",
        elif i == 3:
            print "&\n\t\t\t",
        else:
            print "->"

# Takes a state_id and prints the command corresponding to action taken from that state in adv
def print_command(state_id):
    dec_state = transitions[state_id][0]
    comm_str = transitions[dec_state][1]
    print "\t\t\t1\t: (action' = " + find_action_id(comm_str) + ");"

def run(deck1, deck2, file, team):
    global t, transitions, states
    t = team
    read_player_info(deck1, deck2)
    create_action_list(deck1, deck2)
    transitions = populate_transitions(file)
    states = populate_states(file)
    print "// Educated Strategy for player " + str(t)
    for state in states:                # For every relevant state
        print_guard(states[state])          # Print the guard for said state
        print_command(state)
    print

# UPDATE POP_TRANS() TO INCLUDE ALL POSSIBLE Pt ACTIONS FOUND AFTER A PLAYER_t_TURN

#run(1,3,"tmp",1)
