from flask import Flask, request, jsonify
from service import *

 
app = Flask(__name__)
data = []

def serialize(book):
    return {
        "id" : book.id,
        "title": book.title,
        "author": book.author,
        "date": book.date,
        "last_update": book.last_update
    }
@app.route('/v1/item/<int:item_id>', methods=['GET'])
def item(item_id):
    canceled_items = get_canceled_item_list() # [serialize(book)for book in get_canceled_item_list()]
    print(type(canceled_items['count'].iloc[0]))
    return str(canceled_items['count'].iloc[0])
    
if __name__ == '__main__':
    app.run(debug=True)
