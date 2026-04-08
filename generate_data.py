import pandas as pd
import random

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
cost_centers = ["Marketing","IT","HR","Finance","Sales"]

data = []

for i in range(100):
    row = [
        random.choice(months),
        random.choice(cost_centers),
        random.randint(8000,20000),
        random.randint(9000,21000),
        random.randint(4000,12000),
        random.randint(4500,13000)
    ]
    data.append(row)

df = pd.DataFrame(data, columns=[
    "Month","Cost_Center","Revenue_Actual","Revenue_Budget","Cost_Actual","Cost_Budget"
])

df.to_excel("data/financials.xlsx", index=False)

print("✅ Data generated successfully!")