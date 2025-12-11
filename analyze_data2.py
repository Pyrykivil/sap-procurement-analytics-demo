import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/sap_procurement_data.csv')

df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

df['TotalSpend'] = df['UnitPrice'] * df['Quantity']

total_spend_supplier = df.groupby('Supplier')['TotalSpend'].sum()