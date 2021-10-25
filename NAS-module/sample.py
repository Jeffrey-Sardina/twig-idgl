import random

from hyperopt import hp, fmin, tpe
from hyperopt.mongoexp import MongoTrials

# define an objective function
def objective(args):
    # Reference the GNN-module
    import math
    return math.sin

search_space = hp.uniform('x', -2, 2)

trials = MongoTrials('mongo://mongo:27017/twig_db/jobs', exp_key='exp1')
best = fmin(objective, search_space, trials=trials, algo=tpe.suggest, max_evals=10)

print(best)
# -> {'a': 1, 'c2': 0.01420615366247227}
print(hyperopt.space_eval(space, best))
# -> ('case 2', 0.01420615366247227}




def BOHB_sample(D, p, q, N_s, N_min):
    """
    As described in Falkner et al, 2018
    Paramaters (descriptions adapted from Falkner et al, 2018):
        D, observations
        p, fraction of random runs as a flot on (0,1)
        q, percentile
        N_s, number of samples
        N_min, minimum number of points in a model
    """

    if random.random() < p:
        return random_configuration()
    
    b = 0 #budget
    if b == None:
        return random_configuration()

    alpha = 0 #qth percentile of obs's in D_b
    


def random_configuration():
    return None
