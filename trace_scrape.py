f = open("terminal_trace_1.txt", "r")
lines = f.readlines()
opponent = 1                            # Initialise as seed team
for i in range(len(lines)):
    if lines[i][:9] == "Iteration":
        print lines[i][:13], "- Opponent:", str(opponent)
        it_res = [0,0,0]
        for j in range(1,4):
            it_res[j-1] = float(lines[i+j][lines[i+j].find(".")-1:-1])
        print "\t", it_res
        new_opp = None
        best_v = 0
        for v_it in range(len(it_res)):
            if it_res[v_it] > best_v:
                best_v = it_res[v_it]
                opponent = v_it + 1
        """if lines[i][:7] == "ProbAdv":
            print lines[i]
        """
