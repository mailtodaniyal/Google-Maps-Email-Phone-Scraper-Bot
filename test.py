import pandas as pd

sample_data = [
    {"name": "Joe's Coffee House", "phone": "+1 212-555-1234", "email": "contact@joescoffee.com"},
    {"name": "Brew Bros NYC", "phone": "+1 646-555-9876", "email": "hello@brewbrosnyc.com"},
    {"name": "Cafe Luna", "phone": "+1 917-555-4321", "email": "info@cafeluna.com"},
]

df = pd.DataFrame(sample_data)
df.to_csv("sample_business_data.csv", index=False)
print("Sample CSV generated: sample_business_data.csv")
