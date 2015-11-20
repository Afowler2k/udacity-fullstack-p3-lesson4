from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, 
# 		  {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
# 		  {'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
# 		  {'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
# 		  {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route("/")
@app.route("/restaurants")
def showRestaurants():
	# query all restaurants and return as a list
	restaurants = session.query(Restaurant).all()
	#return "This page will show all my restaurants"
	return render_template('restaurants.html', restaurants=restaurants)

@app.route("/restaurants/JSON")
def showRestaurantsJSON():
	# query all restaurants and return as a list
	restaurants = session.query(Restaurant).all()
	#return "This page will show all my restaurants"
	return jsonify(Restaurants=[i.serialize for i in restaurants])

# define route for a new restaurant via GET (display the new restaurant page) or POST (create the restaurant in the db)
@app.route("/restaurant/new", methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("New Restaurant Created")
		return redirect(url_for('showRestaurants'))
	else:
		#return "This page will be for making new restaurants"
		return render_template('newRestaurant.html')

@app.route("/restaurant/<int:restaurant_id>/edit", methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Restaurant Successfully Edited")        
		return redirect(url_for('showRestaurants'))
	else:
		#return "This page will be for editing restaurant %s" % restaurant_id
		return render_template('editRestaurant.html', restaurant=editedItem)

@app.route("/restaurant/<int:restaurant_id>/delete", methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deletedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Restaurant Successfully Deleted")        
		return redirect(url_for('showRestaurants'))
	else:
		#return "This page will for deleting restaurant %s" % restaurant_id
		return render_template('deleteRestaurant.html', restaurant=deletedItem)

@app.route("/restaurant/<int:restaurant_id>")
@app.route("/restaurant/<int:restaurant_id>/menu")
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	#return "This page will show the menu at restaurant %s" % restaurant_id
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def showMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	#return "This page will show the menu at restaurant %s" % restaurant_id
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route("/restaurant/<int:restaurant_id>/menu/new", methods=['GET', 'POST'])
def  newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id, description=request.form['description'], price=request.form['price'])
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
	#return "This page will be for creating new menu items for restaurant %s" % restaurant_id
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def showMenuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)


@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editemItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editemItem.name = request.form['name']
		if request.form['description']:
			editemItem.description = request.form['description']
		if request.form['price']:
			editemItem.price = request.form['price']
		session.add(editemItem)
		session.commit()
		flash("Menu Item Successfully Edited")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
	#return "This page will be for editing menu item %s" %menu_id
		return render_template('editMenuItem.html', menuItem=editemItem, restaurant_id=restaurant_id)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Menu Item Successfully Deleted")        
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	#return "This page will be for deleting menu_id %s" %menu_id
	return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menuItem=deletedItem)

if __name__ == "__main__":
	# use a random key from os.urandom(24)
	app.secret_key = "\xc3,\x91Ub\xe5\xff\x15\xee~\xa7G\xd1\xee\xdfpZF|\xa7\xbe\xd9\x13'"	
	app.debug = True
	app.run(host='0.0.0.0', port=5000)