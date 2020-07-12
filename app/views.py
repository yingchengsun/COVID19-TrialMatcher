'''
Created by Jiaqi Tang
6/17/2020
'''
from app import app
from flask import Flask,render_template,request,session
from app.lib import recommendation
from app.lib import location_plot
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import zipcodes


app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/collaboration')
def index():
    return render_template('index.html')


@app.route('/search_form')
def search_form():
    return render_template('search.html')

@app.route('/result_page')
def result_page():
    print(request.args)
    for key,value in request.args.items():
        print(key)
        print("key: {0}, value: {1}".format(key, value))
    nctid=request.args.get('nctid')
    nctcnt=int(request.args.get('nctcnt'))
    intervention_names_weight = int(request.args.get('intervention_name'))
    condition_names_weight= int(request.args.get('condition_name'))
    study_type_weight=int(request.args.get('study_type'))
    primary_purpose_weight = int(request.args.get('primary_purpose'))
    outcome_measure_weight = int(request.args.get('outcome_measure'))
    intervention_type_weight = int(request.args.get('intervention_type'))
    phase_weight = int(request.args.get('phase'))
    int_obs_weight = int(request.args.get('int_obs'))
    location_weight = int(request.args.get('location'))
    allocation_weight = int(request.args.get('allocation'))
    masking_weight = int(request.args.get('masking'))
    start_date_weight = int(request.args.get('start_date'))
    gender_weight = int(request.args.get('gender'))
    age_weight = int(request.args.get('age'))
    healthy_volunteers_weight = int(request.args.get('healthy_volunteers'))
    result,step_score_highest=recommendation.find_n_highest_score(nctid,nctcnt,intervention_names_weight,condition_names_weight,study_type_weight,\
                                               primary_purpose_weight,outcome_measure_weight,intervention_type_weight,\
                                               phase_weight,int_obs_weight,location_weight,allocation_weight,masking_weight,start_date_weight,\
                                               gender_weight,age_weight,healthy_volunteers_weight)

    id_list=[i[0] for i in result]
    score_list=[i[1] for i in result]
    title_list=[i[2] for i in result]


    marker_loc,heat_loc=location_plot.extract_information(id_list)
    target_marker_loc,target_heat_loc=location_plot.extract_information([nctid])
    heat_map=folium.Map(location=[39.8283, -98.5795], zoom_start=3)
    heat_map.add_child(HeatMap(heat_loc, radius=15))
    heat_map.add_child(HeatMap(target_heat_loc, radius=15))
    heat_map.save('app/templates/heat_map.html')

    marker_map = folium.Map(location=[39.8283, -98.5795], zoom_start=3)
    #marker_cluster = MarkerCluster().add_to(marker_map)

    for i in marker_loc:
        folium.Marker(
            location=[i[1], i[2]],
            popup=i[0] + "<br><br>" + i[3],
            # tooltip = "nct_id"
        ).add_to(marker_map)
    for i in target_marker_loc:
        folium.Marker(
            location=[i[1],i[2]],
            popup=i[0] + "<br><br>" + i[3],
            icon=folium.Icon(color='red')
        ).add_to(marker_map)
    marker_map.save('app/templates/marker_map.html')

    print('Success!')
    return render_template('result_page.html',cur_id=nctid,id_list=id_list,\
                           score_list=score_list,title_list=title_list,step_score_highest=step_score_highest)



@app.route('/heatmap')
def heatmap():
    return render_template('heat_map.html')
@app.route('/markermap')
def markermap():
    return render_template('marker_map.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

