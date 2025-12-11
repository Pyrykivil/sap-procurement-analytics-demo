import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/sap_procurement_data.csv')

# Converting date columns to datetime
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

# Total spend (adjusted for discount)
df['TotalSpend'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

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

# Quality issues per supplier
quality_issues_supplier = df[df['QualityIssues'] == 'Yes'].groupby('Supplier').size()
print("\nQuality Issues per Supplier:")
print(quality_issues_supplier)

# Average discount per supplier
avg_discount_supplier = df.groupby('Supplier')['Discount'].mean()
print("\nAverage Discount per Supplier:")
print(avg_discount_supplier)

# Orders by month
df['OrderMonth'] = df['OrderDate'].dt.to_period('M')
orders_by_month = df.groupby('OrderMonth').size()
print("\nOrders by Month:")
print(orders_by_month)

# Orders by supplier and month
orders_supplier_month = df.groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
print("\nOrders by Supplier and Month:")
print(orders_supplier_month)

# Monthly total spend per supplier
spend_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['TotalSpend'].sum().unstack(fill_value=0)
print("\nMonthly Total Spend per Supplier:")
print(spend_supplier_month)

# Monthly average quantity per supplier
quantity_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Quantity'].mean().unstack(fill_value=0)
print("\nMonthly Average Quantity per Supplier:")
print(quantity_supplier_month)

# Monthly quality issues per supplier
issues_supplier_month = df[df['QualityIssues'] == 'Yes'].groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
print("\nMonthly Quality Issues per Supplier:")
print(issues_supplier_month)

# Monthly average discount per supplier
discount_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Discount'].mean().unstack(fill_value=0)
print("\nMonthly Average Discount per Supplier:")
print(discount_supplier_month)

# Visualizations
plt.figure(figsize=(15, 12))

# Monthly Total Spend per Supplier
plt.subplot(3, 2, 1)
total_spend_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Total Spend per Supplier')
plt.ylabel('')

# Monthly Average Quantity per Supplier
plt.subplot(3, 2, 2)
for supplier in quantity_supplier_month.index:
    quantity_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Average Quantity per Supplier')
plt.ylabel('Average Quantity')
plt.xticks(rotation=45)
plt.legend()

# Monthly Orders per Supplier
plt.subplot(3, 2, 3)
for supplier in orders_supplier_month.index:
    orders_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Orders per Supplier')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.legend()

# Monthly Quality Issues per Supplier
plt.subplot(3, 2, 4)
for supplier in issues_supplier_month.index:
    issues_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Quality Issues per Supplier')
plt.ylabel('Number of Issues')
plt.xticks(rotation=45)
plt.legend()

# Monthly Average Discount per Supplier
plt.subplot(3, 2, 5)
for supplier in discount_supplier_month.index:
    discount_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Average Discount per Supplier')
plt.ylabel('Average Discount (%)')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.savefig('procurement_analysis.png')
print("\nVisualization saved as procurement_analysis.png")