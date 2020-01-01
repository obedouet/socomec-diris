
from flask_restful import Resource

from v1.common import read_counter

class total_real_power(Resource):
    def get(self):
        power = read_counter(790)
        if power != None:
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            else:
                return int(power)
        else:
            return {'error':'no value'}, 500

class total_apparent_power(Resource):
    def get(self):
        power = read_counter(794)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase1_apparent_power(Resource):
    def get(self):
        power = read_counter(50556)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase1_real_power(Resource):
    def get(self):
        power = read_counter(50544)
        if power != None:
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            else:
                return int(power)
        else:
            return {'error':'no value'}, 500

class phase1_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase1_power_factor(Resource):
    def get(self):
        factor = read_counter(50562)
        if factor != None:
            return int(factor)
        else:
            return {'error':'no value'}, 500

class phase2_apparent_power(Resource):
    def get(self):
        power = read_counter(50558)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase2_real_power(Resource):
    def get(self):
        power = read_counter(50546)
        if power != None:
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            else:
                return int(power)
        else:
            return {'error':'no value'}, 500

class phase2_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase2_power_factor(Resource):
    def get(self):
        factor = read_counter(50564)
        if factor != None:
            return int(factor)
        else:
            return {'error':'no value'}, 500

class phase3_apparent_power(Resource):
    def get(self):
        power = read_counter(50560)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase3_real_power(Resource):
    def get(self):
        power = read_counter(50548)
        if power != None:
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            else:
                return int(power)
        else:
            return {'error':'no value'}, 500

class phase3_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power != None:
            return int(power)
        else:
            return {'error':'no value'}, 500

class phase3_power_factor(Resource):
    def get(self):
        factor = read_counter(50564)
        if factor != None:
            return int(factor)
        else:
            return {'error':'no value'}, 500