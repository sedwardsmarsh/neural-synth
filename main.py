# script that manages Massive communication and updating models

import audioRecorder
import geneticAlgorithm as ga

# for the first GA test, only 3 parameters are availible: 
# WT_position, Intensity, Amp: Thus we only need 3 genes 
# per individual.
gen_alg = ga.GeneticAlgorithm(pop_size=10, num_genes=3)