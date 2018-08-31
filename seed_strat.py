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


# Takes card_string (e.g. p2c1) and returns TRUE if card is a rogue
def is_rogue(card):
    candidate_deck = [p1_deck[0], p1_deck[1], p1_deck[2]]
    if card[1] == 2:
        candidate_deck = [p2_deck[0], p2_deck[1], p2_deck[2]]
    return candidate_deck[int(card[3])-1] == "R"

# Takes a list of 6 status' (player c1-3, opponent c1-3) and returns a list of available actions
def find_available_actions(status):
    list_of_actions = []                # empty list of available actions, returned at end.
    #print action_list
    for action_index in range(len(action_list)):
        action = action_list[action_index]
        if action[1] != str(t):         # If action belongs to the correct team
            continue
        if "draw" in action:            # If it's a draw action...
            if status[int(action[-1])-1] == -1:     # ..On a card in the hand..
                list_of_actions += [action_index]             # .. then the action is available
        elif "attacks" in action:       # If it's an archer attack
            if status[int(action[3])-1] == 1:
                list_of_actions += [action_index]
        elif "hero" in action:          # Hero attack
            if action[-3] == "_":           # target is enemy hero...
                if status[3] + status[4] + status[5] == 0:  # No cards on opposing track
                    list_of_actions += [action_index]git
            else:
                if status[int(action[-1])+2] == 1:
                    list_of_actions += [action_index]
        elif "heal" in action and status[int(action[3])-1] == 1:             # Heal action
            if action[-2] == "p":               # Can always heal hero
                list_of_actions += [action_index]
            else:
                if status[int(action[-1])-1] == 1:
                    list_of_actions += [action_index]
        else:                           # Attack action
            if status[int(action[3])-1] == 1:       # actor is on track
                if action[-2] == "p":                   # target is hero
                    if is_rogue(action.split("_")[0]):
                        list_of_actions += [action_index]   # Rogues can always target hero
                    elif status[3] + status[4] + status[5] == 0:    # opponent track is empty
                        list_of_actions += [action_index]
                elif status[int(action[-1])+2] == 1:
                    list_of_actions += [action_index]
    return list_of_actions


# Takes a list of 6 status' (player c1-3, opponent c1-3) and prints the corresponding guard-comm.
def generate_guard_comm(status):
    available_actions = find_available_actions(status)
    # print guard
    print "\t[player_"+str(t)+"_turn] action = 0 & turn_clock = " + str(t) + " &"
    print "\t\t\t",
    for i in range(3):
        print "p" + str(t) + "c" + str(i+1),
        if status[i] == 1:
            print "> 0 &",
        else:
            print "= " + str(status[i]) + " &",
    print "\n\t\t\t",
    for j in range(3,6):
        print "p" + str(3-t) + "c" + str(j-2),
        if status[i] == 1:
            print "> 0",
        else:
            print "< 1",
        if j < 5:
            print "&",
        else:
            print "->"
    #print command
    prob = "1/" + str(len(available_actions)) + ":"
    for k in range(len(available_actions)):
        print "\t\t" + prob + "\t(status' = " + str(available_actions[k]) + ")",
        if k < len(available_actions)-1:
            print "+"
        else: print ";"

# Main run method. Takes 2 ints for deck numbers of P1 and P2 then team to generate naive strat for.
def run(deck1, deck2, team):
    global t
    t = team
    print "// Player " + str(t) + ": Naive seed strategy..."
    read_player_info(deck1, deck2)
    create_action_list(deck1, deck2)
    # Every card on the player's team can be on the track (> 0), dead (0) or in-hand (-1)
    for c1 in [-1,0,1]:
        for c2 in [-1,0,1]:
            for c3 in [-1,0,1]:
                # Every opponent card is either on the track (> 0) or it isn't (< 1)
                for opc1 in [0,1]:
                    for opc2 in [0,1]:
                        for opc3 in [0,1]:
                            generate_guard_comm([c1,c2,c3,opc1,opc2,opc3])
    print
