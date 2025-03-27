# Importing required libraries
import streamlit as st
import pandas as pd
import pickle

# Confirm app is loading
st.write("✅ App loaded successfully.")

# Load the trained model
with open("best_model.pkl", "rb") as file:
    model = pickle.load(file)

# App UI
st.title("🏠 Home Loan Approval Predictor")
st.markdown("Welcome! Please fill in your information below to check your loan approval eligibility.")

# Inputs
married = st.selectbox("Married?", ["Yes", "No"])
dependents = st.selectbox("Number of Dependents", ["0", "1", "2"])
education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed?", ["Yes", "No"])
applicant_income = st.number_input("Applicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
loan_term = st.selectbox("Loan Amount Term (in months)", [360, 180, 120, 84, 60, 36, 12])
credit_history = st.selectbox("Credit History ?", ["Yes", "No"])
rural_area = st.selectbox("Rural Property ?", ["Yes", "No"])
semi_urban = st.selectbox("Semi Urban Property ?", ["Yes", "No"])
urban_area = st.selectbox("Urban Property ?", ["Yes", "No"])

# Conditional input for coapplicant
if married == 'Yes':
    coapplicant_income = st.number_input("CoapplicantIncome", min_value=0)
else:
    coapplicant_income = 0

# Prediction trigger
if st.button("Check Loan Eligibility"):

    # Creating an input dictionary
    input_dict = {
        "married_Yes": [married],
        "Rural": [rural_area],
        "Semiurban" : [semi_urban],
        "Urban" : [urban_area],
        "tot_income": [applicant_income + coapplicant_income]
    }

    input_df = pd.DataFrame(input_dict)

    # Encode categorical variables using same mapping as in training
    replace_dict = {
        "Gender": {"Male": 1, "Female": 0},
        "married_Yes": {"Yes": 1, "No": 0},
        "Rural": {"Yes": 1, "No": 0},
        "Semiurban" : {"Yes": 1, "No": 0},
        "Urban" : {"Yes": 1, "No": 0}
    }

    input_df.replace(replace_dict, inplace=True)

    # Safe prediction with error handling
    try:
        prediction = model.predict(input_df)[0]

        if prediction == 1:
            st.success("✅ Your loan is likely to be approved!")
        else:
            st.error("❌ Sorry, your loan is likely to be denied.")

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
        st.write("📄 Here's the input data that caused the issue:")
        st.dataframe(input_df)