
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

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')
  return func.HttpResponse(
             "Ok",
             status_code=200
        )