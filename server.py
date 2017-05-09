from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps

engine = create_engine('sqlite:///panda.db')

app = Flask(__name__)
api = Api(app)


class Pandas(Resource):
    """Return all pandas, or add new panda"""

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

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('PANDA_ID', type=int)
        parser.add_argument('NAME', type=str)
        parser.add_argument('ZOO', type=str)
        parser.add_argument('CITY', type=str)
        parser.add_argument('STATE', type=str)
        parser.add_argument('COUNTRY', type=str)

        args = parser.parse_args()

        panda = {'PANDA_ID': args['PANDA_ID'], 'NAME': args['NAME'], 'ZOO': args['ZOO'],
        'CITY': args['CITY'], 'STATE': args['STATE'], 'COUNTRY': args['COUNTRY']}

        # add panda to DB here?

        return 201



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


if __name__ == '__main__':
     app.run()