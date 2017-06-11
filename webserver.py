from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBsession = sessionmaker(bind = engine)

session = DBsession()

class webserverHandler(BaseHTTPRequestHandler):
    def get_allrestaurants(self):
        restaurant_list = []
        for item in session.query(Restaurant).order_by(Restaurant.name.asc()).all():
            restaurant_list.append(item)
        return restaurant_list

    def do_GET(self):
        try:
            # List all restaurants
            if self.path.endswith("/restaurants"):
                restaurant_list = self.get_allrestaurants()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "</br><a href='/restaurants/new'>Make a new restaurant</a></br></br>"
                for item in restaurant_list:
                    output += item.name
                    output += "</br><a href='/restaurants/%s/edit'>Edit</a>" % item.id
                    output += "</br><a href='/restaurants/%s/delete'>Delete</a>" % item.id
                    output += "</br></br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            # Create a new restaurant
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "</br><h2>Make a new restaurant</h2></br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new' >"
                output += "<input name='newrestaurant' type='text' placeholder='Enter a name'>"
                output += "<input value='Create' type='submit'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
            # Edit a restaurant name
            if self.path.endswith("/edit"):
                restaurantID = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "</br><h2>"
                    output += myRestaurantQuery.name
                    output += "</h2></br>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit' >" % restaurantID
                    output += "<input name='newrestaurant' type='text' placeholder='%s' >" % myRestaurantQuery.name
                    output += "<input value='Submit' type='submit'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                return
            # Delete a restaurant name
            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body></br>"
                    output += "<h2> Are you sure you want to delete %s?</h2>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete' >" % restaurantID
                    output += "<input value='Delete' type='submit'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newrestaurant')

                # Create a new Restaurant class
                newrestaurant = Restaurant(name = messagecontent[0])
                session.add(newrestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newrestaurant')
                    restaurantID = self.path.split("/")[2]

                # Get restaurant object using restaurant ID
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    restaurantQuery.name = messagecontent[0]
                    session.add(restaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return

            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]

                # Get restaurant object using restaurant ID
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery:
                    session.delete(restaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return

        except :
            pass


def main():
    try:
        port = 5000
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()