from config import db
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas', cascade='delete')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', cascade='delete')
    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')
  
    @validates("price")
    def validate_price(self, key, price):
        if (price < 1) or (price > 30):
            raise ValueError("price must be more than $1 and less than $30")
        return price
    
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates='restaurant')

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"