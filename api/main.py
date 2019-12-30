from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from v1.voltage import phase1_voltage, phase2_voltage, phase3_voltage

app = Flask(__name__)
api = Api(app)

api.add_resource(phase1_voltage,'/phase1/voltage')
api.add_resource(phase2_voltage,'/phase2/voltage')
api.add_resource(phase3_voltage,'/phase3/voltage')

if __name__ == '__main__':
     app.run(host="*", port=5002)
