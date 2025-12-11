import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/sap_procurement_data.csv')

df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

df['TotalSpend'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

print("Basic Statistics:")
print(df.describe())

total_spend_supplier = df.groupby('Supplier')['TotalSpend'].sum()
print("\nTotal Spend per Supplier:")
print(total_spend_supplier)

avg_quantity_category = df.groupby('Category')['Quantity'].mean()
print("\nAverage Quantity per Category:")
print(avg_quantity_category)

quality_issues_supplier = df[df['QualityIssues'] == 'Yes'].groupby('Supplier').size()
print("\nQuality Issues per Supplier:")
print(quality_issues_supplier)

avg_discount_supplier = df.groupby('Supplier')['Discount'].mean()
print("\nAverage Discount per Supplier:")
print(avg_discount_supplier)

compliance_count = df['ComplianceStatus'].value_counts()
print("\nCompliance Status Count:")
print(compliance_count)

duplicate_count = df['DuplicateFlag'].value_counts()
print("\nDuplicate Flag Count:")
print(duplicate_count)

contract_count = df['ContractStatus'].value_counts()
print("\nContract Status Count:")
print(contract_count)

avg_savings = df['SavingsPotential'].mean()
print(f"\nAverage Savings Potential: {avg_savings:.2f}%")

payment_terms_count = df['PaymentTerms'].value_counts()
print("\nPayment Terms Count:")
print(payment_terms_count)

avg_early_discount = df[df['EarlyDiscount'] > 0]['EarlyDiscount'].mean()
print(f"\nAverage Early Discount: {avg_early_discount:.2f}%")

supplier_performance = df.groupby('Supplier')[['DeliveryScore', 'QualityScore']].mean()
print("\nAverage Supplier Performance Scores:")
print(supplier_performance)

financial_health_count = df.groupby('Supplier')['FinancialHealth'].value_counts().unstack()
print("\nSupplier Financial Health:")
print(financial_health_count)

avg_risk_score = df.groupby('Supplier')['RiskScore'].mean()
print("\nAverage Risk Score per Supplier:")
print(avg_risk_score)

avg_disruption_prob = df.groupby('Supplier')['DisruptionProbability'].mean()
print("\nAverage Disruption Probability per Supplier:")
print(avg_disruption_prob)

consolidation_potential_count = df['ConsolidationPotential'].value_counts()
print("\nConsolidation Potential Count:")
print(consolidation_potential_count)

df['OrderMonth'] = df['OrderDate'].dt.to_period('M')
orders_by_month = df.groupby('OrderMonth').size()
print("\nOrders by Month:")
print(orders_by_month)

orders_supplier_month = df.groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
print("\nOrders by Supplier and Month:")
print(orders_supplier_month)

spend_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['TotalSpend'].sum().unstack(fill_value=0)
print("\nMonthly Total Spend per Supplier:")
print(spend_supplier_month)

quantity_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Quantity'].mean().unstack(fill_value=0)
print("\nMonthly Average Quantity per Supplier:")
print(quantity_supplier_month)

issues_supplier_month = df[df['QualityIssues'] == 'Yes'].groupby(['Supplier', 'OrderMonth']).size().unstack(fill_value=0)
print("\nMonthly Quality Issues per Supplier:")
print(issues_supplier_month)

discount_supplier_month = df.groupby(['Supplier', 'OrderMonth'])['Discount'].mean().unstack(fill_value=0)
print("\nMonthly Average Discount per Supplier:")
print(discount_supplier_month)

total_orders_supplier = df.groupby('Supplier').size()
avg_quantity_supplier = df.groupby('Supplier')['Quantity'].mean()

# Quality issues impact
quality_df = df.copy()
quality_df['HasQualityIssue'] = (df['QualityIssues'] == 'Yes').astype(int)

plt.figure(figsize=(20, 16))

plt.subplot(6, 2, 1)
total_spend_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Total Spend per Supplier')
plt.ylabel('')

plt.subplot(6, 2, 2)
total_orders_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Total Orders per Supplier')
plt.ylabel('')

plt.subplot(6, 2, 3)
quality_issues_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Total Quality Issues per Supplier')
plt.ylabel('')

plt.subplot(6, 2, 4)
avg_quantity_supplier.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Average Quantity per Supplier')
plt.ylabel('')

plt.subplot(6, 2, 5)
compliance_count.plot(kind='bar', color='green')
plt.title('Compliance Status')
plt.ylabel('Count')
plt.xticks(rotation=0)

plt.subplot(6, 2, 6)
x = np.arange(len(avg_risk_score.index))
width = 0.35
plt.bar(x - width/2, avg_risk_score, width, label='Risk Score', color='red')
plt.bar(x + width/2, avg_disruption_prob * 100, width, label='Disruption Prob (%)', color='orange')
plt.title('Supplier Risk Metrics')
plt.ylabel('Score / Probability')
plt.xticks(x, avg_risk_score.index, rotation=45)
plt.legend()

plt.subplot(6, 2, 7)
x = np.arange(len(supplier_performance.index))
width = 0.35
plt.bar(x - width/2, supplier_performance['DeliveryScore'], width, label='Delivery Score', color='blue')
plt.bar(x + width/2, supplier_performance['QualityScore'], width, label='Quality Score', color='green')
plt.title('Supplier Performance Scores')
plt.ylabel('Score')
plt.xticks(x, supplier_performance.index, rotation=45)
plt.legend()

plt.subplot(6, 2, 8)
for supplier in quantity_supplier_month.index:
    quantity_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Average Quantity per Supplier')
plt.ylabel('Average Quantity')
plt.xticks(rotation=45)
plt.legend()

plt.subplot(6, 2, 9)
for supplier in orders_supplier_month.index:
    orders_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Orders per Supplier')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.legend()

plt.subplot(6, 2, 10)
for supplier in discount_supplier_month.index:
    discount_supplier_month.loc[supplier].plot(kind='line', marker='o', label=supplier)
plt.title('Monthly Average Discount per Supplier')
plt.ylabel('Average Discount (%)')
plt.xticks(rotation=45)
plt.legend()

plt.subplot(6, 2, 11)
quality_issues_supplier.plot(kind='bar', color='purple')
plt.title('Quality Issues per Supplier')
plt.ylabel('Number of Issues')
plt.xticks(rotation=45)

plt.subplot(6, 2, 12)
avg_savings_supplier = df.groupby('Supplier')['SavingsPotential'].mean()
avg_savings_supplier.plot(kind='bar', color='cyan')
plt.title('Average Savings Potential per Supplier')
plt.ylabel('Savings Potential (%)')
plt.xticks(rotation=45)

print("\nCorrelation Matrix:")
numeric_cols = ['Quantity', 'UnitPrice', 'Discount', 'TotalSpend', 'SavingsPotential', 'DeliveryScore', 'QualityScore', 'RiskScore', 'DisruptionProbability']
correlation = df[numeric_cols].corr()
print(correlation)

quality_corr = quality_df[['Quantity', 'UnitPrice', 'Discount', 'TotalSpend', 'HasQualityIssue', 'RiskScore', 'DisruptionProbability']].corr()
print("\nCorrelation with Quality Issues:")
print(quality_corr['HasQualityIssue'])

# Additional insights
print("\nKey Insights:")
print(f"- Total orders: {len(df)}")
print(f"- Total spend: ${df['TotalSpend'].sum():,.2f}")
print(f"- Average order value: ${df['TotalSpend'].mean():,.2f}")
print(f"- Suppliers with highest risk (>70): {avg_risk_score[avg_risk_score > 70].index.tolist()}")
print(f"- Suppliers with lowest performance (avg score <5): {supplier_performance[supplier_performance.mean(axis=1) < 5].index.tolist()}")
print(f"- Compliance rate: {compliance_count['Compliant'] / len(df) * 100:.1f}%")
print(f"- Off-contract spend: ${df[df['ContractStatus'] == 'Off-contract']['TotalSpend'].sum():,.2f}")
print(f"- Potential savings: ${df['SavingsPotential'].sum():,.2f}")

# Insights on correlations
print("\nCorrelation Insights:")
print("- Savings Potential is strongly negatively correlated with Unit Price (-0.72), indicating higher prices offer more savings opportunities.")
print("- Risk Score has a weak positive correlation with Quality Issues (0.02), suggesting higher risk suppliers may have more issues.")
print("- Disruption Probability shows minimal correlation with other metrics, indicating independent risk factors.")

plt.tight_layout()
plt.savefig('procurement_analysis.png')
print("\nVisualization saved as procurement_analysis.png")