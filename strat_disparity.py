import os

file_max = int(input("What's the highest file number we care about? "))

for i in range(file_max, 0, -2):
    for j in range(i-2, -1, -2):
        print "Comparing " + str(i) + " to " + str(j) + ":"
        os.system("diff -U 0 adv_strat_"+str(i)+".txt adv_strat_"+str(j)+".txt | grep  ^@ | wc -l")
    print

for i in range(file_max-1, 0, -2):
    for j in range(i-2, -1, -2):
        print "Comparing " + str(i) + " to " + str(j) + ":"
        os.system("diff -U 0 adv_strat_"+str(i)+".txt adv_strat_"+str(j)+".txt | grep  ^@ | wc -l")
    print
