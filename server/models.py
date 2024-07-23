from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    #Foreign Key for Pizza id 
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    #Foreign Key for Restaurant id 
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    #Relationship mapping the assignment to related pizza
    pizza = db.relationship('Pizza', back_populates='restaurant_pizza', cascade='delete')
    #Relationship mapping the assignment to related restaurant
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizza', cascade='delete')

    # add serialization rules
    serialize_rules = ('-pizza.restaurant_pizzas', '-restaurant.restaurant_pizzas')
    # add validation
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
    #Relationship mapping the restaurant to related restaurant_pizzas
    restaurant_pizza = db.relationship("RestaurantPizza", back_populates='restaurant')
    #Association proxy to get projects for this employee through assignments
    """ pizza_proxy = association_proxy('restaurant_pizzas', 'pizza',
                                 creator=lambda pizza_obj: RestaurantPizza(pizza=pizza_obj)) """
    # add serialization rules
    serialize_rules = ('-pizzas.restaurant', '-restaurant_pizzas.restaurant')

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    #relationship mapping the pizza to related pizza_restaurants 
    restaurant_pizza = db.relationship('RestaurantPizza', back_populates='pizza')
    #Association proxy to get projects for this employee through assignments
    """ restaurant_proxy = association_proxy('restaurant_pizzas', 'restaurant',
                                 creator=lambda restaurant_obj: RestaurantPizza(restaurant=restaurant_obj)) """
    # add serialization rules
    serialize_rules = ('-restaurants.pizza', '-restaurant_pizzas.pizza')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"