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
    "Discount": np.round(np.random.uniform(0, 0.2, n), 2),
    "ComplianceStatus": np.random.choice(["Compliant", "Non-compliant"], n, p=[0.85, 0.15]),
    "DuplicateFlag": np.random.choice(["No", "Yes"], n, p=[0.95, 0.05]),
    "ContractStatus": np.random.choice(["On-contract", "Off-contract"], n, p=[0.8, 0.2]),
    "MarketPrice": np.round(np.random.uniform(4, 160, n), 2),
    "SavingsPotential": lambda x: np.round((x["MarketPrice"] - x["UnitPrice"]) / x["MarketPrice"] * 100, 2) if x["UnitPrice"] < x["MarketPrice"] else 0,
    "PaymentTerms": np.random.choice(["Net 30", "Net 60", "2/10 Net 30", "1/15 Net 45"], n),
    "EarlyDiscount": np.where(np.random.choice([True, False], n, p=[0.3, 0.7]), np.round(np.random.uniform(0.01, 0.05, n), 2), 0),
    "DeliveryScore": np.random.randint(1, 11, n),
    "QualityScore": np.random.randint(1, 11, n),
    "FinancialHealth": np.random.choice(["Strong", "Moderate", "Weak"], n, p=[0.5, 0.3, 0.2]),
    "RiskScore": np.random.randint(1, 101, n),
    "DisruptionProbability": np.round(np.random.uniform(0, 1, n), 2),
    "ConsolidationPotential": np.random.choice(["High", "Medium", "Low"], n, p=[0.2, 0.5, 0.3])
}

df = pd.DataFrame(data)
df['SavingsPotential'] = np.where(df['UnitPrice'] < df['MarketPrice'], 
                                  np.round((df['MarketPrice'] - df['UnitPrice']) / df['MarketPrice'] * 100, 2), 0)
df.to_csv("data/sap_procurement_data.csv", index=False)
print("File saved to data/sap_procurement_data.csv")