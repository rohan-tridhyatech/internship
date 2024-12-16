import streamlit as st
import pandas as pd
import joblib 

# Title and description
st.title("House Price Prediction App")
st.write("This app predicts house prices based on user inputs for various features.")

# Load pre-trained model
@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

# Input fields for features
st.sidebar.header("Input Features")
def user_input_features():
    CRIM = st.sidebar.number_input("CRIM (per capita crime rate)", 0.0, 100.0, step=0.1)
    ZN = st.sidebar.number_input("ZN (proportion of residential land)", 0.0, 100.0, step=0.1)
    INDUS = st.sidebar.number_input("INDUS (proportion of non-retail business acres)", 0.0, 100.0, step=0.1)
    CHAS = st.sidebar.selectbox("CHAS (Charles River dummy variable)", [0, 1])
    NOX = st.sidebar.number_input("NOX (nitric oxide concentration)", 0.0, 1.0, step=0.01)
    RM = st.sidebar.number_input("RM (average number of rooms per dwelling)", 1.0, 10.0, step=0.1)
    AGE = st.sidebar.number_input("AGE (proportion of owner-occupied units built before 1940)", 0.0, 100.0, step=0.1)
    DIS = st.sidebar.number_input("DIS (distance to employment centers)", 0.0, 20.0, step=0.1)
    RAD = st.sidebar.number_input("RAD (index of accessibility to highways)", 1, 24, step=1)
    TAX = st.sidebar.number_input("TAX (property tax rate per $10,000)", 0, 1000, step=1)
    PTRATIO = st.sidebar.number_input("PTRATIO (pupil-teacher ratio)", 0.0, 50.0, step=0.1)
    B = st.sidebar.number_input("B (proportion of Black population)", 0.0, 400.0, step=1.0)
    LSTAT = st.sidebar.number_input("LSTAT (lower status population percentage)", 0.0, 50.0, step=0.1)

    # Create a DataFrame for the input features
    data = {
        'CRIM': CRIM, 'ZN': ZN, 'INDUS': INDUS, 'CHAS': CHAS,
        'NOX': NOX, 'RM': RM, 'AGE': AGE, 'DIS': DIS,
        'RAD': RAD, 'TAX': TAX, 'PTRATIO': PTRATIO,
        'B': B, 'LSTAT': LSTAT
    }
    return pd.DataFrame([data])

input_df = user_input_features()

# Display input features
st.subheader("User Input Features")
st.write(input_df)

# Ensure input features match the model's expected features
expected_features = model.get_booster().feature_names
try:
    input_df = input_df.reindex(columns=expected_features, fill_value=0)
except ValueError as e:
    st.error(f"Feature mismatch: {e}")
    st.stop()

# Make prediction
if st.button("Predict House Price"):
    prediction = model.predict(input_df)[0]
    st.subheader("Predicted House Price")
    st.write(f"${prediction:,.2f}")

