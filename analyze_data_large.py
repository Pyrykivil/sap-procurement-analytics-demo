import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the large dataset
df = pd.read_csv('data/sap_procurement_data_large.csv')

# Convert date columns to datetime
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

# Calculate total spend (adjusted for discount)
df['TotalSpend'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

# Basic statistics
print("Basic Statistics for Large Dataset:")
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

# Advanced Analysis: Correlations
print("\nCorrelation Matrix:")
numeric_cols = ['Quantity', 'UnitPrice', 'Discount', 'TotalSpend']
correlation = df[numeric_cols].corr()
print(correlation)

# Quality issues impact
quality_df = df.copy()
quality_df['HasQualityIssue'] = (df['QualityIssues'] == 'Yes').astype(int)
quality_corr = quality_df[['Quantity', 'UnitPrice', 'Discount', 'TotalSpend', 'HasQualityIssue']].corr()
print("\nCorrelation with Quality Issues:")
print(quality_corr['HasQualityIssue'])

# Visualizations (similar to before, but for large data)
orders_supplier_month = df.groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
spend_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['TotalSpend'].sum().unstack(fill_value=0)
quantity_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Quantity'].mean().unstack(fill_value=0)
issues_supplier_month = df[df['QualityIssues'] == 'Yes'].groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
discount_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Discount'].mean().unstack(fill_value=0)

plt.figure(figsize=(15, 12))

# Total Spend per Supplier (pie)
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

# Correlation Heatmap (simple bar for correlations with quality issues)
plt.subplot(3, 2, 6)
quality_corr['HasQualityIssue'].drop('HasQualityIssue').plot(kind='bar', color='orange')
plt.title('Correlation with Quality Issues')
plt.ylabel('Correlation Coefficient')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('procurement_analysis_large.png')
print("\nAdvanced analysis and visualization saved as procurement_analysis_large.png")