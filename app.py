from flask import Flask, render_template, request
import pandas as pd
import pickle

model = pickle.load(open("rain_XGBnew_model.pkl", "rb"))
app = Flask(__name__, template_folder="template")

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == "POST":
        date = request.form['date']
        day = pd.to_datetime(date).day
        month = pd.to_datetime(date).month

        # Read inputs as floats
        minTemp = float(request.form['mintemp'])
        maxTemp = float(request.form['maxtemp'])
        rainfall = float(request.form['rainfall'])
        evaporation = float(request.form['evaporation'])
        sunshine = float(request.form['sunshine'])
        windGustSpeed = float(request.form['windgustspeed'])
        windSpeed9am = float(request.form['windspeed9am'])
        windSpeed3pm = float(request.form['windspeed3pm'])
        humidity9am = float(request.form['humidity9am'])
        humidity3pm = float(request.form['humidity3pm'])
        pressure9am = float(request.form['pressure9am'])
        pressure3pm = float(request.form['pressure3pm'])
        temp9am = float(request.form['temp9am'])
        temp3pm = float(request.form['temp3pm'])
        cloud9am = float(request.form['cloud9am'])
        cloud3pm = float(request.form['cloud3pm'])

        # Categorical encodings
        location = request.form['location']
        location_map = {
            'Portland': 1, 'Cairns': 2, 'Walpole': 3, 'Dartmoor': 4,
            'MountGambier': 5, 'NorfolkIsland': 6, 'Albany': 7, 'Witchcliffe': 8,
            'CoffsHarbour': 9, 'Sydney': 10, 'Darwin': 11, 'MountGinini': 12,
            'NorahHead': 13, 'Ballarat': 14, 'GoldCoast': 15, 'SydneyAirport': 16
        }
        location = location_map.get(location, 0)

        winddDir9am = request.form['winddir9am']
        winddDir3pm = request.form['winddir3pm']
        windGustDir = request.form['windgustdir']
        wind_dir_map = {'NMW': 0, 'NW': 1, 'WNW': 2, 'N': 3, 'NNW': 4}
        winddDir9am = wind_dir_map.get(winddDir9am, 0)
        winddDir3pm = wind_dir_map.get(winddDir3pm, 0)
        windGustDir = wind_dir_map.get(windGustDir, 0)

        rainToday = request.form['raintoday']
        rainToday = 1 if rainToday == 'Yes' else 0

        input_lst = [[
            location, minTemp, maxTemp, rainfall, evaporation, sunshine,
            windGustDir, windGustSpeed, winddDir9am, winddDir3pm, windSpeed9am,
            windSpeed3pm, humidity9am, humidity3pm, pressure9am, pressure3pm,
            cloud9am, cloud3pm, temp9am, temp3pm, rainToday, month, day
        ]]

        pred = model.predict(input_lst)[0]
        if pred == 0:
            return render_template("after_sunny.html")
        else:
            return render_template("after_rainy.html")

if __name__ == '__main__':
    app.run(debug=True)
