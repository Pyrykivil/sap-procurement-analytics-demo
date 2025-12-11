import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

os.makedirs("data", exist_ok=True)

np.random.seed(42)

# N = number of samples
n = 2000

suppliers = ['PekanMutteri', 'JarkonPaja', 'O-Rauta', 'MarkunTukki']
categories = ['Electrical', 'Mechanical', 'Hydraulics', 'Consumables']

data = {
    "PurchaseOrder": [f"PO{i:04d}" for i in range(1, n+1)],
    "Supplier": np.random.choice(suppliers, n),
    "Material": [f"MAT{i:03d}" for i in range(1, n+1)],
    "Quantity": np.random.randint(10, 500, n),
    "UnitPrice": np.round(np.random.uniform(5, 150, n), 2),
    "OrderDate": [datetime(2024,1,1) + timedelta(days=int(x)) for x in np.random.uniform(0, 300, n)],
    "DeliveryDate": [datetime(2024,1,1) + timedelta(days=int(x)) for x in np.random.uniform(5, 350, n)],
    "Category": np.random.choice(categories, n),
    "QualityIssues": np.random.choice(["No", "Yes"], n, p=[0.9, 0.1]),
    "Discount": np.round(np.random.uniform(0, 0.2, n), 2)   
}

df = pd.DataFrame(data)
df.to_csv("data/sap_procurement_data.csv", index=False)
print("File saved to data/sap_procurement_data.csv")