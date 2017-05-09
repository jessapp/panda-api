from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

engine = create_engine('sqlite:///panda.db')

app = Flask(__name__)
api = Api(app)


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
            panda_results['name'] = name

            zoo = line[2]
            panda_results['zoo'] = zoo

            city = line[3]
            panda_results['city'] = city

            state = line[4]
            if state != "":
                panda_results['state'] = state

            country = line[5]
            panda_results['country'] = country

            results[panda_id] = panda_results

        return jsonify(results)

class PandaID(Resource):
    """Get panda by id, or add panda by id"""

    def get(self, panda_id):

        conn = engine.connect()

        query = conn.execute("SELECT * FROM pandas WHERE panda_id='%s'" % panda_id)

        results = {}

        for panda in query:
            panda_results = {}

            name = panda[0]

            zoo = panda[1]
            panda_results['zoo'] = zoo

            city = panda[2]
            panda_results['city'] = city

            state = panda[3]
            panda_results['state'] = state

            country = panda[4]
            panda_results['country'] = country

            results[name] = panda_results

            return jsonify(results)



api.add_resource(Countries, '/location/<string:country>')
api.add_resource(Names, '/id/<string:panda_id>')


if __name__ == '__main__':
     app.run()