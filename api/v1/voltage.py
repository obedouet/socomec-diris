
from flask_restful import Resource

from v1.common import read_counter

class phase1_frequency(Resource):
    def get(self):
        frequency = read_counter(788)
        if frequency != None:
            return int(frequency)
        else:
            return {'error':'no value'}, 500

class phase1_voltage(Resource):
    def get(self):
        voltage = read_counter(50520)
        if voltage != None:
            return int(voltage)
        else:
            return {'error':'no value'}, 500

class phase2_voltage(Resource):
    def get(self):
        voltage = read_counter(50522)
        if voltage != None:
            return int(voltage)
        else:
            return {'error':'no value'}, 500

class phase3_voltage(Resource):
    def get(self):
        voltage = read_counter(50524)
        if voltage != None:
            return int(voltage)
        else:
            return {'error':'no value'}, 500
