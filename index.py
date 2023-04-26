from flask import Flask, render_template, url_for, jsonify, make_response
from sqlalchemy import create_engine, Integer, ARRAY, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from threading import *
from TrafficLights import TrafficLights


Traffic = TrafficLights()
app = Flask(__name__)

engine = create_engine('sqlite:///tl.db', connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

class TrafficTime(Base):
    __tablename__ = 'TrafficTime'
    id = Column(Integer, primary_key=True)
    Time1 = Column(Integer, default=10)
    Time2 = Column(Integer, default=10)
    Time3 = Column(Integer, default=10)
    Time4 = Column(Integer, default=10)
    Time5 = Column(Integer, default=10)

sess = Session()
TF = sess.query(TrafficTime).first()

@app.route('/SetTimer/<time>')
def SetTimer(time):
    Traffic.UpdateTimer(time)

    return make_response("All Ok", 200)

@app.route('/PrevState')
def PrevState():
    Traffic.PrevState()
    return make_response("All Ok", 200)

@app.route('/NextState')
def NextState():
    Traffic.NextState()
    return make_response("All Ok", 200)

@app.route('/ToggleTraffic/<status>')
def ToggleTraffic(status):
    if int(status) == 1: Traffic.EnableTrafficLight()
    else: Traffic.DisableTrafficLight()
    return jsonify(TrafficState=Traffic.TrafficOn)

@app.route('/PeopleRequest')
def ResponsePeople():
    return Traffic.PeopleButtonPressed()


@app.route('/GetState')
def GetState():
    UpdateDB()
    return Traffic.ResponseState()


@app.route('/BrakeTraffic')
def BrakeTraffic():
    Traffic.BrakeTrafficLight()
    return make_response("Светофор  выведен из строя ", 200)



def UpdateDB():
    if TF.Time1 != Traffic.TimeArray[0] or TF.Time2 != Traffic.TimeArray[1] or TF.Time3 != Traffic.TimeArray[2] or TF.Time4 != Traffic.TimeArray[3] or TF.Time5 != Traffic.TimeArray[4]:
       
        TF.Time1 = Traffic.TimeArray[0]
        TF.Time2 = Traffic.TimeArray[1]
        TF.Time3 = Traffic.TimeArray[2]
        TF.Time4 = Traffic.TimeArray[3]
        TF.Time5 = Traffic.TimeArray[4]
        sess.commit()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":

    Traffic.TimeArray[0] = int(TF.Time1)
    Traffic.TimeArray[1] = int(TF.Time2)
    Traffic.TimeArray[2] = int(TF.Time3)
    Traffic.TimeArray[3] = int(TF.Time4)
    Traffic.TimeArray[4] = int(TF.Time5)
    Traffic.setTime()

    Thr = Thread(target=Traffic.TrafficStart, daemon=True)
    Thr.start()

    app.run(debug=True)