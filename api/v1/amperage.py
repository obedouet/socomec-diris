
from flask_restful import Resource

from v1.common import read_counter

class phase1_amp(Resource):
    def get(self):
        amp = read_counter(50528)
        if amp != None:
            return int(amp)
        else:
            return {'error':'no value'}, 500

class phase2_amp(Resource):
    def get(self):
        amp = read_counter(50530)
        if amp != None:
            return int(amp)
        else:
            return {'error':'no value'}, 500

class phase3_amp(Resource):
    def get(self):
        amp = read_counter(50532)
        if amp != None:
            return int(amp)
        else:
            return {'error':'no value'}, 500