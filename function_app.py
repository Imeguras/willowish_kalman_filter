
import json
import numpy as np
import azure.functions as func
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import JulierSigmaPoints

from numpy.random import randn
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ADMIN)
# Function to predict the next state
def fx(x, dt):
    # x[0] is distance, x[1] is average speed
    distance = x[0] + x[1] * dt
    speed = x[1]
    return np.array([distance, speed])

# Function to update the measurement based on the state
def hx(x):
    # Assuming the measurement is the distance
    return np.array([x[0]])



@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
  speed = req.params.get('speed').astype(float)
  distance = req.params.get('distance').astype(float)
  timeTruth = req.params.get('timeTruth').astype(float)
  
  try:
    #
    #
    #  Create an Unscented Kalman Filter
    dim_x = 2  # Dimension of the state (distance and speed)
    dim_z = 1  # Dimension of the measurement (distance)
    
    sigmas = JulierSigmaPoints(n=2, kappa=3)
   
    unscentedF = UnscentedKalmanFilter(dim_x=dim_x, dim_z=dim_z, dt=1., hx=hx, fx=fx, points=sigmas )
    
    unscentedF.Q = Q_discrete_white_noise(dim=2, dt=1., var=1.)
    unscentedF.P = np.eye(dim_x) * 1.0
    unscentedF.R = np.array([[0.1]])  # Measurement noise covariance
    unscentedF.predict(timeTruth)
    unscentedF.update(distance)
    # return a json containing all the data
    return func.HttpResponse(json.dumps(unscentedF.x.tolist()))


  except Exception as e:
    return func.HttpResponse(f"Error: {str(e)}", status_code=500)
  
  logging.info('Python HTTP trigger function processed a request.')
  #export the result, and the state, etc...
