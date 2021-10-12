# Parth Korat
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


# Establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create the index.html route
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


# Create the scrape.html route that starts the scrape function
@app.route("/scrape")
def scrape():
    
    mars_data = scrape_mars.scrape_all()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
