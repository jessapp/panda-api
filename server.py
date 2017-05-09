from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask.ext.restful import (reqparse, abort, fields, marshal_with,
                               marshal)
from json import dumps

engine = create_engine('sqlite:///panda.db')

app = Flask(__name__)
api = Api(app)


new_pandas = []

fields = {
    'panda': fields.String
}

class Pandas(Resource):
    """Return all pandas"""

    def get(self):

        conn = engine.connect()

        query = conn.execute("SELECT * FROM panda")

        results = {}

        for line in query:
            panda_results = {}

            panda_id = line[0]
            name = line[1]
            panda_results['NAME'] = name

            zoo = line[2]
            panda_results['ZOO'] = zoo

            city = line[3]
            panda_results['CITY'] = city

            state = line[4]
            if state != "":
                panda_results['STATE'] = state

            country = line[5]
            panda_results['COUNTRY'] = country

            results[panda_id] = panda_results

        return jsonify(results)

class AddPanda(Resource):
    """Add new panda"""

    # Error!

    def post(self):

        json_data = request.get_json(force=True)
        panda_id = json_data['PANDA_ID']
        name = json_data['name']

        return jsonify(panda_id=panda_id, name=name)



class Countries(Resource):
    """Get panda information by country"""

    def get(self, country):

        conn = engine.connect()

        query = conn.execute("SELECT * FROM panda WHERE country='%s'" % country.upper())

        results = {}

        for line in query:
            panda_results = {}

            panda_id = line[0]
            name = line[1]
            panda_results['NAME'] = name

            zoo = line[2]
            panda_results['ZOO'] = zoo

            city = line[3]
            panda_results['CITY'] = city

            state = line[4]
            if state != "":
                panda_results['STATE'] = state

            country = line[5]
            panda_results['COUNTRY'] = country

            results[panda_id] = panda_results

        return jsonify(results)

class PandaID(Resource):
    """Get panda by ID"""

    def get(self, panda_id):

        conn = engine.connect()

        query = conn.execute("SELECT * FROM panda WHERE panda_id='%s'" % str(panda_id))

        results = {}

        for line in query:
            panda_results = {}

            panda_id = line[0]
            name = line[1]
            panda_results['NAME'] = name

            zoo = line[2]
            panda_results['ZOO'] = zoo

            city = line[3]
            panda_results['CITY'] = city

            state = line[4]
            if state != "":
                panda_results['STATE'] = state

            country = line[5]
            panda_results['COUNTRY'] = country

            results[panda_id] = panda_results


        return jsonify(results)



api.add_resource(Pandas, '/pandas')
api.add_resource(Countries, '/location/<string:country>')
api.add_resource(PandaID, '/id/<string:panda_id>')
api.add_resource(AddPanda, '/addpanda')


if __name__ == '__main__':
     app.run()