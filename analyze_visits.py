import pandas as pd
import numpy as np
import random

#Step 1:
data = pd.read_csv("ms_data.csv")
data['visit_date'] = pd.to_datetime(data['visit_date'])
data = data.sort_values(by=['patient_id', 'visit_date']).reset_index(drop=True)

# Step 2:
with open("insurance.lst", 'r') as file:
    ins = [line.strip() for line in file.readlines()][1:]  

patients = data['patient_id'].unique()
ins_map = {i: random.choice(ins) for i in patients}
data['insurance_type'] = data['patient_id'].map(ins_map)

def calculate_cost(row):
    if row['insurance_type'] == "Basic":
        m = 2
    elif row['insurance_type'] == "Premium":
        m = 1.5
    elif row['insurance_type'] == "Platinum":
        m = 1
    else:
        print("something went terribly wrong in calculate_cost")
        return
    v = np.random.uniform(-20, 20)
    return 100 * m + v

data['visit_cost'] = data.apply(calculate_cost, axis=1)

# Step 3:
print("Summary Statistics:\n")

print("\nMean walking speed by education level:")
print(data.groupby('education_level')['walking_speed'].mean())

print("\nMean visit costs by insurance type:")
print(data.groupby('insurance_type')['visit_cost'].mean())

print("\nCorrelation between age and walking speed:")
print(data[['age', 'walking_speed']].corr().iloc[0, 1])

print("\nVariation in walking speed by month:")
data['month'] = data['visit_date'].dt.month
print(data.groupby('month')['walking_speed'].mean())

data.to_csv("processed_data.csv", index=False)