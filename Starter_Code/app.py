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
    return("""Welcome to the Hawaii weather page!""")

@app.route("/stations")
def stations():
    #station_list = session.query(Measurement.station,func.count(Measurement.station)).\
    #group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    # session.close()
    return "help"
#    station_list = list(np.ravel(station_list))
    
#    return jsonify(station_list)


if __name__ == "__main__": 
    app.run()