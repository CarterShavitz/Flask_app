from flask import Flask, request, jsonify
from service import FoodService
from models import Schema

import json

app = Flask(__name__)


@app.after_request
def add_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "*"
   response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
   response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
   return response

@app.route("/")
def hello():
   return "Hello World!"


@app.route("/<name>")
def hello_name(name):
   return "Hello " + name


@app.route("/food", methods=["GET"])
def list_food():
   return jsonify(FoodService().list())


@app.route("/food", methods=["POST"])
def create_food():
   return jsonify(FoodService().create(request.get_json()))


@app.route("/food/<item_id>", methods=["PUT"])
def update_item(item_id):
   return jsonify(FoodService().update(item_id, request.get_json()))

@app.route("/food/<item_id>", methods=["GET"])
def get_item(item_id):
   return jsonify(FoodService().get_by_id(item_id))

@app.route("/food/<item_id>", methods=["DELETE"])
def delete_item(item_id):
   return jsonify(FoodService().delete(item_id))


if __name__ == "__main__":
   Schema()
   app.run(debug=True, host='127.0.0.1', port=5000)
