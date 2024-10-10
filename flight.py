import pandas as pd
from flask import Flask, render_template, request
import joblib
from datetime import datetime

app = Flask(__name__)
model = joblib.load('model.joblib')
print("Model is loaded!")

@app.route("/")
def welcome():
    return "Hello World"

@app.route('/main', methods=['POST', 'GET'])
def homepage():
    if request.method == "GET":
        return render_template("main.html")
    else:
        departed_date = request.form.get('Ddate')
        departed_dt = datetime.fromisoformat(departed_date)
        
        det_hour = departed_dt.hour
        det_minutes = departed_dt.minute
        arrival_time = request.form.get('Atime')
        arrival_dt = datetime.fromisoformat(arrival_time)
        arr_hour = arrival_dt.hour
        arr_minutes = arrival_dt.minute
        
        source = request.form.get('source')
        destination = request.form.get('dest')
        stops = int(request.form.get('stop'))  # Ensure this is an integer
        airline = request.form.get('airline')
        
        # Encode sources
        Source_Delhi = 1 if source == "Delhi" else 0
        Source_Chennai = 1 if source == "Chennai" else 0
        Source_Kolkata = 1 if source == "Kolkata" else 0
        Source_Mumbai = 1 if source == "Mumbai" else 0
        
        # Encode destinations
        Destination_Cochin = 1 if destination == "Cochin" else 0
        Destination_Delhi = 1 if destination == "Delhi" else 0
        Destination_Hyderabad = 1 if destination == "Hyderabad" else 0
        Destination_Kolkata = 1 if destination == "Kolkata" else 0
        Destination_New_Delhi = 1 if destination == "New Delhi" else 0
        
        # Encode airlines
        Airline_Air_India = 1 if airline == "Air India" else 0
        Airline_GoAir = 1 if airline == "Go Air" else 0
        Airline_IndiGo = 1 if airline == "IndiGO" else 0
        Airline_Jet_Airways = 1 if airline == "Jet Airways" else 0
        Airline_Jet_Airways_Business = 1 if airline == "Jet Airways Business" else 0
        Airline_Multiple_carriers = 1 if airline == "Multiple Carriers" else 0
        Airline_Multiple_carriers_Premium_economy = 1 if airline == "Premium Economy" else 0
        Airline_SpiceJet = 1 if airline == "SpiceJet" else 0
        Airline_Trujet = 1 if airline == "TrueJet" else 0
        Airline_Vistara = 1 if airline == "Vistara" else 0
        Airline_Vistara_PE = 1 if airline == "Vistara Premium Economy" else 0
        
        expected_features = [
        'Total_Stops', 'Journey_Day', 'Journey_Month', 'Journey_Year',
        'Dep_hours', 'Dep_Minutes', 'Duration_hours', 'Duration_minutes',
        'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
        'Airline_Jet Airways', 'Airline_Jet Airways Business',
        'Airline_Multiple carriers', 'Airline_Multiple carriers Premium economy',
        'Airline_SpiceJet', 'Airline_Trujet', 'Airline_Vistara',
        'Airline_Vistara Premium economy', 'Source_Chennai', 'Source_Delhi',
        'Source_Kolkata', 'Source_Mumbai', 'Destination_Cochin',
        'Destination_Delhi', 'Destination_Hyderabad',
        'Destination_Kolkata', 'Destination_New Delhi'
        ]

        input_data = {
            'Total_Stops': stops,
            'Journey_Day': departed_dt.day,
            'Journey_Month': departed_dt.month,
            'Journey_Year': departed_dt.year,
            'Dep_hours': det_hour,
            'Dep_Minutes': det_minutes,
            'Duration_hours': arr_hour - det_hour,
            'Duration_minutes': arr_minutes - det_minutes,
            'Airline_Air India': Airline_Air_India,
            'Airline_GoAir': Airline_GoAir,
            'Airline_IndiGo': Airline_IndiGo,
            'Airline_Jet Airways': Airline_Jet_Airways,
            'Airline_Jet Airways Business': Airline_Jet_Airways_Business,
            'Airline_Multiple carriers': Airline_Multiple_carriers,
            'Airline_Multiple carriers Premium economy': Airline_Multiple_carriers_Premium_economy,
            'Airline_SpiceJet': Airline_SpiceJet,
            'Airline_Trujet': Airline_Trujet,
            'Airline_Vistara': Airline_Vistara,
            'Airline_Vistara Premium economy': Airline_Vistara_PE,
            'Source_Chennai': Source_Chennai,
            'Source_Delhi': Source_Delhi,
            'Source_Kolkata': Source_Kolkata,
            'Source_Mumbai': Source_Mumbai,
            'Destination_Cochin': Destination_Cochin,
            'Destination_Delhi': Destination_Delhi,
            'Destination_Hyderabad': Destination_Hyderabad,
            'Destination_Kolkata': Destination_Kolkata,
            'Destination_New Delhi': Destination_New_Delhi
        }

        input_df = pd.DataFrame([input_data], columns=expected_features).fillna(0)
        predicted_price = model.predict(input_df)

        message = f'Best Price is: Rs.{predicted_price[0]:.2f}'  # Format output
        
        return render_template("main.html", msg=message)

if __name__ == "__main__":
    app.run(debug=True)
