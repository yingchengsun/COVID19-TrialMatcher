'''
Created by Jiaqi Tang
6/17/2020

Updated by Yincheng Sun
05/05/2021
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
from flask import Markup,request, url_for, redirect, flash
import pickle

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = 'many random bytes'

@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search_form')
def search_form():
    return render_template('search.html')

@app.route('/result_page')
def result_page():

    with open('app/resources/matrix/nct_id.pkl','rb') as handle:
        nctid_list=pickle.load(handle)

    nctid=request.args.get('nctid')
    if nctid not in nctid_list:
        flash('Your input clinical trial has not included in the system, please try another one.')
        return redirect(url_for('search_form'))
    if not request.args.get('nctcnt').isdigit():
        flash('Please enter the correct value for the "Number of Returned Trials"!')
        return redirect(url_for('search_form'))

    feature_weights={}

    nctcnt=int(request.args.get('nctcnt'))
    print (request.args)
    
    features=['intervention_name','condition_name','study_type', 'primary_purpose','outcome_measure', 'intervention_type', 'phase', 'allocation', 'masking', 
              'int_obs', 'location','start_date', 'eligibility_criteria' ]
    eligibility_criteria_rules=['gender', 'age', 'healthy_volunteers', 'high_risk_status', 'COVID_status', 'current_hosp_status', 'pregancy_status']

    for feature in features:
        feature_weights[feature] = int(request.args.get(feature))
    for feature in eligibility_criteria_rules:
        feature_weights[feature] = int(request.args.get(feature))



    result,step_score_highest=recommendation.find_n_highest_score(nctid,nctcnt,feature_weights, features, eligibility_criteria_rules)

    

    id_list=[i[0] for i in result]
    score_list=[i[1] for i in result]
    title_list=[i[2] for i in result]

    
    marker_loc,heat_loc=location_plot.extract_information(id_list)
    target_marker_loc,target_heat_loc=location_plot.extract_information([nctid])
    

   
    
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


    print('Success!')
    return render_template('result_page.html',cur_id=nctid,nctcnt=nctcnt,id_list=id_list,\
                           score_list=score_list,title_list=title_list,step_score_highest=step_score_highest,\
                           marker_map_div=marker_map_div, marker_map_hdr=marker_map_hdr, marker_map_script=marker_map_script,\
                           heat_map_div=heat_map_div, heat_map_hdr=heat_map_hdr, heat_map_script=heat_map_script,\
                           feature_weights=feature_weights
                           )
   

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


