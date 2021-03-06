#Code adapted from: https://automl.github.io/HpBandSter/build/html/auto_examples/plot_example_6_analysis.html

import os
import matplotlib.pyplot as plt
import hpbandster.core.result as hpres
import hpbandster.visualization as hpvis

def correlation_analysis(config, save_to_disk=True):
    log_dir = os.path.join(config["bohb_log_dir"], config['run_id'])

    # load the example run from the log files
    result = hpres.logged_results_to_HBS_result(log_dir)

    # get all executed runs
    all_runs = result.get_all_runs()

    # get the 'dict' that translates config ids to the actual configurations
    id2conf = result.get_id2config_mapping()

    # Here is how you get he incumbent (best configuration)
    inc_id = result.get_incumbent_id()

    # let's grab the run on the highest budget
    inc_runs = result.get_runs_by_id(inc_id)
    inc_run = inc_runs[-1]

    # We have access to all information: the config, the loss observed during
    #optimization, and all the additional information
    # inc_loss = inc_run.loss
    # inc_config = id2conf[inc_id]['config']
    # inc_test_loss = inc_run.info['test accuracy']

    # print('Best found configuration:')
    # print(inc_config)
    # print('It achieved accuracies of %f (validation) and %f (test).'%(1-inc_loss, inc_test_loss))

    # Let's plot the observed losses grouped by budget,
    hpvis.losses_over_time(all_runs)
    plt.show()
    if save_to_disk:
        plt.savefig(os.path.join(log_dir, config["run_id"] + "_losses_over_time.png"), bbox_inches="tight")

    # the number of concurent runs,
    hpvis.concurrent_runs_over_time(all_runs)
    plt.show()
    plt.savefig(os.path.join(log_dir, config["run_id"] + "_concurrent_runs_over_time.png"), bbox_inches="tight")

    # and the number of finished runs.
    hpvis.finished_runs_over_time(all_runs)
    plt.show()
    if save_to_disk:
        plt.savefig(os.path.join(log_dir, config["run_id"] + "_finished_runs_over_time.png"), bbox_inches="tight")

    # This one visualizes the spearman rank correlation coefficients of the losses
    # between different budgets.
    hpvis.correlation_across_budgets(result)
    plt.show()
    if save_to_disk:
        plt.savefig(os.path.join(log_dir, config["run_id"] + "_correlation_across_budgets.png"), bbox_inches="tight")

    # For model based optimizers, one might wonder how much the model actually helped.
    # The next plot compares the performance of configs picked by the model vs. random ones
    hpvis.performance_histogram_model_vs_random(all_runs, id2conf)
    plt.show()
    if save_to_disk:
        plt.savefig(os.path.join(log_dir, config["run_id"] + "_performance_histogram_model_vs_random.png"), bbox_inches="tight")

def load_config(filename):
    '''
    Load the config file from disk
    '''
    import yaml

    try:
        with open(filename, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
    except:
        raise ValueError("Could not load configuration for running Twig.", filename)
    return config

if __name__ == "__main__":
    import sys
    config_file = sys.argv[1]
    config = load_config(config_file)
    correlation_analysis(config)
