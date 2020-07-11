from flask import Flask, render_template, request, redirect
from flask import jsonify
import ASUCourseScraper.py as scraper
import sys

app = Flask(__name__)

#Routes-------------------
#Main page redirects to portfolio
@app.route('/')
def start():
    return render_template("index.html")

@app.route('/backgroundRMPASU')
def queryRMP():
    inputURL = request.args.get('url')
    scraper.GetRMPData(inputURL)
app.run(debug=True)
