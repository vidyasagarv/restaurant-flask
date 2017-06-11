## Restaurant menu

A simple web app made with Python.

### Setup

Set up VirtualBox and Vagrant to create your own server. With Vagrant installed, run:

$ vagrant up
$ vagrant ssh
$ cd <SYNCED PATH TO REPOSITORY>
Initialize and fill the database with these scripts.

$ python database_setup.py
$ python lotsofmenus.py

### Run

Run the web app project.py:

$ python project.py
The app runs on port 5000:

http://localhost:5000/

### API Endpoints

Available in JSON at the following endpoints:

List all restaurants:

http://localhost:5000/restaurants/json
List all menu items for a given RESTAURANT_ID:

http://localhost:5000/restaurants/<RESTAURANT ID>/menu/json
List a single menu item:

http://localhost:5000/restaurants/<RESTAURANT ID>/menu/<ITEM ID>/json