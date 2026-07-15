import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Electricity Price Forecasting",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------
# Title
# ---------------------------------------
st.title("⚡ Electricity Market Price Forecasting")

st.markdown("""
### Real-Time Market Clearing Price Prediction

This application predicts **Day-Ahead Electricity Prices (MCP)** using a trained **Random Forest Regression** model.

---

### 📌 Project Summary

- **Dataset:** IEX Day-Ahead Market (2018–2024)
- **Target Variable:** MCP (Rs/MWh)
- **Machine Learning Model:** Random Forest Regressor
- **Deployment:** Streamlit
- **Purpose:** Predict electricity prices from bidding and market features.

---
""")

# ---------------------------------------
# Load Model
# ---------------------------------------
from pathlib import Path

@st.cache_resource
def load_model():
    model_path = Path(__file__).parent.parent / "models" / "electricity_price_model.pkl"
    return joblib.load(model_path)

with st.sidebar:

    st.header("📁 Project Details")

    st.write("### Dataset")
    st.write("IEX Day Ahead Market")

    st.write("### Algorithm")
    st.write("Random Forest Regression")

    st.write("### Features")
    st.write("19 Engineered Features")

    st.write("### Target")
    st.write("Market Clearing Price (Rs/MWh)")

    st.write("### Model")
    st.success("Random Forest Regressor")

    st.write("### R² Score")
    st.success("0.9813")

    st.divider()

    st.write("### Built With")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- Scikit-Learn")
    st.write("- Streamlit")

model = load_model()

# ---------------------------------------
# Header
# ---------------------------------------
#st.title("⚡ Electricity Market Price Forecasting")

st.markdown("""
Predict **Day-Ahead Market (DAM)** electricity prices using a Machine Learning model.

This project was built using:

- Random Forest Regression
- IEX Day-Ahead Market Dataset
- Streamlit
- Python
""")

st.success("✅ Model Loaded Successfully")

col1, col2, col3 = st.columns(3)

col1.metric("R² Score", "0.9813")
col2.metric("MAE", "188.65")
col3.metric("RMSE", "379.22")

# -------------------------------------------------
# Prediction Inputs
# -------------------------------------------------

st.header("📊 Enter Market Inputs")

col1, col2 = st.columns(2)

with col1:
    purchase_bid = st.number_input(
        "Purchase Bid (MW)",
        min_value=0.0,
        value=9000.0
    )

    sell_bid = st.number_input(
        "Sell Bid (MW)",
        min_value=0.0,
        value=11000.0
    )

    mcv = st.number_input(
        "MCV (MW)",
        min_value=0.0,
        value=6200.0
    )

with col2:

    final_volume = st.number_input(
        "Final Scheduled Volume (MW)",
        min_value=0.0,
        value=6200.0
    )

    prediction_date = st.date_input("Prediction Date")

    prediction_time = st.time_input("Prediction Time")

predict = st.button("⚡ Predict Electricity Price")

if predict:

    # Create a reference row
    input_data = {
        "Purchase Bid (MW)": purchase_bid,
        "Sell Bid (MW)": sell_bid,
        "MCV (MW)": mcv,
        "Final Scheduled Volume (MW)": final_volume,

        # Reference lag features
        "Lag_1": 1859.84,
        "Lag_4": 2359.78,
        "Lag_96": 2219.64,
        "Lag_672": 1999.21,

        "Rolling_Mean_4": 2097.3375,
        "Rolling_Mean_96": 2995.368333,

        # Calendar features
        "Year": prediction_date.year,
        "Month": prediction_date.month,
        "Day": prediction_date.day,
        "Hour": prediction_time.hour,
        "Minute": prediction_time.minute,
        "DayOfWeek": prediction_date.weekday(),
        "Quarter": ((prediction_date.month - 1) // 3) + 1,
        "WeekOfYear": prediction_date.isocalendar()[1],
        "IsWeekend": 1 if prediction_date.weekday() >= 5 else 0
    }

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]

    st.success("Prediction Completed Successfully!")

    st.subheader("⚡ Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Predicted MCP",
            value=f"{prediction:.2f} Rs/MWh"
        )

    with col2:
        st.metric(
            label="Model Used",
            value="Random Forest"
        )

    st.caption(
        "This prediction is generated using the trained Random Forest Regression model "
        "based on the provided market inputs and engineered time features."
    )

   