from flask import Flask, jsonify, request
from WebScraper import WebScraper
from Image_Training import Semi_Automatic_Training as ST
import asyncio

# Create an instance of the Flask class
app = Flask(__name__)

# Webscraper Route
@app.route('/Webscraper', methods=['POST'])
def WebscraperAPI():
    WebScraperMessage = request.get_json()
    asyncio.run(WebScraper.WebScraper(WebScraperMessage.get('NumOfImages'), WebScraperMessage.get('County')))
    return jsonify(WebScraperMessage), 201

# Semi-Automatic Training Route
@app.route('/TrainImages', methods=['POST'])
def SemiAutoTrainingAPI():
    new_item = request.get_json()
    asyncio.run(ST.StartSemiAutoTraining())

# Run the application
if __name__ == '__main__':
    app.run(debug=True)