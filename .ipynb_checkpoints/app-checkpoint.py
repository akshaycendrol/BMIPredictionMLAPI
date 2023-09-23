from flask import Flask, request, redirect
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer
from flask_cors import CORS
import os
import prediction

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to, BMI prediction API!'}

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}

class GetPredictionOutput(Resource):
    def get(self):
        return {"error":"Invalid Method."}

    def post(self):
        try:
            data = request.get_json()
            predict = prediction.predict_mpg(data)
            predictOutput = predict
            return {'message': 'BMI prediction API!', 'data': predictOutput}

        except Exception as error:
            return {'error': error}

api.add_resource(Home,'/')
api.add_resource(GetPredictionOutput,'/get-bmi')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9876))
    # app.run(host='127.0.0.1', port=port)
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()