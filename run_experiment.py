import sys
import prefix, suffix, free_strat

sys.stdout = open("test_model.prism","w")
prefix.run(1,3,"mdp")
free_strat.run(1,3,1)
free_strat.run(1,3,2)
suffix.run(1,3,0)
sys.stdout = sys.__stdout__
