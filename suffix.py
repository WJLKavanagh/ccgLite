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
            for target in ["_hero", "c1", "c2", "c3"]:
                action_list += [card_string + "_attack_" + opponent + target]
        elif cards[i] == "P":
            for target in ["_hero", "_c1", "_c2", "_c3"]:
                action_list += [card_string + "_heal" + target]
        elif cards[i] == "A":
            action_list += [card_string + "_attacks_all","not_used","not_used","not_used"]
    action_list += ["next_turn"]

def display_action_guard_comm(action, i):
    buff_string = "\t"
    if len(action) < 8:
        buff_string += "\t\t"
    elif len(action) < 14:
        buff_string += "\t"
    label = "\t[" + action + "]" + buff_string + action + " = " + str(i)
    if action[:2] != "no":
        print label

    TODO

# Main run method. Takes 2 ints for deck numbers of P1 and P2 then team to generate strat for.
def run(deck1, deck2, multiple_initial_states):
    global t, guard_pos
    print "// Actions"
    read_player_info(deck1, deck2)
    print p1_deck, p2_deck
    create_action_list(deck1, deck2)
    for i in range(len(action_list)):
        display_action_guard_comm(action_list[i], i)


    print "\n\n\n"
    for i in range(len(action_list)):
        print i, "\t", action_list[i], "\t",
        if len(action_list[i]) < 8:
            print "\t\t",
        elif len(action_list[i]) < 16:
            print "\t",
        if i%2 == 1:
            print

run(1,3,1)      # TESTING PURPOSES
