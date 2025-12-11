import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/sap_procurement_data.csv')

# Converting date columns to datetime
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

# Total spend
df['TotalSpend'] = df['UnitPrice'] * df['Quantity']

# Basic statistics
print("Basic Statistics:")
print(df.describe())

# Total spend per supplier
total_spend_supplier = df.groupby('Supplier')['TotalSpend'].sum()
print("\nTotal Spend per Supplier:")
print(total_spend_supplier)

# Average quantity per category
avg_quantity_category = df.groupby('Category')['Quantity'].mean()
print("\nAverage Quantity per Category:")
print(avg_quantity_category)

# Orders by month
df['OrderMonth'] = df['OrderDate'].dt.to_period('M')
orders_by_month = df.groupby('OrderMonth').size()
print("\nOrders by Month:")
print(orders_by_month)

# Orders by supplier and month
orders_supplier_month = df.groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
print("\nOrders by Supplier and Month:")
print(orders_supplier_month)

# Visualizations
plt.figure(figsize=(12, 8))

# Total Spend per Supplier
plt.subplot(2, 2, 1)
total_spend_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Total Spend per Supplier')
plt.ylabel('')  # Remove ylabel for pie chart

# Average Quantity per Category
plt.subplot(2, 2, 2)
avg_quantity_category.plot(kind='bar', color='lightgreen')
plt.title('Average Quantity per Category')
plt.ylabel('Average Quantity')
plt.xticks(rotation=45)

# Orders by Month
plt.subplot(2, 2, 3)
orders_by_month.plot(kind='line', marker='o', color='orange')
plt.title('Total Orders by Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)

# Orders by Supplier per Month
plt.subplot(2, 2, 4)
for supplier in orders_supplier_month.index:
    orders_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Orders by Supplier per Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.savefig('procurement_analysis.png')
print("\nVisualization saved as procurement_analysis.png")