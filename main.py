import os
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Skin Clinic Campaign Analysis API")

# Load dataset
file_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_dir, "skin clinic campaign.csv")
data = pd.read_csv(data_path)

# Categorize customers based on unique products purchased in the last year
data['Product_Usage'] = pd.cut(
    data['Unique_Products_Purchased'],
    bins= [0, 4, 8, np.inf],
    labels= ['1-4', '5-8', '>8']
)

def calculate_segment_table(df, col, col_name, categories=None):
    if categories is None:
        categories = df[col].unique()
    rows = []
    for cat in categories:
        sub = df[df[col] == cat]
        total = len(sub)
        resp = (sub['Response_to_Campaign'] == 'Yes').sum()
        rate = round((resp / total) * 100, 2) if total > 0 else 0
        rows.append({
            col_name: cat,
            'Total Customers': total,
            'Responders': resp,
            'Response Rate (%)': f'{rate:.2f}%'
        })
    return pd.DataFrame(rows)

# Generate tables for each customer segment
gender_table = calculate_segment_table(data, 'Gender', 'Gender', ['Female', 'Male'])
age_table = calculate_segment_table(data, 'AgeGroup', 'Age Group', ['<30', '30-50', '>50'])
purchase_table = calculate_segment_table(data, 'Purchase_Last_Quarter', 'Purchase in Last Quarter', ['Yes', 'No'])
product_usage_table = calculate_segment_table(data, 'Product_Usage', 'Unique Products Purchased', ['1-4', '5-8', '>8'])

def render_tabular_html():
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Skin Clinic Campaign Analysis</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #fafafa;
                    color: #333333;
                }}
                h1 {{
                    color: #1e293b;
                    margin-bottom: 5px;
                }}
                p.subtitle {{
                    color: #64748b;
                    margin-top: 0;
                    margin-bottom: 30px;
                }}
                h2 {{
                    color: #334155;
                    font-size: 18px;
                    margin-top: 30px;
                    margin-bottom: 10px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 70%;
                    max-width: 700px;
                    background: #ffffff;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    margin-bottom: 25px;
                }}
                th, td {{
                    border: 1px solid #e2e8f0;
                    text-align: left;
                    padding: 10px 14px;
                }}
                th {{
                    background-color: #f1f5f9;
                    font-weight: 600;
                    color: #1e293b;
                }}
                tr:hover {{
                    background-color: #f8fafc;
                }}
            </style>
        </head>
        <body>
            <h1>Skin Clinic Campaign Analysis</h1>
            <p class="subtitle">M10 PMLS - Assignment 1: Model Deployment Using FastAPI</p>

            <h2>1. Gender vs Campaign Response</h2>
            {gender_table.to_html(index=False)}

            <h2>2. Age Group vs Campaign Response</h2>
            {age_table.to_html(index=False)}

            <h2>3. Purchase in Last Quarter vs Campaign Response</h2>
            {purchase_table.to_html(index=False)}

            <h2>4. Product Usage vs Campaign Response</h2>
            {product_usage_table.to_html(index=False)}
        </body>
    </html>
    """

# Both root "/" and "/campaign-analysis" return the tabular format directly
@app.get("/", response_class=HTMLResponse)
def root():
    return render_tabular_html()

@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():
    return render_tabular_html()
