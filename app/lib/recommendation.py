import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from collections import defaultdict
import numpy as np


root='app/resources/'

aact_trial_info=pd.read_csv(root+'matrix/all_info_1007_COVID_trials.csv')
# aact_trial = aact_trial_info
with open(root+'matrix/precomputed_weights.pkl','rb') as handle:
    precomputed_scores=pickle.load(handle)

with open(root+'matrix/nct_id.pkl','rb') as handle:
    nct_id=pickle.load(handle)



def find_n_highest_score(nct,n,feature_weights,features, eligibility_criteria_rules):
    '''find the n highest score and nct pairs
    
    Args:
        nct: nct_id
        n: the number of highest score
    Returns:
        highest_score: list of n nct_id and score pairs with highest scores
        step_score_highest: overlap score for each feature of the selected nctids which have the highest similarity score
    
    '''
    
    features=features
    eligibility_criteria_rules=eligibility_criteria_rules
    target_trial_idx  = nct_id.index(nct)

    size=len(precomputed_scores['intervention_name'])
    total_score=np.zeros((1, size))
    EC_scores = np.zeros((1, size))


    EC_weight = 0
    for feature in eligibility_criteria_rules:
        EC_scores += precomputed_scores[feature][target_trial_idx] * feature_weights[feature]
        EC_weight += feature_weights[feature]
        
    if EC_weight == 0:
        precomputed_scores['eligibility_criteria'][target_trial_idx] =0
    else:
        precomputed_scores['eligibility_criteria'][target_trial_idx] = EC_scores/EC_weight*1.0

    total_weight = 0
    for feature in features:
        total_score += precomputed_scores[feature][target_trial_idx] * feature_weights[feature]
        total_weight += feature_weights[feature]

    if total_weight == 0:
        total_score =np.zeros((1, size))[0]
    else:
        total_score = (total_score/total_weight*1.0)[0]

    #score_list = total_score/total_weight*1.0
    score_list =zip(aact_trial_info.nct_id,total_score, aact_trial_info.brief_title)

    sorted_score_list=sorted(score_list,key=lambda x:x[1],reverse=True)

    highest_score=[]
    count=0
    for item in sorted_score_list:
        if item[0]!=nct:
            highest_score.append(item)
            count+=1
            if count==n:
                break

    #highest_score=sorted_score_list_new[:n]

    table_features=['nct_id', 'intervention_names', 'condition_names', \
                           'study_type', 'primary_purpose', 'outcome_measure', \
                           'phase', 'intervention_model','observation_model',  \
                           'allocation', 'masking', 'start_date', \
                           'gender',  'healthy_volunteers']
    aact_ordered=aact_trial_info[table_features]
    table_score_highest = [table_features,aact_ordered[aact_ordered['nct_id']==nct].values[0]]
    for i in highest_score:
        table_score_highest.append(aact_ordered[aact_ordered['nct_id']==i[0]].values[0])
    table_score_highest=list(map(list, zip(*table_score_highest)))
    return highest_score,table_score_highest


