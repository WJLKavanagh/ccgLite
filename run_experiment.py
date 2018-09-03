import sys, os
import prefix, suffix, free_strat, seed_strat

"""
    file usage:
        prefix.run(deck1, deck2, model_string, multiple_initial_states)
        seed_strat.run(deck1, deck2, team)
        free_strat.run(deck1, deck2, team)
        educate.run(deck1, deck2, file_prefix, team)
        suffix.run(deck1, deck2, multiple_initial_states)

"""

sys.stdout = open("test_model_2.prism","w")
prefix.run(1,3,"mdp",0)
sys.stdout = sys.__stdout__
os.system("cat test_adversary.txt >> test_model_2.prism")
sys.stdout = open("test_model_2.prism","w")
free_strat.run(1,3,2)
suffix.run(1,3,0)
sys.stdout = sys.__stdout__
