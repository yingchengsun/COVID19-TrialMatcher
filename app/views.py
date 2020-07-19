'''
Created by Jiaqi Tang
6/17/2020
'''
from app import app
from flask import Flask,render_template,request,session, url_for
from app.lib import recommendation
from app.lib import location_plot
import zipcodes

from app.lib.folium import folium
from app.lib.folium import map
from app.lib.folium.plugins import HeatMap
from app.lib.folium.plugins import MarkerCluster
from flask import Markup

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
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
    

    marker_map = folium.Map(location=[39.8283, -98.5795], zoom_start=3,  width='30%', height='30%', left = '20%')
    #marker_cluster = MarkerCluster().add_to(marker_map)

    for i in marker_loc:
        map.Marker(
            location=[i[1], i[2]],
            popup=i[0] + "<br><br>" + i[3],
            # tooltip = "nct_id"
        ).add_to( marker_map )
    for i in target_marker_loc:
        map.Marker(
            location=[i[1],i[2]],
            popup=i[0] + "<br><br>" + i[3],
            icon=map.Icon(color='red')
        ).add_to( marker_map )
   # first, force map to render as HTML, for us to dissect
    _ = marker_map._repr_html_()

    # get definition of map in body
    marker_map_div = Markup(marker_map.get_root().html.render())

    # html to be included in header
    marker_map_hdr = Markup(marker_map.get_root().header.render())

    # html to be included in <script>
    marker_map_script = Markup(marker_map.get_root().script.render())

    
    heat_map=folium.Map(location=[39.8283, -98.5795], zoom_start=3,  width='30%', height='30%',left = '21%')
    heat_map.add_child(HeatMap(heat_loc, radius=15))
    heat_map.add_child(HeatMap(target_heat_loc, radius=15))

    #heat_map.save('app/static/heat_map.html')
    _ = heat_map._repr_html_()

    # get definition of map in body
    heat_map_div = Markup(heat_map.get_root().html.render())

    # html to be included in header
    heat_map_hdr = Markup(heat_map.get_root().header.render())

    # html to be included in <script>
    heat_map_script = Markup(heat_map.get_root().script.render())


    print('Success!')
    return render_template('result_page.html',cur_id=nctid,id_list=id_list,\
                           score_list=score_list,title_list=title_list,step_score_highest=step_score_highest, 
                           marker_map_div=marker_map_div, marker_map_hdr=marker_map_hdr, marker_map_script=marker_map_script, 
                           heat_map_div=heat_map_div, heat_map_hdr=heat_map_hdr, heat_map_script=heat_map_script)
   

# @app.route('/heatmap')
# def heatmap():
#     return render_template('heat_map.html')
# @app.route('/markermap')
# def markermap():
#     return render_template('marker_map.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

