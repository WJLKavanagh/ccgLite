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

# Take int of opposing player (2 for p2) returns C of a guardian or 0 if none are present
def find_guardian(opposing_team):
    candidate_deck = [p1_deck[0], p1_deck[1], p1_deck[2]]
    if opposing_team == 2:
        candidate_deck = [p2_deck[0], p2_deck[1], p2_deck[2]]
    for i in range(len(candidate_deck)):
        if candidate_deck[i] == "G":
            return i+1
    return 0

# Takes card_string (e.g. p2c1) and returns TRUE if card is a rogue
def is_rogue(card):
    candidate_deck = [p1_deck[0], p1_deck[1], p1_deck[2]]
    if card[1] == 2:
        candidate_deck = [p2_deck[0], p2_deck[1], p2_deck[2]]
    return candidate_deck[int(card[3])-1] == "R"

# Take a command from the comm_list and print the guard
def display_guard_command(action, i):
    label = "\t[player_"+str(t)+"_turn] attack = 0 & turn_clock = " + str(t) + " & "
    if action.split("_")[1] == "draw":              # Action is a card draw
        print label + action.split("_")[2] + " = -1 ->"
    elif action.split("_")[1] == "hero":            # Action is a hero attack
        if "c" not in action[-4:]:                           # Target is enemy hero
            print label + "p" + str(3-t) + "c1 < 1",
            print "& p" + str(3-t) + "c2 < 1 & p" + str(3-t) + "c3 < 1 ->"
        else:                                               # Target is enemy card
            print label + action.split("_")[-1] + " > 0",
            if guard_pos > 0 and guard_pos != int(action[-1]):
                print "& p" + str(3-t) + "c" + str(guard_pos) + " < 1 ->"
            else:
                print "->"
    elif action.split("_")[1] == "attack":          # If action belongs to K/R/G
        if len(action.split("_")) > 3:                      # Target is enemy hero
            print label + action.split("_")[0] + " > 0",
            if is_rogue(action.split("_")[0]):                  # Rogues ignore enemy track when targetting hero
                print "->"
            else:
                print "& p" + str(3-t) + "c1 < 1",
                print "& p" + str(3-t) + "c2 < 1 & p" + str(3-t) + "c3 < 1 ->"
        else:                                               # Target is enemy card
            print label + action.split("_")[0] + " > 0 & " + action.split("_")[-1] + " > 0",
            if guard_pos > 0 and guard_pos != int(action[-1]):
                print "& p" + str(3-t) + "c" + str(guard_pos) + " < 1 ->"
            else:
                print "->"
    elif action.split("_")[1] == "attacks":         # If action belongs to A
        print label + action.split("_")[0] + " > 0 ->"
    elif action.split("_")[1] == "heal":            # action belongs to P
        if "c" not in action[-4:]:                           # Target is hero
            print label + action.split("_")[0] + " > 0 & " + action[:2] + " < " + action[:2] + "_hea ->"
        else:
            if action[2:4] != action[-2:]:             # If healing self
                print label + action.split("_")[0] + " > 0 & " + action[:2] + action[-2:] + " > 0 &",
                print action[:2] + action[-2:] + " < " + action[:2] + action[-2:] + "_hea ->"
            else:
                print label + action.split("_")[0] + " > 0 &",
                print action[:2] + action[-2:] + " < " + action[:2] + action[-2:] + "_hea ->"
    else:
        print "Oh crumbs"                           # This shouldn't happen
    print "\t\t(attack' = " + str(i) + ");\t\t\t\t//" + action


# Main run method. Takes 2 ints for deck numbers of P1 and P2 then team to generate strat for.
def run(deck1, deck2, team):
    global t, guard_pos
    t = team
    print "// Player " + str(t) + ": Free strategy..."
    read_player_info(deck1, deck2)
    print p1_deck, p2_deck
    create_action_list(deck1, deck2)
    guard_pos = find_guardian(3-t)
    for i in range(len(action_list)):
        if action_list[i][1] == str(team):
            display_guard_command(action_list[i], i)
    print

run(1,3,1)      # TESTING PURPOSES
