import subprocess

# Calculating number of states..
num_states = 5*5*5*5*5*5*5*5

file_max = int(input("What's the highest file number we care about? "))

for i in range(file_max, 0, -2):
    for j in range(i-2, -1, -2):
        res = int(subprocess.check_output("diff -U 0 adv_strat_"+str(i)+".txt adv_strat_"+str(j)+".txt | grep  ^@ | wc -l", shell=True))
        print "Comparing " + str(i) + " to " + str(j) + ": " + str(res) + ", output differs in " + str(res/num_states * 100) + "% of states"

for i in range(file_max-1, 0, -2):
    for j in range(i-2, -1, -2):
        res = int(subprocess.check_output("diff -U 0 adv_strat_"+str(i)+".txt adv_strat_"+str(j)+".txt | grep  ^@ | wc -l", shell=True))
        print "Comparing " + str(i) + " to " + str(j) + ": " + str(res) + ", output differs in " + str(res/num_states * 100) + "% of states"
