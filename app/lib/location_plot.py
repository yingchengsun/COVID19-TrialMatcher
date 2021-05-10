import pandas as pd
import zipcodes
from collections import defaultdict


aact_trial=pd.read_csv('app/resources/matrix/all_info_1007_COVID_trials.csv')


def extract_information(nct_list):

    result_list=[]
    pure_lat_long_list=[]

    selected_df=aact_trial[aact_trial['nct_id'].isin(nct_list)]

    for index,zipcode,b in zip(selected_df.nct_id,selected_df.zip_codes,selected_df.brief_title):
        if pd.isnull(zipcode)==False:
            zipcodelist=zipcode.split('|')
            for z in zipcodelist:
                z=z[:5]
                if zipcodes.matching(z):
                    current_location=[zipcodes.matching(z)[0]['lat'],zipcodes.matching(z)[0]['long']]
                    result_list.append([index,zipcodes.matching(z)[0]['lat'],zipcodes.matching(z)[0]['long'],b])
                    pure_lat_long_list.append(current_location)
    return result_list,pure_lat_long_list
