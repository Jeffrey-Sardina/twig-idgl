## python main.py -config config/cora/idgl.yml
/root/miniconda3/envs/pyenv/lib/python3.7/site-packages/sklearn/externals/joblib/externals/cloudpickle/cloudpickle.py:47: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
main.py:58: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  config = yaml.load(setting)
**************** MODEL CONFIGURATION ****************
bignn                    -->   False
cuda_id                  -->   0
data_dir                 -->   ../data/cora/
data_type                -->   network
dataset_name             -->   cora
degree_ratio             -->   0
dropout                  -->   0.5
eary_stop_metric         -->   nloss
eps_adj                  -->   4e-5
feat_adj_dropout         -->   0.5
gat_alpha                -->   0.2
gat_nhead                -->   8
gl_dropout               -->   0.5
grad_accumulated_steps   -->   1
grad_clipping            -->   None
graph_hops               -->   2
graph_include_self       -->   False
graph_learn              -->   True
graph_learn_epsilon      -->   0
graph_learn_hidden_size  -->   70
graph_learn_num_pers     -->   4
graph_learn_ratio        -->   0
graph_learn_regularization -->   True
graph_learn_topk         -->   None
graph_metric_type        -->   weighted_cosine
graph_module             -->   gcn
graph_skip_conn          -->   0.8
graph_type               -->   dynamic
hidden_size              -->   16
learning_rate            -->   0.01
logging                  -->   True
lr_patience              -->   2
lr_reduce_factor         -->   0.5
max_epochs               -->   10000
max_iter                 -->   10
max_rl_ratio             -->   0.99
model_name               -->   GraphClf
no_cuda                  -->   False
optimizer                -->   adam
out_dir                  -->   ../out/cora/idgl
out_predictions          -->   False
out_raw_learned_adj_path -->   cora_idgl_raw_adj.npy
patience                 -->   100
pretrain_epoch           -->   0
pretrained               -->   None
print_every_epochs       -->   500
random_seed              -->   1234
rl_ratio                 -->   0
rl_ratio_power           -->   1
rl_reward_metric         -->   acc
rl_start_epoch           -->   1
rl_wmd_ratio             -->   0
save_params              -->   True
seed                     -->   42
shuffle                  -->   True
smoothness_ratio         -->   0.2
sparsity_ratio           -->   0
task_type                -->   classification
update_adj_ratio         -->   0.1
use_bert                 -->   False
verbose                  -->   20
weight_decay             -->   0.0005
**************** MODEL CONFIGURATION ****************
Traceback (most recent call last):
  File "main.py", line 127, in <module>
    main(config)
  File "main.py", line 23, in main
    model = ModelHandler(config)
  File "/workspace/IDGL/src/core/model_handler.py", line 45, in __init__
    self.logger = DummyLogger(config, dirname=config['out_dir'], pretrained=config['pretrained'])
  File "/workspace/IDGL/src/core/utils/logger.py", line 17, in __init__
    raise Exception('Directory already exists: {}'.format(dirname))
