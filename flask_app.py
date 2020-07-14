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

@app.route('/quickreturn')
def linkdata():
    inputURL = request.args.get('url')
    #https://webapp4.asu.edu/catalog/classlist?t=2207&s=CSE&n=110&hon=F&promod=F&e=open&page=1
    returnInfo = {}
    returnInfo['department'] = inputURL[(inputURL.find('&s=')+3):(inputURL.find('&s=')+6)]
    returnInfo['courseNumber'] = inputURL[(inputURL.find('&n=')+3):(inputURL.find('&n=')+6)]
    return jsonify(str(returnInfo))

@app.route('/backgroundRMPASU')
def queryRMP():
    inputURL = request.args.get('url')
    data = scraper.GetRMPData(inputURL)
    print("Data: ")
    print(data)
    return jsonify(str(data))

if __name__ == '__main__':
    app.run(debug=True)
