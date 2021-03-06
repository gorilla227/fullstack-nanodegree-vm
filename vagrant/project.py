from flask import Flask, render_template
from database_setup import Base, Restaurant, MenuItem
import restaurantmenu
app = Flask(__name__)

@app.route('/')
@app.route('/menuitems')
def AllMenuItems():
    menu_items = restaurantmenu.get_all_menu_items()
    output = ""
    for item in menu_items:
        output += "{0}<br>{1}<br>{2}<br><br>".format(item.name, item.price, item.description)
    return output

@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = restaurantmenu.get_restaurant(restaurant_id)
    items = restaurantmenu.get_all_menu_items_for(restaurant_id)
    return render_template("menu.html", restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/menuitem/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/menuitem/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/menuitem/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)