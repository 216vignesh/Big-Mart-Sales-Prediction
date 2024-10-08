from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load
import mlflow.pyfunc
app = Flask(__name__)
from mlflow.tracking import MlflowClient
mlflow.set_tracking_uri('http://192.168.137.1:5000')



@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
#test
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # model = mlflow.pyfunc.load_model('models:/BigMartSalesModel/Production')
        # data = {key: request.form[key] for key in request.form.keys()}
        # data_df = pd.DataFrame([data])
        
        client = MlflowClient()
        model_version_info = client.get_latest_versions('BigMartSalesModel', stages=['Production'])
        model_uri = f"models:/{model_version_info[0].name}/{model_version_info[0].version}"
        model = mlflow.pyfunc.load_model(model_uri)

        # Process the input data and predict
        data = {key: request.form[key] for key in request.form.keys()}
        data_df = pd.DataFrame([data])
        predictions = model.predict(data_df)
        return f'Predicted Sales: {predictions[0]}'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
