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

def is_guardian(actor):
    if len(actor) != 4:
        return False
    query_team = int(actor[1])
    query_card = int(actor[3]) - 1
    if query_team == 1:
        if p1_deck[query_card] == "G":
            return True
    else:
        if p2_deck[query_card] == "G":
            return True
    return False

def gen_archer_guard_health(bool):
    if bool:
        return "> 0"
    return "<= 0"

# Difficult:
# Takes list of archer targets and archer reference and generates command to hit (giving all possible permutations)
def gen_archer_comm(attacks, actor):
    # hits 4
    acc = actor + "_acc"
    dmg = actor + "_dmg"
    for j in range(4,0,-1):
        if len(attacks) == j:
            if j > 1:
                print "\t\tpow(" + acc + "," + str(j) + ")\t\t:",
            else:
                print "\t\t" + acc + "\t\t:",
            for t in range(len(attacks)):
                print "(" + attacks[t] + "' = " + attacks[t] + " - " + dmg + ")",
                if t < j-1:
                    print "&",
                if t == 1 and j > 2:
                    print "\n\t\t\t\t\t",
                if t == j-1:
                    print "& (action' = 39) +"
    # hits all but one (1/2, 2/3 or 3/4)
        if len(attacks)-1 == j:
            for i in range(len(attacks)):
                print "\t\tpow(" + acc + "," + str(j) + ")*pow(1-" + acc + "," + str(len(attacks)-(j)) + ")\n\t\t\t\t\t:",
                for act_index in range(len(attacks)):
                    if act_index != i:
                        hit = attacks[act_index]
                        print "(" + hit + "' = " + hit + " - " + dmg + ")",
                        if act_index < len(attacks):
                            print "&",
                        if act_index == 2 and len(attacks) > 2:
                            print "\n\t\t\t\t\t",
                print "(action' = 39) + "
    # hits all but two (2/4 or 1/3)
        if len(attacks)-2 == j:
            if len(attacks) == 4:
                for a in [1,0]:
                    for b in [1,0]:
                        for c in [1,0]:
                            for d in [1,0]:
                                if a+b+c+d == 2:
                                    print "\t\tpow(" + acc + ",2)*pow(1-" + acc +",2)\n\t\t\t\t\t:",
                                    output_6_archer_comm = ""
                                    if a:
                                        output_6_archer_comm += "(" + attacks[0] + "' = " + attacks[0] + " - " + dmg + ") & "
                                    if b:
                                        output_6_archer_comm += "(" + attacks[1] + "' = " + attacks[1] + " - " + dmg + ")"
                                        if a:
                                            output_6_archer_comm += " + "
                                            print output_6_archer_comm
                                            break
                                        else:
                                            output_6_archer_comm += " & "
                                    if c:
                                        output_6_archer_comm += "(" + attacks[2] + "' = " + attacks[2] + " - " + dmg + ")"
                                        if a or b:
                                            output_6_archer_comm += " + "
                                            print output_6_archer_comm
                                            break
                                        else:
                                            output_6_archer_comm += " & "
                                    if d:
                                        output_6_archer_comm += "(" + attacks[3] + "' = " + attacks[3] + " - " + dmg + ") +"
                                    print output_6_archer_comm
            else:
                for i in range(len(attacks)):
                    print "\t\tpow(" + acc + "," + str(j) + ")*pow(1-" + acc + "," + str(len(attacks)-(j)) + ")\n\t\t\t\t\t:",
                    for act_index in range(len(attacks)):
                        if act_index == i:
                            hit = attacks[act_index]
                            print "(" + hit + "' = " + hit + " - " + dmg + ")",
                            if act_index < len(attacks):
                                print "&",
                            if act_index == 2 and len(attacks) > 2:
                                print "\n\t\t\t\t\t",
                    print "(action' = 39) +"
    # hits all but 3 (i.e. hits 1 of 4)
        if len(attacks)-3 == j:
            for i in range(len(attacks)):
                print "\t\t" + acc + "*pow(1-" + acc + "," + str(len(attacks)-(j)) + ")\n\t\t\t\t\t:",
                for act_index in range(len(attacks)):
                    if act_index == i:
                        hit = attacks[act_index]
                        print "(" + hit + "' = " + hit + " - " + dmg + ")",
                        if act_index < len(attacks):
                            print "&",
                        if act_index == 2 and len(attacks) > 2:
                            print "\n\t\t\t\t\t",
                print "(action' = 39) +"
    # hits none
    if len(attacks) > 1:
        print "\t\tpow(1-"+acc+","+str(len(attacks))+")\t: (action' = 39);\n"
    else:
        print "\t\t1-"+acc+"\t\t: (action' = 39);\n"

