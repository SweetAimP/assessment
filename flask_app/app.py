from flask import Flask, request, jsonify
from service import *

 
app = Flask(__name__)
data = []

@app.route('/v1/item/<license_plate>', methods=['GET'])
def item(license_plate):
    print("Controler")
    item = get_canceled_item_list(license_plate) # [serialize(book)for book in get_canceled_item_list()]
    return jsonify(item)
    
if __name__ == '__main__':
    app.run(debug=True)