Exception: Directory already exists: ../out/cora/idgl
(pyenv) root@4715d998eeaf:/workspace/IDGL/src# rm -r ../out/cora/idgl
(pyenv) root@4715d998eeaf:/workspace/IDGL/src# python main.py -config config/cora/idgl.yml
/root/miniconda3/envs/pyenv/lib/python3.7/site-packages/sklearn/externals/joblib/externals/cloudpickle/cloudpickle.py:47: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
main.py:58: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  config = yaml.load(setting)
**************** MODEL CONFIGURATION ****************
bignn                    -->   False
cuda_id                  -->   0
data_dir                 -->   ../data/cora/
data_type                -->   network
dataset_name             -->   cora
degree_ratio             -->   0
dropout                  -->   0.5
eary_stop_metric         -->   nloss
eps_adj                  -->   4e-5
feat_adj_dropout         -->   0.5
gat_alpha                -->   0.2
gat_nhead                -->   8
gl_dropout               -->   0.5
grad_accumulated_steps   -->   1
grad_clipping            -->   None
graph_hops               -->   2
graph_include_self       -->   False
graph_learn              -->   True
graph_learn_epsilon      -->   0
graph_learn_hidden_size  -->   70
graph_learn_num_pers     -->   4
graph_learn_ratio        -->   0
graph_learn_regularization -->   True
graph_learn_topk         -->   None
graph_metric_type        -->   weighted_cosine
graph_module             -->   gcn
graph_skip_conn          -->   0.8
graph_type               -->   dynamic
hidden_size              -->   16
learning_rate            -->   0.01
logging                  -->   True
lr_patience              -->   2
lr_reduce_factor         -->   0.5
max_epochs               -->   10000
max_iter                 -->   10
max_rl_ratio             -->   0.99
model_name               -->   GraphClf
no_cuda                  -->   False
optimizer                -->   adam
out_dir                  -->   ../out/cora/idgl
out_predictions          -->   False
out_raw_learned_adj_path -->   cora_idgl_raw_adj.npy
patience                 -->   100
pretrain_epoch           -->   0
pretrained               -->   None
print_every_epochs       -->   500
random_seed              -->   1234
rl_ratio                 -->   0
rl_ratio_power           -->   1
rl_reward_metric         -->   acc
rl_start_epoch           -->   1
rl_wmd_ratio             -->   0
save_params              -->   True
seed                     -->   42
shuffle                  -->   True
smoothness_ratio         -->   0.2
sparsity_ratio           -->   0
task_type                -->   classification
update_adj_ratio         -->   0.1
use_bert                 -->   False
verbose                  -->   20
weight_decay             -->   0.0005
**************** MODEL CONFIGURATION ****************
[ Using CUDA ]
[ Using ground-truth input graph ]
[ Running GraphClf model ]
[ Multi-perspective weighted_cosine GraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Multi-perspective weighted_cosine GraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Graph Learner ]
[ Graph Regularization]
encoder.graph_encoders.0.weight: torch.Size([1433, 16])
encoder.graph_encoders.1.weight: torch.Size([16, 7])
graph_learner.weight_tensor: torch.Size([4, 1433])
graph_learner2.weight_tensor: torch.Size([4, 16])
#Parameters = 28836

<> <> <> Starting Timer [Train] <> <> <>

>>> Train Epoch: [500 / 10000]
<> <> Timer [Train] <> <> Interval [Training Epoch 500]: 0h 01m 31s <> <>
Training Epoch 500 -- Loss: 1.04003 | NLOSS = -1.04003 | ACC = 0.90714

>>> Validation Epoch: [500 / 10000]
<> <> Timer [Train] <> <> Interval [Validation Epoch 500]: 0h 00m 00s <> <>
Validation Epoch 500 -- Loss: 1.33633 | NLOSS = -1.33633 | ACC = 0.81800
<> <> <> Finished Timer [Train] <> <> <> Total time elapsed: 0h 02m 28s <> <> <>
Finished Training: ../out/cora/idgl
Training time: 148.58

<<<<<<<<<<<<<<<< MODEL SUMMARY >>>>>>>>>>>>>>>> 
Best epoch = 818; 
NLOSS = -1.25936
ACC = 0.81400

 <<<<<<<<<<<<<<<< MODEL SUMMARY >>>>>>>>>>>>>>>> 
Restoring best model
[ Loading saved model ../out/cora/idgl/params.saved ]
[ Multi-perspective weighted_cosine GraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Multi-perspective weighted_cosine GraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Graph Learner ]
[ Graph Regularization]
<> <> <> Starting Timer [Test] <> <> <>
Saved raw_learned_adj to ../out/cora/idgl/cora_idgl_raw_adj.npy
[test] | test_exs = 1000 | step: [1 / 1] | NLOSS = -1.14736 | ACC = 0.83800
<> <> <> Finished Timer [Test] <> <> <> Total time elapsed: 0h 00m 00s <> <> <>
Finished Testing: ../out/cora/idgl
Testing time: 0.06

