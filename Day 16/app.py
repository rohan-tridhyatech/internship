import streamlit as st
import pandas as pd
import joblib

# Title and description
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
        }
        .subtitle {
            font-size: 1.2rem;
            text-align: center;
            color: #666;
        }
    </style>
    <div class="main-title">🏠 House Price Prediction App</div>
    <div class="subtitle">This app predicts house prices based on user inputs.</div>
    """,
    unsafe_allow_html=True
)

# Load the pre-trained model
@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

# Sidebar inputs
st.sidebar.header("🔧 Input Features")
def user_input_features():
    feature_input_html = """
    <style>
        .feature-input {
            margin: 10px 0;
            padding: 5px;
        }
        .feature-input label {
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
    """
    st.markdown(feature_input_html, unsafe_allow_html=True)

    CRIM = st.sidebar.number_input("CRIM (crime rate)", 0.0, 100.0, step=0.1)
    ZN = st.sidebar.number_input("ZN (residential land proportion)", 0.0, 100.0, step=0.1)
    INDUS = st.sidebar.number_input("INDUS (non-retail acres)", 0.0, 100.0, step=0.1)
    CHAS = st.sidebar.selectbox("CHAS (Charles River proximity)", [0, 1])
    NOX = st.sidebar.number_input("NOX (nitric oxide concentration)", 0.0, 1.0, step=0.01)
    RM = st.sidebar.number_input("RM (avg rooms per dwelling)", 1.0, 10.0, step=0.1)
    AGE = st.sidebar.number_input("AGE (old units proportion)", 0.0, 100.0, step=0.1)
    DIS = st.sidebar.number_input("DIS (distance to jobs)", 0.0, 20.0, step=0.1)
    RAD = st.sidebar.number_input("RAD (highway accessibility index)", 1, 24, step=1)
    TAX = st.sidebar.number_input("TAX (property tax rate)", 0, 1000, step=1)
    PTRATIO = st.sidebar.number_input("PTRATIO (pupil-teacher ratio)", 0.0, 50.0, step=0.1)
    B = st.sidebar.number_input("B (Black population proportion)", 0.0, 400.0, step=1.0)
    LSTAT = st.sidebar.number_input("LSTAT (% lower status population)", 0.0, 50.0, step=0.1)

    data = {
        'CRIM': CRIM, 'ZN': ZN, 'INDUS': INDUS, 'CHAS': CHAS,
        'NOX': NOX, 'RM': RM, 'AGE': AGE, 'DIS': DIS,
        'RAD': RAD, 'TAX': TAX, 'PTRATIO': PTRATIO,
        'B': B, 'LSTAT': LSTAT
    }
    return pd.DataFrame([data])

input_df = user_input_features()

# Display inputs
st.markdown("### 📝 User Input Features")
table_html = """
<style>
    table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
    th { background-color: #4CAF50; color: white; }
    tr:nth-child(even) { background-color: #f2f2f2; }
    tr:hover { background-color: #ddd; }
</style>
<table>
    <tr>
        <th>Feature</th>
        <th>Value</th>
    </tr>
"""
for feature, value in input_df.iloc[0].items():
    table_html += f"<tr><td>{feature}</td><td>{value}</td></tr>"

table_html += "</table>"
st.markdown(table_html, unsafe_allow_html=True)

# Ensure input matches model's expected features
try:
    input_df = input_df.reindex(columns=model.get_booster().feature_names, fill_value=0)
except ValueError as e:
    st.error(f"Feature mismatch: {e}")
    st.stop()

# Predict button with styling
predict_button_html = """
<style>
    .predict-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px;
        cursor: pointer;
        border-radius: 5px;
    }
    .predict-button:hover {
        background-color: #45a049;
    }
</style>
<div style="text-align:center;">
    <button class="predict-button" onclick="predict()">Predict House Price</button>
</div>
"""

# Prediction and output
if st.button("🔮 Predict House Price"):
    prediction = model.predict(input_df)[0]
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; border: 2px solid #4CAF50; 
        border-radius: 10px; color: #4CAF50; font-size: 1.5rem;">
            <b>🏠 Predicted House Price:</b> ${prediction:,.2f}
        </div>
        """,
        unsafe_allow_html=True
    )
