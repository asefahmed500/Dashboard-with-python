import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv('sales_data.csv')
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date column is in datetime format
    return data

# Load data
data = load_data()

# Header and Title
st.title('E-commerce Dashboard')
st.write('A comprehensive view of your e-commerce performance.')

# Sidebar for Filters
st.sidebar.header('Filters')
date_range = st.sidebar.date_input('Select Date Range', [data['Date'].min(), data['Date'].max()])
category = st.sidebar.selectbox('Select Category', ['All'] + list(data['Category'].unique()))
geography = st.sidebar.selectbox('Select Geography', ['All'] + list(data['Geography'].unique()))
customer_segment = st.sidebar.selectbox('Customer Segment', ['All', 'New', 'Returning'])

# Apply filters
filtered_data = data[(data['Date'] >= pd.to_datetime(date_range[0])) & (data['Date'] <= pd.to_datetime(date_range[1]))]
if category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == category]
if geography != 'All':
    filtered_data = filtered_data[filtered_data['Geography'] == geography]
if customer_segment != 'All':
    filtered_data = filtered_data[filtered_data['Customer_Type'] == customer_segment]

# Key Metrics Summary
st.subheader('Key Metrics')
st.metric('Total Sales', f"${filtered_data['Sales'].sum():,.2f}")
st.metric('Total Revenue', f"${filtered_data['Revenue'].sum():,.2f}")
st.metric('Number of Orders', f"{filtered_data['Order_ID'].nunique():,}")
st.metric('Average Order Value', f"${filtered_data['Revenue'].mean():,.2f}")
st.metric('Conversion Rate', f"{(filtered_data['Orders'] / filtered_data['Visits']).mean() * 100:.2f}%")

# Sales Over Time
st.subheader('Sales Over Time')
sales_over_time = filtered_data.groupby('Date')['Sales'].sum()
fig, ax = plt.subplots()
sales_over_time.plot(ax=ax)
st.pyplot(fig)

# Revenue Breakdown
st.subheader('Revenue Breakdown')
revenue_by_category = filtered_data.groupby('Category')['Revenue'].sum()
fig, ax = plt.subplots()
revenue_by_category.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Customer Insights
st.subheader('Customer Insights')
customer_type_counts = filtered_data['Customer_Type'].value_counts()
fig, ax = plt.subplots()
customer_type_counts.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Product Performance
st.subheader('Top Selling Products')
top_products = filtered_data.groupby('Product_Name')['Sales'].sum().nlargest(10)
st.write(top_products)

# Order Details
st.subheader('Recent Orders')
recent_orders = filtered_data[['Order_ID', 'Customer', 'Total_Amount', 'Status']].head(10)
st.write(recent_orders)

# Conversion Funnel
st.subheader('Conversion Funnel')
funnel_data = filtered_data.groupby('Stage')['Count'].sum()
fig, ax = plt.subplots()
funnel_data.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Traffic Sources
st.subheader('Traffic Sources')
traffic_sources = filtered_data['Traffic_Source'].value_counts()
fig, ax = plt.subplots()
traffic_sources.plot(kind='pie', ax=ax, autopct='%1.1f%%')
st.pyplot(fig)

# User Engagement
st.subheader('User Engagement')
avg_session_duration = filtered_data['Session_Duration'].mean()
bounce_rate = filtered_data['Bounce_Rate'].mean()
pages_per_session = filtered_data['Pages_Per_Session'].mean()
st.metric('Average Session Duration', f"{avg_session_duration:.2f} mins")
st.metric('Bounce Rate', f"{bounce_rate * 100:.2f}%")
st.metric('Pages Per Session', f"{pages_per_session:.2f}")
