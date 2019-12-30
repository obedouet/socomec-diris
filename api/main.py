from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from v1.voltage import phase1_voltage, phase2_voltage, phase3_voltage
from v1.power import *

app = Flask(__name__)
api = Api(app)

api.add_resource(total_real_power, '/total/real')
api.add_resource(phase1_voltage,'/phase1/voltage')
api.add_resource(phase1_apparent_power, '/phase1/apparent')
api.add_resource(phase1_reactive_power, '/phase1/reactive')
api.add_resource(phase1_real_power, '/phase1/real')
api.add_resource(phase2_voltage,'/phase2/voltage')
api.add_resource(phase2_apparent_power, '/phase3/apparent')
api.add_resource(phase2_reactive_power, '/phase3/reactive')
api.add_resource(phase2_real_power, '/phase3/real')
api.add_resource(phase3_voltage,'/phase3/voltage')
api.add_resource(phase3_apparent_power, '/phase3/apparent')
api.add_resource(phase3_reactive_power, '/phase3/reactive')
api.add_resource(phase3_real_power, '/phase3/real')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5002)