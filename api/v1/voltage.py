
from flask_restful import Resource

from common import read_counter

class phase1_voltage(Resource):
    def get():
        voltage = read_counter(50520)
        if voltage != None:
            return {'value':voltage}
        else:
            return {'error':'no value'}, 500

class phase2_voltage(Resource):
    def get():
        voltage = read_counter(50522)
        if voltage != None:
            return {'value':voltage}
        else:
            return {'error':'no value'}, 500

class phase3_voltage(Resource):
    def get():
        voltage = read_counter(50524)
        if voltage != None:
            return {'value':voltage}
        else:
            return {'error':'no value'}, 500
