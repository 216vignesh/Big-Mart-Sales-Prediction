import pickle

# Load your model to inspect it
model = pickle.load(open('C:/Users/vigne/OneDrive/Documents/ML/Big-Mart-Sales-Prediction/Big-Mart-Sales-Prediction/models/advanced_sales_prediction_pipeline.pkl', 'rb'))
print(type(model))  # Check the type of the loaded object
print(model)        # Optionally, print or log the model to understand its structure
