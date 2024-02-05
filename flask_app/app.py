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
    item = get_canceled_item_list(item_id) # [serialize(book)for book in get_canceled_item_list()]
    return jsonify(item)
    
if __name__ == '__main__':
    app.run(debug=True)
