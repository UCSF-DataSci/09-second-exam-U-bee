import pandas as pd
from scipy.stats import f_oneway
import statsmodels.formula.api as smf

data = pd.read_csv('processed_data.csv')
data['visit_date'] = pd.to_datetime(data['visit_date'])

def analyze_walking_speed(data):
    data['education_level'] = data['education_level'].astype('category')
    formula = "walking_speed ~ age + C(education_level)"
    model = smf.mixedlm(formula, data, groups=data['patient_id'])
    result = model.fit()
    
    print("\nWalking Speed Regression Results:")
    print(result.summary())
    
    print("\nSignificant Trends in Walking Speed:")
    age_trend = smf.ols('walking_speed ~ age', data=data).fit()
    print(age_trend.summary())

def analyze_costs(data):
    print("\nInsurance Type Effect on Visit Costs:")
    grouped = data.groupby('insurance_type')['visit_cost']
    print(grouped.mean())
    
    insurance_types = data['insurance_type'].unique()
    cost_data = [data[data['insurance_type'] == ins]['visit_cost'] for ins in insurance_types]
    f_stat, p_val = f_oneway(*cost_data)
    print(f"ANOVA Result: F-stat={f_stat}, p-value={p_val}")

def advanced_analysis(data):
    formula = "walking_speed ~ age * C(education_level)"
    model = smf.mixedlm(formula, data, groups=data['patient_id'])
    result = model.fit()
    print("\nEducation-Age Interaction Results:")
    print(result.summary())

    print("\nControl for Confounders in Walking Speed:")
    confounder_model = smf.mixedlm("walking_speed ~ age + C(education_level) + visit_cost", data, groups=data['patient_id'])
    confounder_result = confounder_model.fit()
    print(confounder_result.summary())

analyze_walking_speed(data)
analyze_costs(data)
advanced_analysis(data)
