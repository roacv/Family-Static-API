"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200
@app.route('/member/<id>', methods=['GET'])
def member(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)
    response_body = member
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def addmember():

    # this is how you can use the Family datastructure by calling its methods
    member = {}
    member['id'] = request.json.get('id')    
    member['first_name'] = request.json.get('first_name')
    member['age'] = request.json.get('age')
    member['lucky_numbers'] = request.json.get('lucky_numbers')
    
    response_body = jackson_family.add_member(member)

    return jsonify(response_body), 200
    pass


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
