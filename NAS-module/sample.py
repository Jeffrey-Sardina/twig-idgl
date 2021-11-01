import random

import hyperopt, math
from hyperopt import hp, fmin, tpe
from hyperopt.mongoexp import MongoTrials, Trials

# define an objective function
def objective(args):
    case, val = args
    if case == 'case 1':
        return val
    else:
        return val ** 2

if __name__ == '__main__':
    search_space = hp.choice('a',
        [
            ('case 1', 1 + hp.lognormal('c1', 0, 1)),
            ('case 2', hp.uniform('c2', -10, 10))
        ])

    # I may not need itto be parallel; the GPU is the limiting resource
    # so CPU parallelisation on mongo may mean nothing or be worse
    trials = Trials() #MongoTrials('mongo://localhost:27017/twig_db/jobs', exp_key='exp1') #Not working yet
    best = fmin(objective, search_space, trials=trials, algo=tpe.suggest, max_evals=1000)

    print(best)
    print(hyperopt.space_eval(search_space, best))
