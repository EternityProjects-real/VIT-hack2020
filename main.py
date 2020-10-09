#main code for the backend
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///database.db'

# db = SQLAlchemy(app)

@app.route('/')
def index():
    r = requests.get('https://api.rootnet.in/covid19-in/contacts')
    r = r.json()["data"]["contacts"]["regional"]
    q = requests.get('https://api.rootnet.in/covid19-in/notifications')
    q = q.json()["data"]["notifications"]
    h = requests.get('https://api.rootnet.in/covid19-in/hospitals/beds')
    h = h.json()["data"]["regional"]
    m = requests.get('https://api.rootnet.in/covid19-in/hospitals/medical-colleges')
    m  = m.json()["data"]["medicalColleges"]
    return render_template('index.html', r = r, q= q, h = h, m =m )

if __name__ == "__main__":
    app.run(debug=True)