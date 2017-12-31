from flask import Flask
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

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)