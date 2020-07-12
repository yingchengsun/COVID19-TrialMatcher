import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from collections import defaultdict
from .overlap import *

root='app/resources/'
aact_trial=pd.read_csv(root+'aact_trial_web.csv')
aact_trial_info=pd.read_csv(root+'aact_trial_info.csv')

with open(root+'outcome_measures_embedding.pickle','rb') as handle:
    outcome_measure_dict=pickle.load(handle)


def find_n_highest_score(nct,n,intervention_names_weight, condition_names_weight, study_type_weight,\
                        primary_purpose_weight, outcome_measure_weight, intervention_type_weight,\
                        phase_weight,int_obs_weight,location_weight,allocation_weight,masking_weight,\
                        start_date_weight,gender_weight,age_weight,healthy_volunteers_weight):
    '''find the n highest score and nct pairs
    
    Args:
        nct: nct_id
        n: the number of highest score
    Returns:
        highest_score: list of n nct_id and score pairs with highest scores
        step_score_highest: overlap score for each feature of the selected nctids which have the highest similarity score
    
    '''
    total_weight = intervention_names_weight + condition_names_weight + study_type_weight + \
                   primary_purpose_weight + outcome_measure_weight + intervention_type_weight + phase_weight + int_obs_weight + location_weight + \
                   allocation_weight + masking_weight + start_date_weight + gender_weight + age_weight + healthy_volunteers_weight
    score_list=[]
    step_score_list=[]
    max_zipcode_length=find_max_zipcode_overlap_length(nct)
    max_condition_length=find_max_condition_names_overlap_length(nct)
    max_intervention_length=find_max_intervention_names_overlap_length(nct)
    max_intervention_type_length=find_max_intervention_type_overlap_length(nct)
    
    for i,title in zip(aact_trial.nct_id,aact_trial.brief_title):
        if i!=nct:
            if max_intervention_length==0:
                intervention_names_score=0
            else:
                intervention_names_score=compute_normalized_intervention_names_overlap_between_pairs(nct,i,max_intervention_length)
                
            if max_intervention_type_length==0:
                intervention_type_score=0
            else:
                intervention_type_score=compute_normalized_intervention_type_overlap_between_pairs(nct,i,max_intervention_type_length)
            
            if max_condition_length==0:
                condition_names_score=0
            else:
                condition_names_score=compute_normalized_condition_names_overlap_between_pairs(nct,i,max_condition_length)
                
            
            if max_zipcode_length==0:
                location_score=0
            else:
                location_score=compute_normalized_zip_overlap_between_pairs(nct,i,max_zipcode_length)
                            
            study_type_score=compute_single_feature_standardized_similarity('study_type',nct,i)
            primary_purpose_score=compute_single_feature_standardized_similarity('primary_purpose',nct,i)
            phase_score=compute_single_feature_standardized_similarity('phase',nct,i)
            int_obs_score=compute_single_feature_standardized_similarity('int_and_obs_model',nct,i)
            allocation_score=compute_single_feature_standardized_similarity('allocation',nct,i)
            masking_score=compute_single_feature_standardized_similarity('masking',nct,i)
            start_date_score=compute_single_feature_standardized_similarity('start_date',nct,i) 
            gender_score=compute_single_feature_standardized_similarity('gender',nct,i)
            age_score=compute_single_feature_standardized_similarity('minimum_age',nct,i)
            healthy_volunteers_score=compute_single_feature_standardized_similarity('healthy_volunteers',nct,i)
            outcome_measure_score=compute_outcome_measure_standardized_similarity(nct,i,outcome_measure_dict)
            
            
            total_score=(intervention_names_score*intervention_names_weight + \
                         condition_names_score*condition_names_weight + \
                         study_type_score * study_type_weight + \
                         primary_purpose_score * primary_purpose_weight + \
                         outcome_measure_score * outcome_measure_weight + \
                         intervention_type_score*intervention_type_weight+\
                         phase_score * phase_weight + \
                         int_obs_score * int_obs_weight + \
                         location_score*location_weight   + \
                         allocation_score * allocation_weight + \
                         masking_score * masking_weight + \
                         start_date_score * start_date_weight + \
                         gender_score * gender_weight + \
                         age_score * age_weight + \
                         healthy_volunteers_score * healthy_volunteers_weight) / total_weight
            
            location_overlap=find_zip_overlap_number(nct,i)
            condition_names_overlap=find_condition_names_overlap_number(nct,i)
            intervention_names_overlap=find_intervention_names_overlap_number(nct,i)
            intervention_type_overlap=find_intervention_type_overlap_number(nct,i)
            step_score_list.append([i,intervention_names_overlap,condition_names_overlap,\
                                study_type_score,primary_purpose_score,outcome_measure_score,\
                                intervention_type_overlap,phase_score,int_obs_score,location_overlap, \
                                 allocation_score,masking_score,start_date_score,  \
                                 gender_score ,age_score,healthy_volunteers_score])
            
            
            score_list.append([i,total_score,title])
    sorted_score_list=sorted(score_list,key=lambda x:x[1],reverse=True)
    highest_score=sorted_score_list[:n]

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


