from flask_pymongo import PyMongo, ObjectId
from type import *


def dbInitialize(app, uri) -> 'None | any':
    try:
        app.config['MONGO_URI'] = uri
        mongo = PyMongo(app)

        return mongo.db
    except:
        return None


def dbMerchantLogin(db, merchant: Merchant) -> 'list[Merchant]':
    if db.merchants.find_one({'email': merchant['email']}) and db.merchants.find_one({'email': merchant['email']})['password'] == merchant['password']:
        return db.merchants.find_one({'email': merchant['email']})
    return None


def dbUserLogin(db, user: User) -> 'list[User]':
    if db.users.find_one({'email': user['email']}) and db.users.find_one({'email': user['email']})['password'] == user['password']:
        return db.users.find_one({'email': user['email']})
    return None


def dbCreateUser(db, user: User) -> bool:
    try:
        result = db.users.insert_one(user)

        return result.acknowledged
    except:
        return False


def dbGetUsers(db) -> 'list[User]':
    try:
        users = db.users.find()

        result = [{
            'id': user['_id'],
            'username': user['username'],
            'password': user['password'],
            'email': user['email'],
            'isBulkBuyer': user['isBulkBuyer'],
            'balance': user['balance'],
            'tickets': user['tickets']
        } for user in users]

        return result
    except:
        return []


def dbGetUser(db, id: str = None, email: str = None) -> 'User | None':
    if id != None and email == None:
        return db.users.find_one({'_id': ObjectId(id)})
    elif id == None and email != None:
        return db.users.find_one({'email': email})
    else:
        return None


def dbUpdateUser(db, ticket, id: str = None, email: str = None) -> bool:
    try:
        if id != None and email == None:
            result = db.users.update_one(
                {'_id': ObjectId(id)},
                {'$push': {
                    'tickets': ticket
                }}
            )
            return result.acknowledged
        elif id == None and email != None:
            result = db.users.update_one(
                {'email': email},
                {'$push': {
                    'tickets': ticket
                }}
            )
            return result.acknowledged
        else:
            return []
    except:
        return []


def dbCreateMerchant(db, merchant: Merchant) -> bool:
    try:
        result = db.merchants.insert_one(merchant)

        return result.acknowledged
    except:
        return False


def dbGetMerchants(db) -> 'list[Merchant]':
    try:
        merchants = db.merchants.find()
        result = [{
            'id': merchant['_id'],
            'username': merchant['username'],
            'password': merchant['password'],
            'email': merchant['email'],
            'concerts': merchant['concerts']
        } for merchant in merchants]

        return result
    except:
        return []


def dbGetMerchant(db, id: str = None, email: str = None) -> 'Merchant | None':
    if id != None and email == None:
        return db.merchants.find_one({'_id': ObjectId(id)})
    elif id == None and email != None:
        return db.merchants.find_one({'email': email})
    else:
        return None


def dbUpdateMerchant(db, consert: Concert, id: str = None, email: str = None) -> bool:
    try:
        if id != None and email == None:
            result = db.merchants.update_one(
                {'_id': ObjectId(id)},
                {'$push': {
                    'concerts': consert
                }}
            )
            return result.acknowledged
        elif id == None and email != None:
            result = db.merchants.update_one(
                {'email': email},
                {'$push': {
                    'concerts': consert
                }}
            )
            return result.acknowledged
        else:
            return False
    except:
        return []


def dbCreateConcert(db, concert: Concert) -> bool:
    try:
        result = db.concerts.insert_one(concert)

        return result.acknowledged
    except:
        return False


def dbGetConcerts(db) -> 'list[Concert]':
    try:
        results = db.merchants.aggregate([
            {'$match': {
                'concerts': {
                    '$exists': True
                }    
            }},
            {'$unwind': '$concerts'},
            {'$project': {
                'title': '$concerts.title',
                'artist': '$concerts.artist',
                'description': '$concerts.description',
                'date': '$concerts.date',
                'image': '$concerts.image',
                'utilization': '$concerts.utilization',
                'price': '$concerts.price',
                'venue': '$concerts.venue'
            }}
        ])
        collection = []
        for document in results:
            collection.append(document)

        return collection
    except:
        return []


def dbGetConcert(db, id: str = None, title: str = None) -> 'Concert | None':
    conserts = dbGetConcerts(db)
    for consert in conserts:
        if id != None and title == None:
            if consert['_id'] == id:
                return consert
        elif id == None and title != None:
            if consert['title'] == title:
                return consert
        else:
            return None


# title is a required parameter
def dbRemoveConcert(db, id: str = None, name: str = None, title: str = None) -> bool:
    try:
        if id != None and name == None:
            result = db.merchants.update_one(
                {'_id': ObjectId(id)},
                {'$pull': {
                    'concerts': {
                        'title': title
                    }
                }}
            )
            db.concerts.delete_one({ 'title' : title })
            return result.acknowledged
        elif id == None and name != None:
            result = db.merchants.update_one(
                {'name': name},
                {'$pull': {
                    'concerts': {
                        'title': title
                    }
                }}
            )
            db.concerts.delete_one({ 'title' : title })
            return result.acknowledged
        else:
            return False
    except:
        return False
    
# values are interpreted as negative by default
def dbUpdateConcert(db, title: str, section : str, qty : int):
    try:
        match section:
            case 'floor':
                result = db.merchants.update_one(
                    {'concerts.title': title},
                        {'$inc': {
                            'concerts.$.venue.totalSeats': -qty,
                            'concerts.$.venue.sections.floor': -qty,
                        }
                    }
                )
            case 'bowl':
                result = db.merchants.update_one(
                    {'concerts.title': title},
                        {'$inc': {
                            'concerts.$.venue.totalSeats': -qty,
                            'concerts.$.venue.sections.bowl': -qty,
                        }
                        }
                )
            case 'box':
                result = db.merchants.update_one(
                    {'concerts.title': title},
                        {'$inc': {
                            'concerts.$.venue.totalSeats': -qty,
                            'concerts.$.venue.sections.box': -qty,
                        }
                        }
                )

        return result.acknowledged
    except:
        return False

def dbReplaceConcert(db, title: str, concert: Concert):
    try:
        result = db.merchants.update_one(
            {'concerts.title': title},
            {'$set': {
                'concerts.$.title': concert['title'],
                'concerts.$.artist': concert['artist'],
                'concerts.$.description': concert['description'],
                'concerts.$.date': concert['date'],
                'concerts.$.image': concert['image'],
                'concerts.$.utilization': concert['utilization'],
                'concerts.$.price': concert['price'],
                'concerts.$.venue': concert['venue']
            }}
        )

        return result.acknowledged
    except:
        return False

# Developer use only
def dbCreateVenue(db, venue: Venue) -> bool:
    try:
        result = db.venues.insert_one(venue)

        return result.acknowledged
    except:
        return False


def dbGetVenues(db) -> 'list[Venue]':
    try:
        venues = db.venues.find()
        result = [{
            'id': venue['_id'],
            'name': venue['name'],
            'location': venue['location'],
            'totalSeats': venue['totalSeats'],
            'sections': venue['sections']
        } for venue in venues]

        return result
    except:
        return []


def dbGetVenue(db, id: str = None, name: str = None) -> Venue:
    if id != None and name == None:
        return db.venues.find_one({'_id': ObjectId(id)})
    elif id == None and name != None:
        return db.venues.find_one({'name': name})
    else:
        return None

