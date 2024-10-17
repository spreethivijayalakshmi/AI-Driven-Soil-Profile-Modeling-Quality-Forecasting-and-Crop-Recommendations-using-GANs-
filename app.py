def evaluate_soil(pH, soil_ec, phosphorus, potassium, urea, tsp, mop, moisture, temperature):
    # Dictionary to store evaluation results
    evaluation = {}

    # Evaluate pH (6.0 - 7.5 is ideal)
    if 6.0 <= pH <= 7.5:
        evaluation['pH'] = 'Good'
    else:
        evaluation['pH'] = 'Bad'

    # Evaluate Soil EC (0.1 - 0.5 dS/m is ideal)
    if 0.1 <= soil_ec <= 0.5:
        evaluation['Soil EC'] = 'Good'
    else:
        evaluation['Soil EC'] = 'Bad'

    # Evaluate Phosphorus (10 - 40 mg/kg is ideal)
    if 10 <= phosphorus <= 40:
        evaluation['Phosphorus'] = 'Good'
    else:
        evaluation['Phosphorus'] = 'Bad'

    # Evaluate Potassium (120 - 200 mg/kg is ideal)
    if 120 <= potassium <= 200:
        evaluation['Potassium'] = 'Good'
    else:
        evaluation['Potassium'] = 'Bad'

    # Evaluate Urea (20 - 50 mg/kg is typical)
    if 20 <= urea <= 50:
        evaluation['Urea'] = 'Good'
    else:
        evaluation['Urea'] = 'Bad'

    # Evaluate T.S.P (10 - 30 mg/kg is ideal)
    if 10 <= tsp <= 30:
        evaluation['T.S.P'] = 'Good'
    else:
        evaluation['T.S.P'] = 'Bad'

    # Evaluate M.O.P (20 - 60 mg/kg is typical)
    if 20 <= mop <= 60:
        evaluation['M.O.P'] = 'Good'
    else:
        evaluation['M.O.P'] = 'Bad'

    # Evaluate Moisture (60% - 80% is ideal for most crops)
    if 60 <= moisture <= 80:
        evaluation['Moisture'] = 'Good'
    else:
        evaluation['Moisture'] = 'Bad'

    # Evaluate Temperature (15 - 35°C is ideal for most crops)
    if 15 <= temperature <= 35:
        evaluation['Temperature'] = 'Good'
    else:
        evaluation['Temperature'] = 'Bad'  # Temperature is too high

    # Generate Conclusion
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


# Sample soil values
soil_data = {
    "pH": 6.021427916171047,
    "soil_ec": 0.23770047282119494,
    "phosphorus": 15.98794726646431,
    "potassium": 133.20619268230152,
    "urea": 45.62737295210718,
    "tsp": 16.95280934240313,
    "mop": 23.362073652509867,
    "moisture": 79.23400589775385,
    "temperature": 52.094082666970834
}

# Get the evaluation and conclusion
soil_quality, soil_conclusion = evaluate_soil(**soil_data)

# Print the evaluation
for parameter, result in soil_quality.items():
    print(f"{parameter}: {result}")

# Print the conclusion
print("\nConclusion:", soil_conclusion)
