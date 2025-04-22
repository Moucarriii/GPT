import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Generate the dataset directly in the app ---
months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS').strftime('%B')
categories = ['Electronics', 'Clothing', 'Home & Kitchen']

np.random.seed(42)
data = []
for month in months:
    for category in categories:
        sales = np.random.randint(20000, 50000)
        profit_margin = np.random.uniform(0.1, 0.3)
        profit = round(sales * profit_margin)
        visitors = np.random.randint(5000, 15000)
        conversion_rate = np.random.uniform(0.02, 0.05)
        orders = round(visitors * conversion_rate)
        data.append([month, category, sales, profit, visitors, orders])

df = pd.DataFrame(data, columns=[
    'Month', 'Category', 'Sales ($)', 'Profit ($)', 'Website Visitors', 'Orders'
])

# Streamlit App
st.title("E-commerce Store 2024 Performance Dashboard")

# --- Sidebar Global Filters ---
st.sidebar.header("Global Filters")

# Category filter
category_options = df['Category'].unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Categories:",
    options=category_options,
    default=list(category_options)
)

# Month filter
month_options = df['Month'].unique()
selected_months = st.sidebar.multiselect(
    "Select Months:",
    options=month_options,
    default=list(month_options)
)

# Global filter data
global_filtered_df = df[(df['Category'].isin(selected_categories)) & (df['Month'].isin(selected_months))]

# --- Visual 1: Sales Over Time ---
st.subheader("Monthly Sales by Category")
st.markdown("This line chart shows how each product category performed over the months of 2024. Use the filters to explore specific trends.")
fig1 = px.line(global_filtered_df, x="Month", y="Sales ($)", color="Category", markers=True, title="Monthly Sales Trends")
st.plotly_chart(fig1)

# --- Visual 2: Profit vs Sales Scatter with Sales Threshold Slider ---
st.subheader("Profit vs Sales")
st.markdown("This scatter plot highlights the relationship between sales and profit. Use the slider below to filter out low-performing data points.")

# Add slider interaction
sales_threshold = st.slider("Minimum Sales Amount ($)", min_value=int(df['Sales ($)'].min()), max_value=int(df['Sales ($)'].max()), value=20000, step=1000)
filtered_profit_df = global_filtered_df[global_filtered_df['Sales ($)'] >= sales_threshold]

fig2 = px.scatter(filtered_profit_df, x="Sales ($)", y="Profit ($)", color="Category", size="Profit ($)", hover_name="Month", title="Profit vs Sales Bubble Chart")
st.plotly_chart(fig2)

# --- Visual 3: Orders by Category (Bar Chart) ---
st.subheader("Orders by Category")
st.markdown("This bar chart represents the total number of orders per category.")
orders_df = global_filtered_df.groupby("Category")["Orders"].sum().reset_index()
fig3 = px.bar(orders_df, x="Category", y="Orders", color="Category", title="Total Orders by Product Category")
st.plotly_chart(fig3)

# --- Visual 4: Conversion Rate Analysis with View Toggle ---
st.subheader("Conversion Rate Analysis")
st.markdown("Compare how effectively visitors turn into orders. Toggle between average and distribution view.")
global_filtered_df["Conversion Rate (%)"] = (global_filtered_df["Orders"] / global_filtered_df["Website Visitors"] * 100).round(2)

view_option = st.radio("View Mode:", ["Box Plot (Distribution)", "Bar Chart (Average)"])

if view_option == "Box Plot (Distribution)":
    fig4 = px.box(global_filtered_df, x="Category", y="Conversion Rate (%)", color="Category", title="Conversion Rate Distribution")
else:
    avg_conv_df = global_filtered_df.groupby("Category")["Conversion Rate (%)"].mean().reset_index()
    fig4 = px.bar(avg_conv_df, x="Category", y="Conversion Rate (%)", color="Category", title="Average Conversion Rate by Category")
st.plotly_chart(fig4)

# --- Visual 5: 3D Scatter (Sales, Profit, Visitors) ---
st.subheader("Sales, Profit, and Visitors Relationship")
st.markdown("A 3D view to understand how sales, profit, and visitors relate across categories.")
fig5 = px.scatter_3d(global_filtered_df, x="Sales ($)", y="Profit ($)", z="Website Visitors", color="Category", title="3D Sales-Profit-Visitors Analysis")
st.plotly_chart(fig5)

# End of App
st.markdown("---")
st.markdown("Data is fictional and created for visualization and storytelling purposes only.")
