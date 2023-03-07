import os
import base64
from db import *
from form import *
from type import *
from image import *
from dotenv import load_dotenv
from flask_session import Session
from flask import Flask, render_template, redirect, url_for, request, flash, session
from random import randint
import math

load_dotenv()

# define the mongo url and the key for db
MONGO_URI = os.getenv('MONGO_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# Project configuration
app = Flask(__name__)

# define config values for the key and file sesssion to be used
# then continue to initializing the database 
# from mongo connection string
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
db = dbInitialize(app, MONGO_URI)
Session(app)

@app.context_processor
def inject_session():
    # returns a session
    return dict(session=session)

@app.route("/")#Home route
@app.route("/home")
def home_page():
    return render_template("/home.html")


@app.route("/market", methods=['GET'])#Route to get market page
def market_page():
    items = dbGetConcerts(db)
    # loop through items and render each item in the concerts collection
    for item in items:
        print(item['title'])
    return render_template("market.html", items=items, FinalUser=session.get('user'))# Sends user and all concert to mhtl template

@app.route("/merchant",methods=["GET","POST"])#Merchant market
def merchant_market():
    return render_template("/MerchantMarket.html",user=session.get("user"))#sends user to template

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()#creates form

    # validate success when user submits info for individual/bulk registration
    if form.validate_on_submit():
        d = {#stores form data
            'name':form.Name.data,
            'password': form.Pass1.data,
            'email': form.Email.data,
            'isBulkBuyer': form.Bulk.data,
            'tickets' : []
        }
        usr = dbGetUser(db, email=form.Email.data)#Checks if user already excists
        
        # display error message if user has existing email in the system 
        # (usr results to true)
        if usr:
            flash('Email already used! Please try again.', category='danger')
            return render_template("/register.html", form=form)
        
        session['user']= usr#creates session for user
        dbCreateUser(db, d)#stores user to database
        flash(f'Account created. Pls login to feel the wrath fo the Vortex 🌪️.',category='success')
        return redirect(url_for("market_page"))
    
    # Error Handling
    # Display an error if there are any problems occuring in the 
    # individual / bulk buyer registration process
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'There was an error while registering a user: {msg}', category='danger')

    return render_template("/register.html", form=form)