# Takes action and index and prints guard and command
def display_action_guard_comm(action, i):
    buff_string = "\t"
    if len(action) < 8:
        buff_string += "\t\t"
    elif len(action) < 14:
        buff_string += "\t"
    label = "\t[" + action + "]" + buff_string + "action = " + str(i)
    split_action = action.split("_")
    if action[:2] != "no":  # Otherwise unused...
        if "attack" in split_action:         # if the action is a standard attack action..
            """if "c" in split_action[-1]:
                target = split_action[-1] + "_hea"
            else:
                target = split_action[-1]"""
            target = split_action[-1]
            actor = split_action[0]
            if is_guardian(actor):
                # 4 labels, 4 comms (2x comms to ensure health is never negative & 2x comms to ensure hero never has > max_health)
                # g-heal can be performed
                label1 = label + " & " + target + " > " + actor + "_dmg & " + actor[:2] + " < " + actor[:2] + "_hea ->"
                # g-heal cannot be performed.
                label2 = label + " & " + target + " > " + actor + "_dmg & " + actor[:2] + " = " + actor[:2] + "_hea ->"
                label3 = label + " & " + target + " <= " + actor + "_dmg & " + actor[:2] + " < " + actor[:2] + "_hea ->"
                label4 = label + " & " + target + " <= " + actor + "_dmg & " + actor[:2] + " = " + actor[:2] + "_hea ->"
                # g-heal is possible, target_hea won't become 0
                comm1 = "\t\t" + actor + "_acc\t\t: (" + target + "' = " + target + " - " + actor + "_dmg) & (" + actor[:2]
                comm1 += "' = " + actor[:2] + " + 1) & (action' = 39) + \n\t\t1 - " + actor + "_acc\t\t: (action'= 39);"
                # etc..
                comm2 = "\t\t" + actor + "_acc\t\t: (" + target + "' = " + target + " - " + actor + "_dmg) & (action' = 39) +"
                comm2 += "\n\t\t1 - " + actor + "_acc\t\t: (action'= 39);"
                comm3 = "\t\t" + actor + "_acc\t\t: (" + target + "' = 0) & (" + actor[:2]
                comm3 += "' = " + actor[:2] + " + 1) & (action' = 39) + \n\t\t1 - " + actor + "_acc\t\t: (action'= 39);"
                comm4 = "\t\t" + actor + "_acc\t\t: (" + target + "' = 0) & (action' = 39) +"
                comm4 += "\n\t\t1 - " + actor + "_acc\t\t: (action' = 39);"
                print label1 + "\n" + comm1
                print label2 + "\n" + comm2
                print label3 + "\n" + comm3
                print label4 + "\n" + comm4 + "\n"
            elif len(actor) <= 2:           # hero attack, no accuracy
                print label + " & " + target + " > 0 ->"
                print "\t\t\t\t\t(" + target + "' = " + target + " - 1) & (action' = 39);\n"
            else:
                # 2 labels, 2 comms (second comm ensures health is never negative)
                label1 = label + " & " + target + " > " + actor + "_dmg ->"
                label2 = label + " & " + target + " <= " + actor + "_dmg ->"
                tab_buff = "\t"
                if "c" not in actor:            # Unify tab position.
                    tab_buff += "\t"
                comm1 = "\t\t" + actor + "_acc " + tab_buff + "\t: (" + target + "' = " + target + " - "
                comm1 += actor + "_dmg) & (action' = 39) +\n\t\t1 - " + actor + "_acc \t\t: (action' = 39);"
                comm2 = "\t\t" + actor + "_acc " + tab_buff + "\t: (" + target + "' = 0) & (action' = 39) +\n"
                comm2 += "\t\t1 - " + actor + "_acc \t\t: (action' = 39);"
                print label1 + "\n" + comm1
                print label2 + "\n" + comm2 + "\n"
        elif split_action[1] == "heal":         # if the action is a heal
            actor = split_action[0]
            if len(split_action[2]) > 2:
                target = actor[:2]+split_action[2]+"_hea"
            else:
                target = actor[:2]
            # can't heal fully -> heal to max.
            label1 = label + " & " + target + " >= (" + target + " - " + actor + "_dmg) ->"
            comm1 = "\t\t" + actor + "_acc\t\t: (" + target + "' = " + target + "_hea) & (action' = 39) +"
            comm1 += "\n\t\t1 -" + actor + "_acc\t\t: (action' = 39);"
            # heal fully
            label2 = label + " & " + target + " < " + target + " - " + actor + "_dmg ->"
            comm2 = "\t\t" + actor + "_acc\t\t: (" + target + "' = " + target + " + " + actor + "_dmg) & (action' = 39)+ "
            comm2 += "\n\t\t1 -" + actor + "_acc\t\t: (action' = 39);"
            print label1 + "\n" + comm1
            print label2 + "\n" + comm2 + "\n"
        elif split_action[1] == "attacks":      # if the action is a multi-target attack..
            opp = "p" + str(3-int(split_action[0][1]))
            actor = split_action[0]
            for a in [1,0]:
                for b in [1,0]:
                    for c in [1,0]:
                        label = "\t[" + action + "]" + buff_string + "action = " + str(i)
                        on_track = [a,b,c]
                        label += " & " + opp + "c1 " + gen_archer_guard_health(a) + " & " + opp + "c2 " + gen_archer_guard_health(b)
                        label += " & " + opp + "c3 " + gen_archer_guard_health(c) + " & " + opp + " > 0"
                        print label + " ->"
                        legal_attacks = [opp]
                        for k in range(len(on_track)):
                            if on_track[k]:
                                legal_attacks += [opp + "c" + str(k+1)]
                        gen_archer_comm(legal_attacks,actor)
        elif split_action[1] == "draw":         # if the action is a card-draw
            card = split_action[-1]
            print label + " & " + card + " = -1 ->"
            print "\t\t\t\t\t(" + card + "' = " + card + "_hea) & (action' = 39);\n"
        else:                                   # next turn
            print label + " & turn_clock > 0 & p1 > 0 & p2 > 0 ->\n\t\t\t\t\t(turn_clock' = 3 - turn_clock) & (action' = 0);"

