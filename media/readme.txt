This directory saves the pre-trained model.

Usage: 
1. set options['max_proposal_num'] = 1000, and predict at most 1000 proposals for each video. The items would have been ordered with joint ranking.
2. use command "python2 evaluate.py -s [json_file] -ppv 100" or "python2 evaluate_old.py -s [json_file] -ppv 100" to evaluate the top 100 proposal-caption pairs for each video.


NEW metric (meteor): 5.42
OLD metric (meteor): 9.77