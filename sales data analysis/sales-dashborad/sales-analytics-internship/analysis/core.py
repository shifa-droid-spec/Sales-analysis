import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json
import os

class SalesAnalyzer:
    def __init__(self):
        self.products = ['Laptop', 'Phone', 'Tablet', 'Accessories']
        self.regions = ['North', 'South', 'East', 'West']
        self.metrics = {}
        
    def generate_data(self, days=90, customers=20):
        """Generate realistic sales data with business patterns"""
        np.random.seed(42)
        
        dates = [datetime(2023,1,1) + timedelta(days=i) for i in range(days)]
        weekday_pattern = [1.2 if d.weekday() < 5 else 0.8 for d in dates]  # Weekend effect
        
        data = {
            'date': dates,
            'product': np.random.choice(self.products, days, p=[0.4, 0.3, 0.2, 0.1]),
            'customer': [f"CUST-{np.random.randint(1000,9999)}" for _ in range(days)],
            'region': np.random.choice(self.regions, days, p=[0.3, 0.3, 0.2, 0.2]),
            'quantity': np.random.poisson(2, days) + 1,
            'unit_price': np.random.normal(500, 150, days).round(2),
            'discount': np.random.uniform(0, 0.3, days) * (np.random.rand(days) > 0.7)  # 30% chance
        }
        
        df = pd.DataFrame(data)
        df['revenue'] = df['quantity'] * df['unit_price'] * (1 - df['discount']) * weekday_pattern
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/sales_records.csv', index=False)
        return df
    
    def analyze(self):
        """Run full analysis pipeline"""
        df = self.generate_data()
        
        # Key Metrics
        self.metrics = {
            'total_revenue': df['revenue'].sum(),
            'avg_order_value': df['revenue'].mean(),
            'conversion_rate': len(df) / len(df['customer'].unique()),
            'top_product': df.groupby('product')['revenue'].sum().idxmax()
        }
        
        # Generate Visualizations
        self._generate_charts(df)
        self._save_insights()
        
        return self.metrics
    
    def _generate_charts(self, df):
        """Create professional visualizations"""
        os.makedirs('static/images', exist_ok=True)
        
        # Revenue by Product
        plt.figure(figsize=(10,6))
        df.groupby('product')['revenue'].sum().sort_values().plot(
            kind='barh', color='#4361ee')
        plt.title('Revenue by Product Category')
        plt.tight_layout()
        plt.savefig('static/images/product_revenue.png')
        plt.close()
        
        # Monthly Trend
        plt.figure(figsize=(10,5))
        df.groupby('month')['revenue'].sum().plot(
            kind='line', marker='o', color='#3a0ca3')
        plt.title('Monthly Revenue Trend')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/images/monthly_trend.png')
        plt.close()
        
    def _save_insights(self):
        """Export analysis results"""
        with open('data/insights.json', 'w') as f:
            json.dump({
                'metrics': self.metrics,
                'generated_at': str(datetime.now()),
                'recommendations': [
                    f"Focus on {self.metrics['top_product']} - highest revenue generator",
                    "Run weekend promotions to boost off-peak sales",
                    "Implement loyalty program for frequent customers"
                ]
            }, f)