## python main.py -config config/cora/idgl_anchor.yml
/root/miniconda3/envs/pyenv/lib/python3.7/site-packages/sklearn/externals/joblib/externals/cloudpickle/cloudpickle.py:47: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
main.py:58: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  config = yaml.load(setting)
**************** MODEL CONFIGURATION ****************
bignn                    -->   False
cuda_id                  -->   0
data_dir                 -->   ../data/cora/
data_type                -->   network
dataset_name             -->   cora
degree_ratio             -->   0
dropout                  -->   0.6
eary_stop_metric         -->   nloss
eps_adj                  -->   8.5e-05
feat_adj_dropout         -->   0.5
gat_alpha                -->   0.2
gat_nhead                -->   8
gl_dropout               -->   0
grad_accumulated_steps   -->   1
grad_clipping            -->   None
graph_hops               -->   2
graph_include_self       -->   False
graph_learn              -->   True
graph_learn_epsilon      -->   0
graph_learn_hidden_size  -->   70
graph_learn_num_pers     -->   4
graph_learn_ratio        -->   0
graph_learn_regularization -->   True
graph_learn_topk         -->   None
graph_metric_type        -->   weighted_cosine
graph_module             -->   gcn
graph_skip_conn          -->   0.8
graph_type               -->   dynamic
hidden_size              -->   16
learning_rate            -->   0.01
logging                  -->   True
lr_patience              -->   2
lr_reduce_factor         -->   0.5
max_epochs               -->   10000
max_iter                 -->   10
max_rl_ratio             -->   0.99
model_name               -->   GraphClf
no_cuda                  -->   False
num_anchors              -->   1000
optimizer                -->   adam
out_dir                  -->   ../out/cora/idgl_anchor
out_predictions          -->   False
out_raw_learned_adj_path -->   cora_idgl_node_anchor_adj.npy
patience                 -->   100
pretrain_epoch           -->   0
pretrained               -->   None
print_every_epochs       -->   500
random_seed              -->   1234
rl_ratio                 -->   0
rl_ratio_power           -->   1
rl_reward_metric         -->   acc
rl_start_epoch           -->   1
rl_wmd_ratio             -->   0
save_params              -->   True
scalable_run             -->   True
seed                     -->   42
shuffle                  -->   True
smoothness_ratio         -->   0.2
sparsity_ratio           -->   0.1
task_type                -->   classification
update_adj_ratio         -->   0.1
use_bert                 -->   False
verbose                  -->   20
weight_decay             -->   0.0005
**************** MODEL CONFIGURATION ****************
[ Using CUDA ]
[ Using ground-truth input graph ]
[ Running GraphClf model ]
[ Multi-perspective weighted_cosine AnchorGraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Multi-perspective weighted_cosine AnchorGraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Graph Learner ]
[ Graph Regularization]
encoder.graph_encoders.0.weight: torch.Size([1433, 16])
encoder.graph_encoders.1.weight: torch.Size([16, 7])
graph_learner.weight_tensor: torch.Size([4, 1433])
graph_learner2.weight_tensor: torch.Size([4, 16])
#Parameters = 28836

<> <> <> Starting Timer [Train] <> <> <>

>>> Train Epoch: [500 / 10000]
<> <> Timer [Train] <> <> Interval [Training Epoch 500]: 0h 00m 29s <> <>
Training Epoch 500 -- Loss: 0.50122 | NLOSS = -0.50122 | ACC = 1.00000

>>> Validation Epoch: [500 / 10000]
<> <> Timer [Train] <> <> Interval [Validation Epoch 500]: 0h 00m 00s <> <>
Validation Epoch 500 -- Loss: 1.40277 | NLOSS = -1.40277 | ACC = 0.81800
<> <> <> Finished Timer [Train] <> <> <> Total time elapsed: 0h 00m 45s <> <> <>
Finished Training: ../out/cora/idgl_anchor
Training time: 45.52

<<<<<<<<<<<<<<<< MODEL SUMMARY >>>>>>>>>>>>>>>> 
Best epoch = 690; 
NLOSS = -1.34469
ACC = 0.80800

 <<<<<<<<<<<<<<<< MODEL SUMMARY >>>>>>>>>>>>>>>> 
Restoring best model
[ Loading saved model ../out/cora/idgl_anchor/params.saved ]
[ Multi-perspective weighted_cosine AnchorGraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Multi-perspective weighted_cosine AnchorGraphLearner: 4 ]
[ Graph Learner metric type: weighted_cosine ]
[ Graph Learner ]
[ Graph Regularization]
<> <> <> Starting Timer [Test] <> <> <>
Saved raw_learned_adj to ../out/cora/idgl_anchor/cora_idgl_node_anchor_adj.npy
[test] | test_exs = 1000 | step: [1 / 1] | NLOSS = -1.26766 | ACC = 0.84200
<> <> <> Finished Timer [Test] <> <> <> Total time elapsed: 0h 00m 00s <> <> <>
Finished Testing: ../out/cora/idgl_anchor
Testing time: 0.03