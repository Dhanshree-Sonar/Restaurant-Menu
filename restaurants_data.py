from flask import Flask, render_template, request, url_for, redirect, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurant_list = session.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in restaurant_list])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenusJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    return jsonify(MenuItem = item.serialize)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    #return "This page will show Restaurant list"
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    #return "This page will show add option for new Restaurant"
    if request.method == 'POST':
        new_restaurant = Restaurant(name = request.form['rest_name'])
        session.add(new_restaurant)
        session.commit()
        message = "New Restaurant '" + request.form['rest_name'] + "' added to the list!!"
        flash(message)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    #return "This page will show edit option for Restaurant"
    edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    old_restaurant_name = edit_restaurant.name
    if request.method == 'POST':
        edit_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        edit_restaurant.name = request.form['rest_name']
        session.add(edit_restaurant)
        session.commit()
        message = "Restaurant '" + old_restaurant_name + "' updated to '" + request.form['rest_name'] + "'!!"
        flash(message)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurant_name = edit_restaurant.name)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    #return "This page will show delete option for Restaurant"
    del_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    old_restaurant_name = del_restaurant.name
    if request.method == 'POST':
        session.delete(del_restaurant)
        session.commit()
        message = "Restaurant '" + old_restaurant_name + "' deleted from the list!!"
        flash(message)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, restaurant_name = del_restaurant.name)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    #return "This page will show Menu Item list for restaurant"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant_id = restaurant.id, restaurant_name = restaurant.name, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    #return "This page will show option to add new menu item for restaurant"
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['new_name'],restaurant_id = restaurant_id,
                        price = request.form['new_price'], description = request.form['new_description'],
                        course = request.form['new_course'])
        session.add(new_item)
        session.commit()
        message = "New Menu Item '" + request.form['new_name'] + "' added to the list!!"
        flash(message)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    #return "This page will show option to edit menu item for restaurant"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    old_item_name = item.name
    if request.method == 'POST':
        item.name = request.form['new_name']
        item.price = request.form['new_price']
        item.description = request.form['new_description']
        item.course = request.form['new_course']
        session.add(item)
        session.commit()
        message = "Menu Item '" + old_item_name + "' has been updated!!"
        flash(message)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id,
                                restaurant_name = restaurant.name, item = item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    #return "This page will show option to delete menu item for restaurant"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    old_item_name = item.name
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        message = "Menu Item '" + old_item_name + "' deleted from the list!!"
        flash(message)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id,
                            restaurant_name = restaurant.name, item_name = item.name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
