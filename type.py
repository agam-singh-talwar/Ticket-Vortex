from typing import TypedDict
import datetime

User = TypedDict('User', {
    'fullname': str,
    'password': str,
    'email': str,
    'isBulkBuyer': bool,
    'balance': float,
    'tickets': 'list[Ticket]'
})

Sections = TypedDict('Sections', {
    'floor': float,
    'bowl': float,
    'box': float,
})

Venue = TypedDict('Venue', {
    'name': str,
    'location': str,
    'totalSeats': int, # overall number of seats
    'sections': Sections # max number of seats in each section
})

Concert = TypedDict('Concert', {
    'title': str,
    'artist': str,
    'description': str,
    'date': datetime.datetime,
    'image': str,
    'utilization': float, # must be between 0.5 and 1
    'price': Sections, # price per seat in each section
    'venue': Venue
})

Merchant = TypedDict('Merchant', {
    'email': str,
    'password': str,
    'name' : str,
    'concerts': 'list[Concert]'
})

Ticket = TypedDict('Ticket', {
    'quantity': int,
    'section': str, # can be one of floor, bowl, or box
    'price': float,
    'concert': str,
})
