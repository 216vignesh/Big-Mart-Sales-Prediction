from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load

app = Flask(__name__)

# Load the model using joblib
model = load('./models/advanced_sales_prediction_pipeline.pkl')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {key: request.form[key] for key in request.form.keys()}
        data_df = pd.DataFrame([data])
        predictions = model.predict(data_df)
        return f'Predicted Sales: {predictions[0]}'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
