# train_model.py
from machine import Machine
import pandas as pd
import os

# Use the correct path to your data
df = pd.read_csv(r'C:\All Folder\Bloomtech\Assignments\Sprint 21-24\Bloomtech Underdog\your_data_file.csv')

# Initialize the Machine class with your data and train the model
machine = Machine(df)

# Ensure the 'app' directory exists
app_dir = os.path.join('C:', 'All Folder', 'Bloomtech', 'Assignments', 'Sprint 21-24', 'Bloomtech Underdog', 'app')
if not os.path.exists(app_dir):
    os.makedirs(app_dir)

# Save the model to the 'app' directory
machine.save(os.path.join(app_dir, 'model.joblib'))

@APP.route('/model', methods=['GET', 'POST'])
def model():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')
    prediction, confidence = None, None  # Initialize to None
    level, health, energy, sanity = None, None, None, None  # Initialize form variables to None
    retrain = False  # Initialize retrain checkbox to unchecked

    if request.method == 'POST':
        level = request.form.get('level', type=float)
        health = request.form.get('health', type=float)
        energy = request.form.get('energy', type=float)
        sanity = request.form.get('sanity', type=float)
        retrain = 'retrain' in request.form

        if retrain or not os.path.exists(model_path):
            db = Database()
            df = db.dataframe()  # Fetch data from MongoDB
            machine = Machine()
            machine.train(df)
            machine.save(model_path)
        else:
            machine = Machine.load(model_path)

        features = pd.DataFrame([[level, health, energy, sanity]], columns=['Level', 'Health', 'Energy', 'Sanity'])
        prediction, confidence = machine.predict(features)
        confidence = f"{confidence * 100:.2f}%"  # Format confidence as a percentage
    else:
        # For GET request, simply generate random values without making predictions
        level = random_int(1, 20)  # Example: Assuming levels are between 1 and 20
        health = random_float(10, 100)  # Example range
        energy = random_float(10, 100)
        sanity = random_float(10, 100)
        # No prediction or confidence calculation here

    return render_template('model.html', timestamp=timestamp,
                           prediction=prediction, confidence=confidence,
                           level=level, health=health, energy=energy,
                           sanity=sanity, retrain=retrain)
