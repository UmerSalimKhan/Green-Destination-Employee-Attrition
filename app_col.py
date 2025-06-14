import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load('attrition_model.pkl')

st.set_page_config(page_title="Employee Attrition Predictor", layout="wide")

st.title("👤 Employee Attrition Predictor")
st.markdown("Fill the details below to predict if the employee is likely to leave the company.")

# --- Layout in Two Columns ---
col1, col2 = st.columns(2)

with col1:
    age = st.slider('Age', 18, 60, 30)
    daily_rate = st.number_input('Daily Rate', 100, 1500, 800)
    distance_from_home = st.slider('Distance From Home (km)', 0, 50, 10)
    education = st.selectbox('Education Level', [1, 2, 3, 4, 5])
    environment_satisfaction = st.selectbox('Environment Satisfaction', [1, 2, 3, 4])
    hourly_rate = st.number_input('Hourly Rate', 30, 100, 60)
    job_involvement = st.selectbox('Job Involvement', [1, 2, 3, 4])
    job_level = st.selectbox('Job Level', [1, 2, 3, 4, 5])
    job_satisfaction = st.selectbox('Job Satisfaction', [1, 2, 3, 4])
    monthly_income = st.number_input('Monthly Income', 1000, 20000, 5000)
    monthly_rate = st.number_input('Monthly Rate', 1000, 30000, 15000)
    num_companies_worked = st.slider('Number of Companies Worked', 0, 10, 2)

with col2:
    percent_salary_hike = st.slider('Percent Salary Hike', 0, 100, 15)
    performance_rating = st.selectbox('Performance Rating', [1, 2, 3, 4])
    relationship_satisfaction = st.selectbox('Relationship Satisfaction', [1, 2, 3, 4])
    stock_option_level = st.selectbox('Stock Option Level', [0, 1, 2, 3])
    total_working_years = st.slider('Total Working Years', 0, 40, 10)
    training_times_last_year = st.slider('Training Times Last Year', 0, 10, 3)
    work_life_balance = st.selectbox('Work Life Balance', [1, 2, 3, 4])
    years_at_company = st.slider('Years at Company', 0, 40, 5)
    years_in_current_role = st.slider('Years in Current Role', 0, 20, 3)
    years_since_last_promotion = st.slider('Years Since Last Promotion', 0, 15, 1)
    years_with_curr_manager = st.slider('Years with Current Manager', 0, 20, 3)

# --- Categorical Inputs ---
st.markdown("---")
st.markdown("### Categorical Features")

cat1, cat2, cat3 = st.columns(3)

with cat1:
    business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Frequently", "Travel_Rarely"])
    department = st.selectbox("Department", ["Human Resources", "Research & Development", "Sales"])

with cat2:
    education_field = st.selectbox("Education Field", ["Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"])
    gender = st.selectbox("Gender", ["Female", "Male"])

with cat3:
    job_role = st.selectbox("Job Role", [
        "Healthcare Representative", "Human Resources", "Laboratory Technician", "Manager",
        "Manufacturing Director", "Research Director", "Research Scientist",
        "Sales Executive", "Sales Representative"])
    marital_status = st.selectbox("Marital Status", ["Divorced", "Married", "Single"])
    overtime = st.selectbox("OverTime", ["Yes", "No"])

# --- Encoding Function ---
def encode_input():
    data = {
        'Age': age,
        'DailyRate': daily_rate,
        'DistanceFromHome': distance_from_home,
        'Education': education,
        'EnvironmentSatisfaction': environment_satisfaction,
        'HourlyRate': hourly_rate,
        'JobInvolvement': job_involvement,
        'JobLevel': job_level,
        'JobSatisfaction': job_satisfaction,
        'MonthlyIncome': monthly_income,
        'MonthlyRate': monthly_rate,
        'NumCompaniesWorked': num_companies_worked,
        'PercentSalaryHike': percent_salary_hike,
        'PerformanceRating': performance_rating,
        'RelationshipSatisfaction': relationship_satisfaction,
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': total_working_years,
        'TrainingTimesLastYear': training_times_last_year,
        'WorkLifeBalance': work_life_balance,
        'YearsAtCompany': years_at_company,
        'YearsInCurrentRole': years_in_current_role,
        'YearsSinceLastPromotion': years_since_last_promotion,
        'YearsWithCurrManager': years_with_curr_manager,
    }

    # Initialize one-hot features to 0
    categories = [
        'BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
        'Department_Human Resources', 'Department_Research & Development', 'Department_Sales',
        'EducationField_Human Resources', 'EducationField_Life Sciences', 'EducationField_Marketing',
        'EducationField_Medical', 'EducationField_Other', 'EducationField_Technical Degree',
        'Gender_Female', 'Gender_Male',
        'JobRole_Healthcare Representative', 'JobRole_Human Resources', 'JobRole_Laboratory Technician',
        'JobRole_Manager', 'JobRole_Manufacturing Director', 'JobRole_Research Director',
        'JobRole_Research Scientist', 'JobRole_Sales Executive', 'JobRole_Sales Representative',
        'MaritalStatus_Divorced', 'MaritalStatus_Married', 'MaritalStatus_Single',
        'OverTime_No', 'OverTime_Yes'
    ]

    for cat in categories:
        data[cat] = 0

    data[f'BusinessTravel_{business_travel}'] = 1
    data[f'Department_{department}'] = 1
    data[f'EducationField_{education_field}'] = 1
    data[f'Gender_{gender}'] = 1
    data[f'JobRole_{job_role}'] = 1
    data[f'MaritalStatus_{marital_status}'] = 1
    data[f'OverTime_{overtime}'] = 1

    return pd.DataFrame([data])

# --- Prediction ---
if st.button("🔍 Predict Attrition"):
    input_df = encode_input()
    prediction = model.predict(input_df)[0]
    result = "✅ No, likely to stay." if prediction == 0 else "⚠️ Yes, likely to leave."
    st.success(f"**Attrition Prediction:** {result}")
