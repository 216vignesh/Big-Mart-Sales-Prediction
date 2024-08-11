import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib
import sklearn
print(sklearn.__version__)
# df_train = pd.read_csv('../data/train.csv')
# df_test = pd.read_csv('../data/test.csv')

def preprocess_data(filepath):
    df_train=pd.read_csv(filepath)
    df_train['Item_Weight'].fillna(df_train['Item_Weight'].mean(), inplace=True)
    df_train['Outlet_Size'].fillna(df_train['Outlet_Size'].mode()[0], inplace=True)
    df_train['Item_Fat_Content'] = df_train['Item_Fat_Content'].replace({'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'})
    df_train['Outlet_Age'] = 2024 - df_train['Outlet_Establishment_Year']

    # Drop the original 'Outlet_Establishment_Year' as it's now redundant
    df_train.drop('Outlet_Establishment_Year', axis=1, inplace=True)
    df_train['Outlet_Location_Type*Outlet_Type'] = df_train['Outlet_Location_Type'] + "*" + df_train['Outlet_Type']
    df_train['Outlet_Location_Type*Item_Type'] = df_train['Outlet_Location_Type'] + "*" + df_train['Item_Type']
    from sklearn.preprocessing import LabelEncoder
    le=LabelEncoder()
    visibility_avg = df_train.pivot_table(values='Item_Visibility', index='Item_Identifier')
    df_train.loc[df_train['Item_Visibility'] == 0, 'Item_Visibility'] = df_train.loc[df_train['Item_Visibility'] == 0, 'Item_Identifier'].apply(lambda x: visibility_avg.at[x, 'Item_Visibility'])
    df_train.to_csv('data/cleaned_data.csv', index=False)
if __name__ == "__main__":
    preprocess_data('data/train.csv')
    



