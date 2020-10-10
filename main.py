from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import json
import plotly
import plotly.graph_objs as go


app = Flask(__name__)


@app.route('/')
def index():
    regional_data = requests.get('https://api.rootnet.in/covid19-in/contacts')
    regional_data = regional_data.json()["data"]["contacts"]["regional"]
    notifications = requests.get('https://api.rootnet.in/covid19-in/notifications')
    notifications = notifications.json()["data"]["notifications"]
    hospital_bed = requests.get('https://api.rootnet.in/covid19-in/hospitals/beds')
    hospital_bed = hospital_bed.json()["data"]["regional"]
    medical_col_bed = requests.get('https://api.rootnet.in/covid19-in/hospitals/medical-colleges')
    medical_col_bed  = medical_col_bed.json()["data"]["medicalColleges"]
    return render_template('index.html', medical_col_bed = medical_col_bed, regional_data = regional_data, notifications = notifications, hospital_bed = hospital_bed)


def create_plot(x,y):
    data = [ go.Bar( x=x, y=y)]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
        

@app.route('/wow')
def wow():
    dataset = pd.read_csv('.\covid19india.csv')
    dataset = dataset.drop(['onsetEstimate', 'notes', 'contractedFrom' ], axis = 1)
    dataset = dataset[['patientId', 'reportedOn', 'ageEstimate','gender','state','status']] 
    deceased_df = dataset.loc[dataset['status'] == 'Deceased']
    gen_df = deceased_df.pivot_table(index=['gender'], aggfunc='size')
    gen_cat = ["female","male"]
    gen=[]
    for i in gen_df:
        gen.append(i)
    state_df = deceased_df.pivot_table(index=['state'], aggfunc='size')
    state_name = ["Bihar", "Delhi", "Gujarat", "Himachal Pradesh", "Jammu and Kashmir", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
    "Odisha", "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"]
    state_case = []
    for i in state_df:
        state_case.append(i)
    date_df = deceased_df.pivot_table(index=['reportedOn'], aggfunc='size')
    date_ddf = ["02-04-2020", "03-04-2020", "04-04-2020", "05-04-2020", "06-04-2020", "07-04-2020", "08-04-2020", "09-04-2020", "10-04-2020", "11-04-2020", "12-04-2020",
    "13-04-2020", "14-04-2020", "15-04-2020", "16-04-2020", "17-04-2020", "18-04-2020", "19-04-2020", "20-04-2020", "21-04-2020", "22-04-2020", "23-04-2020",
    "24-04-2020", "25-04-2020", "26-04-2020", "27-04-2020", "28-04-2020", "29-04-2020", "30-04-2020", "31-04-2020"]
    date_df_total = []
    for i in date_df:
        date_df_total.append(i)
    age_group = ["1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90"]
    age_death = [1,0,1,2,7,5,17,9,1]
    plot_state = create_plot(state_name, state_case)
    plot_gender = create_plot(gen_cat, gen)
    plot_age = create_plot(age_group, age_death)
    plot_date = create_plot(date_ddf, date_df_total)
    return render_template('deceased.html',  plot_state = plot_state, plot_gender = plot_gender, plot_age = plot_age, plot_date = plot_date)


@app.route('/api')
def api():
    dataset = pd.read_csv('.\covid19india.csv')
    dataset = dataset.drop(['onsetEstimate', 'notes', 'contractedFrom' ], axis = 1)
    dataset = dataset[['patientId', 'reportedOn', 'ageEstimate','gender','state','status']]
    dataset = dataset.to_dict()
    return jsonify(dataset)


if __name__ == "__main__":
    app.run(debug=True)