from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import restaurantmenu

class WebServerHandler(BaseHTTPRequestHandler):

    def send_message(self, message, responseCode = 200):
        self.send_response(responseCode)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message)
        print message

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = restaurantmenu.get_all_restaurants()
                output = ""
                output += "<html><body>"
                output += "<h1>All restaurants</h1>"
                output += "<a href='/restaurants/new'>Add new restaurant</a>"
                for restaurant in restaurants:
                    output += "<h4>%s</h4>" % restaurant.name
                    output += "<p><a href='/restaurant/edit/{0}'>Edit</a>&nbsp;&nbsp;<a href='/restaurant/delete/{0}'>Delete</a></p>".format(restaurant.id)
                output += "</body></html>"
                self.send_message(output)
                return
            if self.path.endswith("/restaurants/new"):
                output = ""
                output += "<html><body>"
                output += "<h1>Add new restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Restaurant Name:</h2><input name='name' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.send_message(output)
                return
            else:
                components = self.path.split('/')
                num_of_components = len(components)
                if num_of_components < 3:
                    raise IOError()
                category = components[num_of_components - 3]
                field_name = components[num_of_components - 2]
                id_value = components[num_of_components - 1]
                # Add restaurant
                if category == "restaurant" and field_name == "id":
                    restaurant = restaurantmenu.get_restaurant(id_value)
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Restaurant: %s</h1>" % restaurant.id
                    output += "<h2>%s</h2>" % restaurant.name
                    output += "</body></html>"
                    self.send_message(output)
                    return
                # Edit restaurant
                if category == "restaurant" and field_name == "edit":
                    restaurant = restaurantmenu.get_restaurant(id_value)
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Editing the name of restaurant: %s</h1>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/edit/{0}'><h2>New Name:<input name='name' type='text'></h2><input type='submit' value='Submit'></form>".format(id_value)
                    output += "</body></html>"
                    self.send_message(output)
                    return
                # Delete restaurant
                if category == "restaurant" and field_name == "delete":
                    restaurant = restaurantmenu.get_restaurant(id_value)
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure to delete restaurant '%s'?</h1>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/delete/{0}'><input type='submit' value='Yes, delete it!'><br><a href='/restaurants'>Nop</a></form>".format(id_value)
                    output += "</body></html>"
                    self.send_message(output)
                    return
                else:
                    raise IOError()
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # Add restaurant
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')[0]
                    restaurant = restaurantmenu.add_restaurant(name)
                    output = ""
                    output += "<html><body>"
                    output += "<h2><a href='/restaurant/id/{0}'>{1}</a> saved</h2>".format(restaurant.id, restaurant.name)
                    output += "</body></html>"
                    self.send_message(output, 301)
                return
            else:
                components = self.path.split('/')
                num_of_components = len(components)
                if num_of_components < 3:
                    raise IOError()
                category = components[num_of_components - 3]
                field_name = components[num_of_components - 2]
                id_value = components[num_of_components - 1]
                # Edit restaurant
                if category == "restaurant" and field_name == "edit":
                    ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        name = fields.get('name')[0]
                        restaurant = restaurantmenu.rename_restaurant(id_value, name)
                        output = ""
                        output += "<html><body>"
                        output += "<h2><a href='/restaurant/id/{0}'>{1}</a> is the new name.</h2>".format(restaurant.id, restaurant.name)
                        output += "</body></html>"
                        self.send_message(output, 301)
                    return
                # Delete restaurant
                if category == "restaurant" and field_name == "delete":
                    ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        name = restaurantmenu.get_restaurant(id_value).name
                        restaurantmenu.delete_restaurant(id_value)
                        output = ""
                        output += "<html><body>"
                        output += "<h2>{0} is deleted.<br><a href='/restaurants'>Back</a></h2>".format(name)
                        output += "</body></html>"
                        self.send_message(output, 301)
                    return
        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
