Using Pearson correlation to acc the most important vars (|corr| > 0.3) are: (note, this does NOT distinguish max_select vs not max_select, and is not dataset specific)
- smoothness_ratio, -0.5194157841112127
- graph_skip_conn, -0.42146972247134673
- degree_ratio, -0.37686985651206195
- hidden_size, 0.3761681753760195
- learning_rate, -0.3693279231139809
- weight_decay, -0.3463355976322426

Using Pearson correlation to loss the most important vars (|corr| > 0.3) are: (note, this does NOT distinguish max_select vs not max_select, and is not dataset specific)
- weight_decay, -0.9048524617929493
- graph_skip_conn, 0.42146972247134673
- num_anchors, 0.3761242259848265 
- degree_ratio, 0.33308137046477204
- grad_accumulated_steps, -0.32125570423247923

Using Spearman correlation to acc the most important vars (|corr| > 0.3) are: (note, this does NOT distinguish max_select vs not max_select, and is not dataset specific)
- weight_decay, -0.6636363636363637
- smoothness_ratio, -0.5116883116883116
- degree_ratio, -0.36493506493506495 
- graph_skip_conn, 0.36623376623376624
- hidden_size, 0.3374515206884317

Using Spearman correlation to loss the most important vars (|corr| > 0.3) are: (note, this does NOT distinguish max_select vs not max_select, and is not dataset specific)
- degree_ratio, 0.9311688311688312
- num_anchors, 0.36883116883116884
- gl_dropout, 0.3103896103896104
- weight_decay, -0.3012987012987013

Some initial notes:
- present in all: weight_decay, degree_ratio
- present in 3: graph_skip_conn
- present in 2: smoothness_ratio, hidden_size, num_anchors
- present in only 1: gl_dropout, grad_accumulated_steps, learning_rate

There seems to be similarity between corr's for the same target (acc or loss)

Note that targeting acc is not what you "should" do -- it was just included as a test case for context.

Note that data from TwigJob_n20_bdg250_loglr_target_loss_pubmed and TwigJob_n20_bdg250_loglr_target_loss_pubmed_try2 was never included, since its training always failed with out of memory errors
