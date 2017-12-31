from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def get_all_restaurants():
    restaurants = session.query(Restaurant).all()
    print restaurants
    return restaurants

def get_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    print restaurant
    return restaurant

def add_restaurant(name):
    restaurant = Restaurant(name = name)
    session.add(restaurant)
    session.commit()
    print restaurant
    return restaurant

def rename_restaurant(restaurant_id, newName):
    restaurant = get_restaurant(restaurant_id)
    restaurant.name = newName
    session.add(restaurant)
    session.commit()
    print restaurant
    return restaurant

def delete_restaurant(restaurant_id):
    restaurant = get_restaurant(restaurant_id)
    session.delete(restaurant)
    session.commit()
    return

def get_all_menu_items():
    items = session.query(MenuItem).all()
    print items
    return items