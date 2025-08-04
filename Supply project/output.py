#!/usr/bin/env python3
"""
Final Streamlit dashboard code with updated detailed analytics and visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Supply Chain Analytics Dashboard")
st.markdown("---")

# Load the preprocessed data
df = pd.read_csv("data/processed_data.csv", parse_dates=["Order Date", "Ship Date"])

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
start_date = st.sidebar.date_input("Start Date", df["Order Date"].min())
end_date = st.sidebar.date_input("End Date", df["Order Date"].max())
category = st.sidebar.selectbox("Category", ["All"] + sorted(df["Category"].dropna().unique().tolist()))

# Filter data
filtered_df = df[(df["Order Date"] >= pd.to_datetime(start_date)) & (df["Order Date"] <= pd.to_datetime(end_date))]
if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]

# Metrics
filtered_df["Lead Time"] = (filtered_df["Ship Date"] - filtered_df["Order Date"]).dt.days
total_orders = filtered_df["Order ID"].nunique()
avg_lead_time = round(filtered_df["Lead Time"].mean(), 1)
fill_rate = round(filtered_df["Quantity Delivered"].sum() / filtered_df["Quantity Ordered"].sum() * 100, 1)
inventory_turnover = round(filtered_df["Quantity Delivered"].sum() / filtered_df["Inventory"].sum(), 1)
products_at_risk = (filtered_df["Inventory"] < filtered_df["Reorder Level"]).sum()
total_products = filtered_df["Product ID"].nunique()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Orders", total_orders)
col2.metric("⏱️ Avg Lead Time", f"{avg_lead_time} days")
col3.metric("📈 Fill Rate", f"{fill_rate}%")
col4.metric("🔄 Inventory Turnover", f"{inventory_turnover}x")

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Lead Time Distribution")
    fig = px.histogram(filtered_df, x="Lead Time", nbins=20, title="Lead Time Histogram", color_discrete_sequence=["orange"])
    fig.update_layout(xaxis_title="Lead Time (Days)", yaxis_title="Number of Orders", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 Inventory Trends")
    inventory_trend = filtered_df.groupby("Order Date")["Inventory"].sum().reset_index()
    fig_inv = px.line(inventory_trend, x="Order Date", y="Inventory", markers=True, title="Inventory Over Time", line_shape="spline")
    st.plotly_chart(fig_inv, use_container_width=True)

with col2:
    st.subheader("🏷 Category Performance")
    cat_perf = filtered_df.groupby("Category")["Quantity Delivered"].sum().reset_index().sort_values(by="Quantity Delivered", ascending=False)
    fig_cat = px.bar(cat_perf, x="Category", y="Quantity Delivered", color="Quantity Delivered", title="Delivered Quantity by Category")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("📈 Fill Rate Analysis")
    filled = filtered_df["Quantity Delivered"].sum()
    unfilled = filtered_df["Quantity Ordered"].sum() - filled
    fig_pie = px.pie(names=["Filled", "Unfilled"], values=[filled, unfilled], title="Overall Fill Rate")
    st.plotly_chart(fig_pie, use_container_width=True)

# Alerts
st.subheader("🚨 Alerts & Notifications")
if products_at_risk > 0:
    st.warning(f"⚠️ {products_at_risk} products at risk of stockout")
else:
    st.success("✅ All stock levels are healthy")

# Detailed analytics
    st.markdown("---")
    st.subheader("📊 Detailed Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Performance Metrics", "📦 Inventory Analysis", "🚚 Fulfillment"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Lead Time Metrics")
            st.metric("Mean Lead Time", f"{sample_orders['Lead Time (Days)'].mean():.1f} days")
            st.metric("Median Lead Time", f"{sample_orders['Lead Time (Days)'].median():.1f} days")
            st.metric("Standard Deviation", f"{sample_orders['Lead Time (Days)'].std():.1f} days")
        
        with col2:
            st.subheader("Fill Rate Metrics")
            st.metric("Mean Fill Rate", f"{sample_inventory['fill_rate'].mean():.1%}")
            st.metric("Products at Risk", sample_inventory['stockout_risk'].sum())
            st.metric("Total Products", len(sample_inventory))
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Inventory Turnover")
            turnover_stats = sample_inventory['annualized_turnover'].describe()
            st.dataframe(turnover_stats)
        
        with col2:
            st.subheader("Stockout Risk")
            risk_count = sample_inventory['stockout_risk'].sum()
            total_count = len(sample_inventory)
            st.metric("Products at Risk", f"{risk_count} / {total_count}")
    
    with tab3:
        st.subheader("Fulfillment Performance")
        
        # Monthly trends
        sample_orders['Order Month'] = sample_orders['Order Date'].dt.to_period('M')
        monthly_lead_time = sample_orders.groupby('Order Month')['Lead Time (Days)'].mean()
        
        fig = px.line(
            x=monthly_lead_time.index.astype(str),
            y=monthly_lead_time.values,
            title="Monthly Average Lead Time"
        )
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Average Lead Time (Days)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Sidebar
    st.sidebar.header("📊 Dashboard Filters")
    
    # Date range filter
    min_date = sample_orders['Order Date'].min()
    max_date = sample_orders['Order Date'].max()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    categories = ['All'] + list(sample_orders['Category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    st.sidebar.markdown("---")
    st.sidebar.header("📈 Quick Actions")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.sidebar.button("📊 Export Report"):
        # Create a comprehensive report
        report_data = {
            'summary': {
                'total_orders': len(sample_orders),
                'avg_lead_time': sample_orders['Lead Time (Days)'].mean(),
                'fill_rate': sample_inventory['fill_rate'].mean(),
                'inventory_turnover': sample_inventory['annualized_turnover'].mean(),
                'products_at_risk': sample_inventory['stockout_risk'].sum()
            },
            'orders_data': sample_orders,
            'inventory_data': sample_inventory
        }
        
        # Create report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"supply_chain_report_{timestamp}.xlsx"
        
        # Save to Excel file
        with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([report_data['summary']])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Orders data
            report_data['orders_data'].to_excel(writer, sheet_name='Orders', index=False)
            
            # Inventory data
            report_data['inventory_data'].to_excel(writer, sheet_name='Inventory', index=False)
        
        st.success(f"📊 Report exported successfully to: {report_filename}")
        st.info(f"📁 File saved in: {os.getcwd()}")

if _name_ == "_main_":
    main()