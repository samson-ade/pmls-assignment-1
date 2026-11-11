import os
import pandas as pd
import numpy as np

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title= "Skin Clinic Campaign Analysis API")

# Load dataset
file_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_dir, "skin clinic campaign.csv")
data = pd.read_csv(data_path)

# Categorise customers based on unique products purchased in the last year
data['Product_Usage'] = pd.cut(
    data['Unique_Products_Purchased'],
    bins= [0, 4, 8, np.inf],
    labels= ['1-4', '5-8', '>8']
)

def calculate_response_rate(df, column):
    results = []
    for category in df[column].unique():
        category_data = df[df[column] == category]
        total_customers = len(category_data)
        responders = (category_data['Response_to_Campaign'] == 'Yes').sum()
        response_rate = (responders / total_customers * 100) if total_customers > 0 else 0
        
        results.append({
            "segment": category,
            "total_customers": int(total_customers),
            "responders": int(responders),
            "response_rate_pct": round(response_rate, 2)
        })
        
    return pd.DataFrame(results)

# Generate tables for each customer segment
gender_table = calculate_response_rate(data, "Gender")
age_table = calculate_response_rate(data, "AgeGroup")
purchase_table = calculate_response_rate(data, "Purchase_Last_Quarter")
product_usage_table = calculate_response_rate(data, "Product_Usage")

@app.get("/")
def home():
    return {
        "message": "Welcome to the Skin Clinic Campaign Analysis API. Visit /campaign-analysis to view the results in tabular format."
    }

@app.get("/campaign-analysis", response_class= HTMLResponse)
def get_campaign_analysis():
    html_content = f"""
    <html>
        <head>
            <title>Campaign Analysis</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 30px;
                }}
                h1 {{
                    color: #333333;
                }}
                h2 {{
                    color: #555555;
                    margin-top: 25px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 70%;
                    margin-bottom: 25px;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Skin Clinic Campaign Analysis</h1>

            <h2>1. Gender vs Campaign Response</h2>
            {gender_table.to_html(index= False)}

            <h2>2. Age Group vs Campaign Response</h2>
            {age_table.to_html(index= False)}

            <h2>3. Purchase in Last Quarter vs Campaign Response</h2>
            {purchase_table.to_html(index= False)}

            <h2>4. Product Usage vs Campaign Response</h2>
            {product_usage_table.to_html(index= False)}
        </body>
    </html>
    """
    return html_content
