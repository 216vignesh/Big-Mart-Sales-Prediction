from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Create a Flask application
app = Flask(__name__)

# Load your trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        # Convert data into DataFrame
        data_df = pd.DataFrame([data])
        
        # Make prediction
        predictions = model.predict(data_df)
        
        # Return the prediction as JSON
        return jsonify({'prediction': list(predictions)})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
