#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, g
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.before_request
def run_logic_before_any_route():
    if request.endpoint == 'restaurant':
        id = request.view_args.get('id')
        g.restaurant = Restaurant.query.get(id)
        if not g.restaurant:
            return {"error": "Restaurant not found"}, 404
    if request.endpoint == 'restaurant_pizza':
        id = request.view_args.get('id')
        g.restaurant_pizza = RestaurantPizza.query.get(id)
        if not g.restaurant_pizza:
            return {"error": "Restaurant Pizza not found"}, 404

class RestaurantsResource(Resource):
    def get(self):
        restaurants = [restaurant.to_dict(only=('name','address','id')) for restaurant in Restaurant.query.all()]
        return restaurants, 200
    
api.add_resource(RestaurantsResource, '/restaurants', endpoint='restaurants')

class RestaurantResource(Resource):
    def get(self, id):
        g.restaurant = Restaurant.query.get(id)
        return g.restaurant.to_dict(only=('name','address','id','restaurant_pizzas',)), 200
    
    def delete(self, id):
        db.session.delete(g.restaurant)
        db.session.commit()
        return {}, 204

api.add_resource(RestaurantResource, '/restaurants/<int:id>', endpoint='restaurant')

class PizzasResource(Resource):
    def get(self):
        pizzas = [pizza.to_dict(only=('id','ingredients','name',)) for pizza in Pizza.query.all()]
        return pizzas, 200
    
api.add_resource(PizzasResource, '/pizzas', endpoint='pizzas')

class RestaurantPizzaResource(Resource):
    def get(self):
        restaurant_pizzas = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]
        return restaurant_pizzas, 200
    
    def post(self):
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')
        try:
            g.restaurant_pizza = RestaurantPizza(price=price,pizza_id=pizza_id,restaurant_id=restaurant_id)
            db.session.add(g.restaurant_pizza)
            db.session.commit()
            return g.restaurant_pizza.to_dict(), 201 
        except: 
            return {"errors": ["validation errors"]}, 400
          
        """ except: {"errors": ["validation errors"]}, 404 """
       
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas', endpoint='restaurant_pizzas')


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
