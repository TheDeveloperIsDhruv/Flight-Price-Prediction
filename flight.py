from flask import Flask,render_template, request, redirect, url_for
import joblib
import sklearn
print(sklearn.__version__)
app=Flask(__name__)


model = joblib.load('model.joblib')
print("Model is loaded!")

@app.route("/")
def welcome():
    return "Hello World"

lst=[]
@app.route('/main',methods=['POST','GET'])
def homepage():
    if (request.method == "GET"):
        return render_template("main.html")
    else:
        departed_date = request.form.get('Ddate')
        arrival_date = request.form.get('Adate')
        source = request.form.get('source')
        destination = request.form.get('dest')
        stops=request.form.get('stop')
        airline=request.form.get('airline')

        # Print received values to the console
        print(f"Departed date: {departed_date}")
        print(f"Arrival date: {arrival_date}")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        print(f"Number of stops: {stops}")
        print(f"Airline: {airline}")
        message='Submitted!'
        return render_template("main.html",msg=message)
    

if __name__=="__main__":
    app.run(debug=True)