@app.route("/merchant/register", methods=["GET", "POST"])
def merchantRegisterPage():
    form = RegisterForm()#creates form
    
    # validate success when user submits info for merchant registration
    if form.validate_on_submit():
        d = {#stores form data
            'name':form.Name.data,
            'password': form.Pass1.data,
            'email': form.Email.data,
            'concerts' : []
        }
        usr = dbGetMerchant(db, email=form.Email.data)#checks if merchant is in database
        # display error message if user has existing email in the system 
        # (usr results to true)
        if usr:
            flash('Email already used! Please try again.', category='danger')
            return render_template("/merchantRegister.html", form=form)
        
        session['user']= usr#create sessions and stores to database
        dbCreateMerchant(db, d)

        return redirect(url_for("market_page"))
    # Error Handling
    # Display an error if there are any problems occuring in the 
    # merchant registration process
    if form.errors != {}:
        for msg in form.errors.values():
            flash(
                f'There was an error while registering a user: {msg}', category='danger')

    return render_template("/merchantRegister.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():

    form = LoginForm()
    if form.validate_on_submit():
        d = {'password': form.Pass.data,
                'email': form.Email.data}
        usr={}
        usr = dbUserLogin(db, user=d)
        # verify user input info is correct
        # proceed to log in the user
        # redirect to the market page with congrats messages
        if usr: 
            session["user"]= usr
            session['cart'] = []
            flash(f"Hi { usr.get('name')}, how are you doing today!", category="success")
            return redirect(url_for("market_page"))
        else:
            # error handle for if user inputs any wrong info
            flash(f'Wrong Password or Username', category='danger')
    return render_template("/login.html", form=form)


@app.route("/merchant/login", methods=["GET", "POST"])
def merchantLogin_page():
    form = LoginForm()
    if form.validate_on_submit():
        d = {'password': form.Pass.data,
                'email': form.Email.data}
        merchant={}
        merchant = dbMerchantLogin(db, merchant=d)
        # verify merchant info is correct
        # proceed to log in the merchant
        # redirect to the market page with congrats messages
        if merchant: 
            session["user"]= merchant
            session["merchant"] = True
            flash(f"Hi { merchant.get('name')}, how are you doing today!", category="success")
            return render_template('/MerchantMarket.html',user=session.get("user"))
        else:
            # error handle for if user inputs any wrong info
            flash(f'Wrong Password or Username', category='danger')
    return render_template("/merchantLogin.html", form=form)

@app.route("/logout")
def logout_page():
    # create goodbye message for when user logs out
    if 'user' in session:
        session.clear()
        if 'merchant' in session:
            session.clear()
        flash(f'Thanks for using our services!',category='info')
        return render_template("/home.html")
    else:
        return render_template("/LoginError.html")


@app.route("/purchase/<string:title>",methods=["GET","POST"])
def purchase_page(title):
    if 'user' in session:
        # display the concert for ticket purchase by title value
        concert = dbGetConcert(db, title=title)
        if request.method == 'POST':
            price = 0
            match request.form['section']:
                case 'floor':
                    price = int(request.form['floorPrice']) * int(request.form['amount'])
                case 'bowl':
                    price = request.form['bowlPrice'] * request.form['amount']
                case 'box':
                    price = request.form['boxPrice'] * request.form['amount']
            session['cart'].append({'quantity': request.form['amount'],
            'section': request.form['section'], # can be one of floor, bowl, or box
            'price': price,
            'concert': request.form['concert'],})
        return render_template("/purchase.html", concert = concert, user=session.get('user'))
    else:
        return render_template("/LoginError.html")


def idGen(id):
    # generate random id between 1 and 9999 for use
    for i in range(len(session['cart'])):
            if session['cart'][i]['num'] == id:
                id = randint(1,9999)
                idGen(id)
    return id

# use function to add any tickets to cart until user desires to purchase
@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    # deny access to any merchants trying to buy tickets
    # redirect merchants back to the market
    if 'merchant' in session:
        flash(f'Merchants cant buy tickets', category='danger')
        return(redirect("/market"))
    price = 0
    totTickets = 0
    match request.form['section']:
        case 'floor':
            price = float(request.form['floorPrice']) * int(request.form['amount'])
            totTickets = int(request.form['floorTickets']) * float(request.form['util'])
        case 'bowl':
            price = float(request.form['bowlPrice']) * int(request.form['amount'])
            totTickets = int(request.form['bowlTickets']) * float(request.form['util'])
        case 'box':
            price = float(request.form['boxPrice']) * int(request.form['amount'])
            totTickets = int(request.form['boxTickets']) * float(request.form['util'])

    # display message if tickets wanted are not available for purchase
    if int(request.form['amount']) > int(totTickets):
        flash(f'Not enough tickets available', category='danger')
        return(redirect("/purchase/" + request.form['concert']))
    
    id = idGen(randint(1, 9999))
    session['cart'].append({'num' : id, 'quantity': request.form['amount'],
    'section': request.form['section'], # can be one of floor, bowl, or box
    'price': price,
    'concert': request.form['concert'],})
    return(redirect("/market"))


# create solution for user to decide they want to continue to payment
# and finalize sale of cart items
@app.route("/buyNow", methods=['GET', 'POST'])
def buyNow():
    if 'merchant' in session:
        flash(f'Merchants cant buy tickets', category='danger')
        return(redirect("/market"))
    if request.method == 'POST':
        price = 0
        totTickets = 0
        match request.form['section']:
            case 'floor':
                price = float(request.form['floorPrice']) * int(request.form['amount'])
                totTickets = int(request.form['floorTickets']) * float(request.form['util'])
            case 'bowl':
                price = float(request.form['bowlPrice']) * int(request.form['amount'])
                totTickets = int(request.form['bowlTickets']) * float(request.form['util'])
            case 'box':
                price = float(request.form['boxPrice']) * int(request.form['amount'])
                totTickets = int(request.form['boxTickets']) * float(request.form['util'])

        # display message if tickets wanted are not available for purchase
        if int(request.form['amount']) > int(totTickets):
            flash(f'Not enough tickets available', category='danger')
            return(redirect("/purchase/" + request.form['concert']))
        id = idGen(randint(1, 9999))
        

        session['cart'].append({'num' : id, 'quantity': request.form['amount'],
        'section': request.form['section'], # can be one of floor, bowl, or box
        'price': price,
        'concert': request.form['concert'],})
    # need to pass hte form in the html file
    return(render_template("payment.html"))

def genId(id):
    for userTicket in session['user']['tickets']:
        if userTicket['num'] == id:
            genId(randint(1,9999))
    return id

@app.route("/tickets", methods=['GET'])
def tickets():
    if 'merchant' not in session and 'user' in session:
        return render_template('userTickets.html', user = session.get('user'))


# implement the use of entering payment 
# details for ticket purchasing
@app.route("/payment", methods=['POST',"GET"])
def buyTickets():
    for ticket in session['cart']:
        concert = dbGetConcert(db, title=ticket['concert'])
        if concert['venue']['sections'][ticket['section']] - int(ticket['quantity']) < 0:
            flash(f'Not enough tickets available for ' + ticket['concert'], category='danger')
            return(render_template("payment.html"))

    for ticket in session['cart']:
        ticket['num'] = genId(ticket['num'])
        dbUpdateUser(db, ticket, session['user']['_id'])
        dbUpdateConcert(db, ticket['concert'], ticket['section'], int(ticket['quantity']))
        session['user'] = dbGetUser(db, session['user']['_id'])
        session['cart'] = []
    return(redirect("/tickets"))
    #fake payment process

# for each item in the cart if something is removed by use of id, 
# remove and redirect back to market
@app.route("/removeFromCart/<int:id>", methods=['GET'])
def removeCart(id):
    
    for i in range(len(session['cart'])):
        if(session['cart'][i].get('num') == id):
            del session['cart'][i]
            break
    return(redirect("/market"))

@app.route("/removeFromCart/", methods=['GET'])
def removeCartOld():
    
    for i in range(len(session['cart'])):
        if(session['cart'][i].get('cartNum')):
            del session['cart'][i]
            break
    return(redirect("/market"))

# display section for allowing use of merchant to add a concert info
@app.route('/merchant/add', methods=['POST', 'GET'])
def concert_page():
    if 'merchant' in session:
        venues = dbGetVenues(db)
        form = ConcertForm()

        # find selected venue for concert 
        venue = None
        for v in venues:
            if v['id'] == ObjectId(form.venue.data):
                venue = v
                break

        if form.validate_on_submit():
            venue['totalSeats'] = math.ceil(venue['totalSeats'] * (float(form.utilization.data) / 100))
            venue['sections']['floor'] = math.ceil(venue['sections']['floor'] * (float(form.utilization.data) / 100))
            venue['sections']['bowl'] = math.ceil(venue['sections']['bowl'] * (float(form.utilization.data) / 100))
            venue['sections']['box'] = math.ceil(venue['sections']['box'] * (float(form.utilization.data) / 100))
            result = dbUpdateMerchant(db, {
                'title': form.title.data,
                'artist': form.artist.data,
                'description': form.description.data,
                'date': datetime.datetime.combine(form.date.data, form.time.data),
                'image': encode(form.image),
                'utilization': float(form.utilization.data),
                'price': {
                    'floor': float(form.floorPrice.data),
                    'bowl': float(form.bowlPrice.data),
                    'box': float(form.boxPrice.data) 
                },
                'venue': venue
            }, session['user']['_id'])

            if result == False:
                flash('Please try again, concert could not be created', 'error')
                return redirect('/merchant/concert')

            session['user'] = dbGetMerchant(db, email=session['user']['email'])
            return render_template('MerchantMarket.html', user = session.get('user'))
        else:
            flash(form.errors)

        return render_template('concert.html', form=form, venues=venues)
    else:
        return render_template('LoginError.html')

@app.route("/remove_item", methods=['POST'])
def remove_item(ticket):
    if 'user' in session:
        session['user'].tickets.remove(ticket)

# allow merchant to remove a concert they have added
@app.route("/merchant/remove/<string:title>", methods=['POST',"GET","DELETE"])
def merchant_remove_concert(title):
        c=session.get("user").get('concerts')
        if dbRemoveConcert(db,name=session.get("user").get('name') ,title=title):
            for conc in  c:
                if title == conc.get('title'):
                    session.get("user").get('concerts').remove(conc)
            return render_template("/MerchantMarket.html",user=session.get("user"))

# allow a merchant to edit a concert they have added
@app.route("/merchant/edit/<string:title>",methods=["GET","POST"])
def merchant_edit_concert(title):
    if 'merchant' not in session:
        return redirect('/')
    
    form = ConcertForm()
    venues = dbGetVenues(db)
    concert = dbGetConcert(db, title=title)
    
    # find selected venue for concert 
    venue = None
    for v in venues:
        if v['id'] == ObjectId(concert['venue']['id']):
            venue = v
            break

    id = str(venue['id'])

    if request.method == 'GET':
        # fill form with existing data
        form.title.data = concert['title']
        form.artist.data = concert['artist']
        form.preview = concert['image']
        form.description.data = concert['description']
        form.date.data = concert['date'].date()
        form.time.data = concert['date'].time()
        form.utilization.data = concert['utilization']
        form.floorPrice.data = concert['price']['floor']
        form.bowlPrice.data = concert['price']['bowl']
        form.boxPrice.data = concert['price']['box']
        form.submit.label.text = 'Confirm edit'
        form.venue.data = id

    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'artist': form.artist.data,
            'description': form.description.data,
            'date': datetime.datetime.combine(form.date.data, form.time.data),
            'image': encode(form.image),
            'utilization': float(form.utilization.data),
            'price': {
                'floor': float(form.floorPrice.data),
                'bowl': float(form.bowlPrice.data),
                'box': float(form.boxPrice.data) 
            },
            'venue': venue
        }
        dbReplaceConcert(db, title, data)
        session['user'] = dbGetMerchant(db, email=session.get('user')['email'])

        flash(f'Concert edited!!',category="success")
        
        return render_template('MerchantMarket.html', user = session.get('user'))

    return render_template('concert.html', form=form, venues=venues)

# checks for main. runs app with debug on port specified (5050)
if __name__ == '__main__':
    app.run(debug=True, port=5050)