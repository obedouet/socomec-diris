from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from v1.voltage import phase1_voltage, phase2_voltage, phase3_voltage, phase1_frequency
from v1.amperage import *
from v1.power import *

app = Flask(__name__)
api = Api(app)

api.add_resource(total_real_power, '/total/real')
api.add_resource(phase1_voltage,'/phase1/voltage')
api.add_resource(phase1_frequency,'/phase1/frequency')
api.add_resource(phase1_amp,'/phase1/amps')
api.add_resource(phase1_apparent_power, '/phase1/apparent')
api.add_resource(phase1_reactive_power, '/phase1/reactive')
api.add_resource(phase1_real_power, '/phase1/real')
api.add_resource(phase1_power_factor, '/phase1/pf')
api.add_resource(phase2_voltage,'/phase2/voltage')
api.add_resource(phase2_amp,'/phase2/amps')
api.add_resource(phase2_apparent_power, '/phase2/apparent')
api.add_resource(phase2_reactive_power, '/phase2/reactive')
api.add_resource(phase2_real_power, '/phase2/real')
api.add_resource(phase2_power_factor, '/phase2/pf')
api.add_resource(phase3_voltage,'/phase3/voltage')
api.add_resource(phase3_amp,'/phase3/amps')
api.add_resource(phase3_apparent_power, '/phase3/apparent')
api.add_resource(phase3_reactive_power, '/phase3/reactive')
api.add_resource(phase3_real_power, '/phase3/real')
api.add_resource(phase3_power_factor, '/phase3/pf')
api.add_resource(neutral_amp,'/neutral/amps')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5002)
