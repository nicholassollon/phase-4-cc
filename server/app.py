#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = Restaurant.query.all()
    rest_dict = [restaurant.to_dict(
        rules=('-restaurant_pizzas',))for restaurant in restaurants]
    response = make_response(jsonify(rest_dict), 200)
    return response


@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurantsById(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant:
        if request.method == 'GET':
                rest_dict = restaurant.to_dict(rules=('-restaurant_pizzas',))
                response = make_response(jsonify(rest_dict), 200)
        elif request.method == 'DELETE':
             
             response = make_response(jsonify(rest_dict), 200)
    else:
            response = make_response(jsonify("Restaurant not found"), 404)
    return response


@app.route('/pizzas', methods=['GET',])
def pizzas():
    pizzas = Pizza.query.all()
    pizza_dict = [pizza.to_dict(
        rules=('-restaurant_pizzas',))for pizza in pizzas]
    response = make_response(jsonify(pizza_dict), 200)
    return response

@app.route('/restaurant_pizzas', methods=['POST',])
def restaurantPizzaPost():
    try:
        new_rest_pizza = RestaurantPizza(price = request.get_json()['price'],
                                         pizza_id = request.get_json()['pizza_id'],
                                         restaurant_id = request.get_json()['restaurant_id'])
        
        db.session.add(new_rest_pizza) 
        db.session.commit()

        #not sure why but I get null back from this in postman 
        pizza = Pizza.query.filter_by(id=new_rest_pizza.id).first()
        response = make_response(jsonify(pizza),201)
        #I also tried this but that didnt work. The tests won't help me either as they continuously give me nonetype error.
        #pizza = Pizza.query.filter_by(id=new_rest_pizza.id).first()
        #pizza = pizza.to_dict(rules=('-restaurant_pizzas',))
        #response = make_response(jsonify(pizza),201)

    except ValueError:
         response = make_response(jsonify({"errors":"validation errors"}),400)
    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
