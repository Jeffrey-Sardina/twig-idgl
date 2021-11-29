import sys
import glob
import os
import json
import yaml

# Dependent vars to use
def get_ids(models_folder):
    out_files = glob.glob(os.path.join(models_folder, "*.out"))
    return [os.path.basename(name).split(".")[0] for name in out_files]

def extract_scores(line):
    loss_data, acc_data = line.strip().split('|')[-2:]
    loss_data = float(loss_data.strip().replace("NLOSS = ", ""))
    acc_data = float(acc_data.strip().replace("ACC = ", ""))
    return loss_data, acc_data

def read_results(results_file):
    try:
        with open(results_file, 'r') as data:
            last_seen_loss = None
            last_seen_acc = None
            for line in data:
                if " | NLOSS = " in line:
                    last_seen_loss, last_seen_acc = extract_scores(line)
            if last_seen_loss and last_seen_acc:
                return {"loss": last_seen_loss, "acc": last_seen_acc}
            else:
                return None
    except:
        return None

def read_config(config_file):
    try:
        with open(config_file, 'r') as NA:
            return json.load(NA)
    except:
        return None

def get_varied_keys(jobfile):
    try:
        with open(jobfile, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            return config['hyperparameters'].keys()
    except:
        raise

def gather_data(models_folder, ids):
    results = {}
    configs = {}

    # Load data as dicts {run_id => data}
    missed = set()
    for run_id in ids:
        results_folder = os.path.join(models_folder, run_id, "train")
        results_file = os.path.join(results_folder, "metrics", "metrics.log")
        result = read_results(results_file)
        config_file  = os.path.join(results_folder, "config.json")
        config = read_config(config_file)

        if result and config:
            results[run_id] = result
            configs[run_id] = config
        else:
            missed.add(run_id)

    # Gather dict data into a list
    output = []
    varied_keys = get_varied_keys(os.path.join(models_folder, run_id + ".TwigJob.yml"))
    for run_id in ids:
        if run_id in missed:
            continue
        row = [run_id]
        for key in sorted(configs[run_id].keys()): #Make sure all are done in the same order!
            if key in varied_keys:
                row.append(configs[run_id][key])
        for key in sorted(results[run_id].keys()): #Make sure all are done in the same order!#
            row.append(results[run_id][key])
        output.append(row)

    # write header
    header = ['run_id']
    run_id = ids[0]
    for key in sorted(configs[run_id].keys()):
        if key in varied_keys:
            header.append(key)
    for key in sorted(results[run_id].keys()):
        header.append(key)
    output.insert(0, header)

    return output

def output_to_csv(output, out_file):
    with open(out_file, 'w') as out:
        for row in output:
            print(','.join(str(x) for x in row), file=out)

if __name__ == '__main__':
    models_folder = sys.argv[1]
    out_file = sys.argv[2]
    ids = get_ids(models_folder)
    output = gather_data(models_folder, ids)
    output_to_csv(output, out_file)
