
from flask_restful import Resource

from v1.common import read_counter

class total_real_power(Resource):
    def get(self):
        power = read_counter(790)
        if power is not None and power != '':
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            return int(power)
        return {'error':'no value'}, 500

class total_apparent_power(Resource):
    def get(self):
        power = read_counter(794)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class total_kwh(Resource):
    def get(self):
        kwh = read_counter(856)
        if kwh is not None and kwh != '':
            return int(kwh)
        return {'error':'no value'}, 500


class phase1_apparent_power(Resource):
    def get(self):
        power = read_counter(50556)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase1_real_power(Resource):
    def get(self):
        power = read_counter(50544)
        if power is not None and power != '':
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            return int(power)
        return {'error':'no value'}, 500

class phase1_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase1_power_factor(Resource):
    def get(self):
        factor = read_counter(50562)
        if factor is not None and factor != '':
            return int(factor)
        return {'error':'no value'}, 500

class phase2_apparent_power(Resource):
    def get(self):
        power = read_counter(50558)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase2_real_power(Resource):
    def get(self):
        power = read_counter(50546)
        if power is not None and power != '':
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            return int(power)
        return {'error':'no value'}, 500

class phase2_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase2_power_factor(Resource):
    def get(self):
        factor = read_counter(50564)
        if factor is not None and factor != '':
            return int(factor)
        return {'error':'no value'}, 500

class phase3_apparent_power(Resource):
    def get(self):
        power = read_counter(50560)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase3_real_power(Resource):
    def get(self):
        power = read_counter(50548)
        if power is not None and power != '':
            # Real Power must be converted
            if int(power) > 32768:
                return int(power)-65535
            return int(power)
        return {'error':'no value'}, 500

class phase3_reactive_power(Resource):
    def get(self):
        power = read_counter(50550)
        if power is not None and power != '':
            return int(power)
        return {'error':'no value'}, 500

class phase3_power_factor(Resource):
    def get(self):
        factor = read_counter(50566)
        if factor is not None and factor != '':
            return int(factor)
        return {'error':'no value'}, 500
