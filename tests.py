import os
from db import *
from form import *
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
db = dbInitialize(app, MONGO_URI)

# @app.route('/')
# @app.route('/merchant/consert')
# def test_page():
#     return render_template('/consert.html', form=ConsertForm())

# if __name__ == '__main__':
#     app.run(debug=True, port=5050)


# TEST: Create User
# result = dbCreateUser(db, {
#     'username': 'Bob',
#     'password': 'abc123',
#     'email': 'bob@bobby.ca',
#     'isBulkBuyer': False,
#     'balance': 0,
#     'tickets': 0
# })

# print('User created: ', result)

# TEST: GET Users
# result = dbGetUsers(db)

# print('Users recived: ', result)

# TEST: GET User
# result = dbGetUser(db, '63ffdb922723cde71590ae36')

# print('User recived: ', result)

# TEST: UPDATE User
# print('User old: ', result)

# result = dbUpdateUser(db, '63ffdb922723cde71590ae36', 5, [])
# result = dbGetUser(db, '63ffdb922723cde71590ae36')

# print('User new: ', result)

# TEST: CREATE Concert
# result = dbCreateConcert(db, {
#     'title': 'Bob\'s Bobby Consert',
#     'artist': 'Bob',
#     'description': '10 out of 10',
#     'date': datetime.datetime.now(),
#     'venue': {}
# })

# print('Concert new: ', result)

# TEST: GET Concerts
# result = dbGetConcerts(db)

# print('Concerts: ', result)

# TEST: GET Consert by id
# result = dbGetConcert(db, id='64013a597a67818bce813233')

# print('Concert: ', result)

# TEST: GET Consert by title
# result = dbGetConcert(db, title='electric boogaloo')

# print('Concert: ', result)

# TEST: Create Venue
# result = dbCreateVenue(db, {
#     'name': 'Massey Hall',
#     'location': '178 Victoria St, Toronto, ON M5B 1T7, Canada',
#     'totalSeats': 1500,
#     'sections': {
#         'floor': 200,
#         'bowl': 1000,
#         'box': 300
#     }
# })

# print('Venue: ', result)

# TEST: Get Venues
# result = dbGetVenues(db)

# print('venues: ', result)

# TEST: Update User
# result = dbUpdateUser(db, {'section': 'floor', 'price': 32, 'concert': 'Sam', 'quantity': 5}, email='agam@testing.ca')

# print('User: ', result)

# TEST: Update Merchant
# result = dbUpdateMerchant(db, {
#     'title': 'Sammy Sam Concert', 
#     'artist': 'Sam', 
#     'description': 'Cool stuff', 
#     'date': datetime.datetime.now(), 
#     'image': '', 
#     'utilization': 0.5, 
#     'price': {
#         'floor': 20,
#         'bowl': 35,
#         'box': 100
#     },
#     'venue': {
#         'name': 'Danforth Music Hall',
#         'location': '147 Danforth Ave, Toronto, ON M4K 1N2, Canada',
#         'totalSeats': 400,
#         'sections': {
#             'floor': 100,
#             'bowl': 250,
#             'box': 50
#         }
#     },
#     }, email='agamMerc@testing.ca')

# print('Update: ', result)

# TEST: Remove Concert
# result = dbRemoveConcert(db, name='Agam Merchant', title='Hello, World!')

# print('Remove: ', result)

# TEST Update Concert
# result = dbUpdateConcert(db, 'ben', {'floor': 1, 'bowl': 1, 'box': 1})

# print('Update', result)