import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import joblib

app = Flask(__name__)

# Load your trained models
generator = load_model(r'C:\Users\91989\PycharmProjects\soil\.venv\soil\models\generator_epoch_5000.h5')
classification_model = load_model(r'C:\Users\91989\PycharmProjects\soil\.venv\soil\models\classification_model.h5')
scaler = joblib.load(r'C:\Users\91989\PycharmProjects\soil\.venv\soil\models\scaler.pkl')

def generate_new_profiles(generator_model, num_profiles, input_dim, scaler):
    random_conditions = np.random.rand(num_profiles, input_dim)
    generated_profiles = generator_model.predict(random_conditions)
    generated_profiles_original_scale = scaler.inverse_transform(generated_profiles)

    column_names = ['pH', 'Soil EC', 'Phosphorus', 'Potassium', 'Urea', 'T.S.P', 'M.O.P', 'Moisture', 'Temperature']
    profiles_df = pd.DataFrame(generated_profiles_original_scale, columns=column_names)
    return profiles_df

def classify_soil(features):
    features_scaled = scaler.transform([features])
    prediction = classification_model.predict(features_scaled)
    return prediction[0]

def evaluate_soil(pH, soil_ec, phosphorus, potassium, urea, tsp, mop, moisture, temperature):
    evaluation = {}
    evaluation['pH'] = 'Good' if 6.0 <= pH <= 7.5 else 'Bad'
    evaluation['Soil EC'] = 'Good' if 0.1 <= soil_ec <= 0.5 else 'Bad'
    evaluation['Phosphorus'] = 'Good' if 10 <= phosphorus <= 40 else 'Bad'
    evaluation['Potassium'] = 'Good' if 120 <= potassium <= 200 else 'Bad'
    evaluation['Urea'] = 'Good' if 20 <= urea <= 50 else 'Bad'
    evaluation['T.S.P'] = 'Good' if 10 <= tsp <= 30 else 'Bad'
    evaluation['M.O.P'] = 'Good' if 20 <= mop <= 60 else 'Bad'
    evaluation['Moisture'] = 'Good' if 60 <= moisture <= 80 else 'Bad'
    evaluation['Temperature'] = 'Good' if 15 <= temperature <= 35 else 'Bad'

    good_count = sum(1 for result in evaluation.values() if result == 'Good')
    bad_count = len(evaluation) - good_count

    if bad_count == 0:
        conclusion = "This soil is ideal for plant growth and meets all recommended criteria."
    elif bad_count <= 2:
        conclusion = "This soil is mostly good, but attention is required for the following parameters: " + \
                     ", ".join([key for key, result in evaluation.items() if result == 'Bad']) + "."
    else:
        conclusion = "This soil has several issues and requires significant improvement, especially for: " + \
                     ", ".join([key for key, result in evaluation.items() if result == 'Bad']) + "."

    return evaluation, conclusion

@app.route('/', methods=['GET', 'POST'])
def index():
    soil_quality = {}
    soil_conclusion = ""
    generated_data = {}
    plant_type_prediction = ""

    if request.method == 'POST':
        try:
            soil_data = {
                "pH": float(request.form.get('pH', '0')) or 0,
                "soil_ec": float(request.form.get('soil_ec', '0')) or 0,
                "phosphorus": float(request.form.get('phosphorus', '0')) or 0,
                "potassium": float(request.form.get('potassium', '0')) or 0,
                "urea": float(request.form.get('urea', '0')) or 0,
                "tsp": float(request.form.get('tsp', '0')) or 0,
                "mop": float(request.form.get('mop', '0')) or 0,
                "moisture": float(request.form.get('moisture', '0')) or 0,
                "temperature": float(request.form.get('temperature', '0')) or 0
            }

            if 'submit' in request.form:
                features = list(soil_data.values())
                plant_type_prediction = classify_soil(features)
                soil_quality, soil_conclusion = evaluate_soil(**soil_data)

            if 'generate' in request.form:
                num_profiles_to_generate = 1
                input_dim = 8
                new_profiles_df = generate_new_profiles(generator, num_profiles_to_generate, input_dim, scaler)
                generated_data = new_profiles_df.iloc[0].to_dict()

        except ValueError:
            soil_conclusion = "Please make sure all inputs are valid numbers."

    return render_template('index.html', soil_quality=soil_quality, soil_conclusion=soil_conclusion,
                           generated_data=generated_data, plant_type_prediction=plant_type_prediction)

if __name__ == '__main__':
    app.run(debug=True)
