from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import numpy as np



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app=Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')

def home():
    return (f"Welcome to the home page!<br/>"
          f"Here are your available routes:<br/>"
          f"/api/v1.0/precipitation<br/>"
          f"/api/v1.0/stations<br/>"
          f"/api/v1.0/tobs<br/>"
          f"/api/v1.0/start/end<br/>")


@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    prev_date=dt.date(2017,8,23)-dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurement.prcp, Measurement.date).filter(Measurement.date>prev_date).all()
    
    precipitation=[]

    for prcp, date in results:
        precipitationDict={}
        precipitationDict['prcp']=prcp
        precipitationDict['date']=date
        precipitation.append(precipitationDict)

    session.close()
    
    all_dates = list(np.ravel(precipitation))

    return jsonify(all_dates)

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to all of the stations
    stations=session.query(Measurement.station).distinct().all()

    session.close()
    all_stations = list(np.ravel(stations))
    return jsonify({"stations":all_stations})

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Previous Date calculation
    prev_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    results2=session.query(Measurement.tobs,Measurement.date).filter(Measurement.station=='USC00516128').filter(Measurement.date>prev_date).all()
    
    tobs_data=[]

    for tobs, date in results2:
        tobs_dataDict={}
        tobs_dataDict['tobs']=tobs
        tobs_dataDict['date']=date
        tobs_data.append(tobs_dataDict)
 
 
    tobs_result=list(np.ravel(tobs_data))

    session.close()

    return jsonify(tobs_result)

@app.route('/api/v1.0/<start_date>')
def start(start_date=None):
    sel=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    results=session.query(*sel).filter(Measurement.date>=start_date).all()
    temperatures=[]
    for TMIN, TMAX, TAVG in results:
        TDictionary={}
        TDictionary['TMIN']=TMIN
        TDictionary['TMAX']=TMAX
        TDictionary['TAVG']=TAVG
        temperatures.append(TDictionary)
        session.clear
    return jsonify(temperatures)

@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end(start_date=None,end_date=None):
    sel=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    results=session.query(*sel).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
    temps=list(np.ravel(results))
    session.clear
    return jsonify(temps=temps)



if __name__ == '__main__':
    app.run(debug=True)