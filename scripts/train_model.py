import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment("BigMart_Sales_Prediction")
# def train_model(data_path):
#     df_train = pd.read_csv(data_path)
#     numeric_features = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Age']
#     categorical_features = ['Item_Fat_Content', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type', 'Item_Type', 'Outlet_Location_Type*Outlet_Type', 'Outlet_Location_Type*Item_Type']
#     preprocessor = ColumnTransformer(
#         transformers=[
#             ('num', StandardScaler(), numeric_features),
#             ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
#         ])
    
#     # Feature selection using SelectKBest
#     pipeline = Pipeline([
#         ('preprocessor', preprocessor),
#         ('feature_selection', SelectKBest(score_func=f_regression, k=20)),
#         ('regressor', XGBRegressor(objective='reg:squarederror', n_estimators=500, learning_rate=0.01, max_depth=3, subsample=0.9, colsample_bytree=0.9, random_state=0))
#     ])
#     y = df_train['Item_Outlet_Sales']
#     X = df_train.drop('Item_Outlet_Sales', axis=1)

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
#     pipeline.fit(X_train, y_train)
#     print("Model accuracy on test set:", pipeline.score(X_test, y_test))
#     joblib.dump(pipeline, 'models/advanced_sales_prediction_model.pkl')
def train_model(data_path):
    with mlflow.start_run():
        mlflow.log_artifact('BigMartSalesModel.pkl',artifact_path="runs")
        df_train = pd.read_csv(data_path)
        numeric_features = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Age']
        categorical_features = ['Item_Fat_Content', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type', 'Item_Type', 'Outlet_Location_Type*Outlet_Type', 'Outlet_Location_Type*Item_Type']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ])
        
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('feature_selection', SelectKBest(score_func=f_regression, k=20)),
            ('regressor', XGBRegressor(objective='reg:squarederror', n_estimators=500, learning_rate=0.01, max_depth=3, subsample=0.9, colsample_bytree=0.9, random_state=0))
        ])
        
        y = df_train['Item_Outlet_Sales']
        X = df_train.drop('Item_Outlet_Sales', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        pipeline.fit(X_train, y_train)
        
        # Evaluate the model and log metrics
        score = pipeline.score(X_test, y_test)
        mlflow.log_metric("accuracy", score)
        print("Model accuracy on test set:", score)

        # Log parameters
        mlflow.log_param("n_estimators", 500)
        mlflow.log_param("learning_rate", 0.01)
        mlflow.log_param("max_depth", 3)

        # Log model
        mlflow.sklearn.log_model(pipeline, "model")
        
        # Save the pipeline as a pickle file (optional if already logged via MLflow)
        # joblib.dump(pipeline, 'models/advanced_sales_prediction_model.pkl')
if __name__ == "__main__":
    train_model('data/cleaned_data.csv')