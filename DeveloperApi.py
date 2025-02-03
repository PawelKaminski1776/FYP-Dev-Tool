from flask import Flask, jsonify, request
from WebScraper import WebScraper
import asyncio

# Create an instance of the Flask class
app = Flask(__name__)

# Sample data to serve
data = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

# Home route
@app.route('/Webscraper', methods=['POST'])
def WebscraperAPI():
    new_item = request.get_json()
    data.append(new_item)
    print(new_item)
    asyncio.run(WebScraper.WebScraper(new_item.get('NumOfImages'), new_item.get('County')))
    return jsonify(new_item), 201

# Get all items
@app.route('/TrainImages', methods=['POST'])
def get_items():

    return jsonify(data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)