# find highest card health
def find_max_card_health():
    max_health = 0
    for i in range(len(info)):
        if info[i][:4]=="hea=":
            if int(info[i][4]) > max_health:
                max_health = int(info[i][4])
    return max_health

# Main run method. Takes 2 ints for deck numbers of P1 and P2 then team to generate strat for.
def run(deck1, deck2, multiple_initial_states):
    global t, guard_pos
    print "// Actions"
    read_player_info(deck1, deck2)
    create_action_list(deck1, deck2)
    for i in range(len(action_list)):
        display_action_guard_comm(action_list[i], i)
    print "endmodule\n"
    if multiple_initial_states == 1 or multiple_initial_states == "1":
        max_health = find_max_card_health()
        print "// Multiple initial states"
        print "init"
        print "\taction = 0 & (turn_clock = 1 | turn_clock = 2) &"
        print "\tp1 > 0 & p1 < (p1_hea + 1) & p2 > 0 & p2 < (p2_hea + 1) &"
        for i in range(1,4):
            print "\t(p1c" + str(i) + " > -2 & p1c" + str(i) + " < " + str(max_health+1) + ") &",
            print "(p2c" + str(i) + " > -2 & p2c" + str(i) + " < " + str(max_health+1) + ")",
            if i != 3:
                print "&"
        print "\nendinit\n"
    else:
        print "// Single initial state"
    print 'label "p1_win" = (p1 > 0 & p2 <= 0);'
    print 'label "p2_win" = (p2 > 0 & p1 <= 0);'
