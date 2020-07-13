from flask import Flask, render_template, request, redirect
from flask import jsonify, make_response
import ASUCourseScraper as scraper
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')
#Routes-------------------
#Main page redirects to portfolio
@app.route('/')
def start():
    return render_template("index.html")

@app.route('/backgroundRMPASU')
def queryRMP():
    inputURL = request.args.get('url')
    data = scraper.GetRMPData(inputURL)
    print("Data: ")
    print(data)
    return jsonify(str(data))

app.run(debug=True)
