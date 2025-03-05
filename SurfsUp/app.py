# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify
#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return("""Welcome to the Hawaii weather page! <br>
           Please select from: <br>
           /api/v1.0/precipitation <br>
           /api/v1.0/stations <br>
           /api/v1.0/tobs <br>
           /api/v1.0/start_date <br>
           /api/v1.0/start_date/end_date <br>
           Note: start_date and end_date are user defined""")

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year).all()
    precipitation = list(np.ravel(precipitation))
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_list = list(np.ravel(station_list))
    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year, Measurement.station == "USC00519281").all()
    temps = list(np.ravel(temps))
    session.close()
    return jsonify(temps)

# @app.route("/api/v1.0/<start>")
# def stats(start):
#     stats_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
#     where(Measurement.date >= start).all()
#     print(stats_start)
#     stats_start = list(np.ravel(stats_start))
#     session.close()
#     return jsonify(stats_start)

@app.route("/api/v1.0/<start>", defaults={"end":None})
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end):

    if end:
        stats_start = session.query(Measurement.date >= start, Measurement.date <= end)
    else:
        stats_start = session.query(Measurement.date>= start)
    stats_start = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    where(Measurement.date >= start).all()
    print(stats_start)
    stats_start = list(np.ravel(stats_start))
    session.close()
    return jsonify(stats_start)

if __name__ == "__main__": 
    app.run()