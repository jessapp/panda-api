from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
# from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import (reqparse, abort, fields, marshal_with,
                               marshal)
from json import dumps

engine = create_engine('sqlite:///panda.db')

app = Flask(__name__)
api = Api(app)
# db = SQLAlchemy(app)


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

    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('panda_name', type=str, help='Panda name')
            parser.add_argument('pandaid', type=str, help='Panda ID')
            parser.add_argument('panda_zoo', type=str, help='Panda zoo')
            parser.add_argument('panda_city', type=str, help='Panda city')
            parser.add_argument('panda_state', type=str, help='Panda state')
            parser.add_argument('panda_country', type=str, help='country')
            args = parser.parse_args()

            panda_name = args['panda_name']
            panda_num = args['pandaid']
            panda_zoo = args['panda_zoo']
            panda_city = args['panda_city']
            panda_state = args['panda_state']
            panda_country = args['panda_country']

            # Add args to the DB

            conn = engine.connect()

            add_to_db = conn.execute("INSERT INTO panda (PANDA_ID, NAME, ZOO, CITY, STATE, COUNTRY) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (panda_num, panda_name, panda_zoo, panda_city, panda_state, panda_country))

            return jsonify({"New Panda": {'Name': args['panda_name'], 'PandaID': args['pandaid']}})

        except Exception as e:
            return {'error': str(e)}



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
            print type(line)
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