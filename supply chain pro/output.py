#!/usr/bin/env python3
"""
Streamlit Supply Chain Dashboard with updated chart types and colors
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

def main():
    st.set_page_config(
        page_title="SUPPLY CHAIN DASHBOARD",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 SUPPLY CHAIN DASHBOARD")
    st.markdown("---")

    # Sample Data
    sample_orders = pd.DataFrame({
        'Order ID': [f'ORD_{i:03d}' for i in range(1, 101)],
        'Order Date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'Ship Date': pd.date_range('2024-01-03', periods=100, freq='D'),
        'Customer ID': [f'CUST_{i%20:02d}' for i in range(1, 101)],
        'Product ID': [f'PROD_{i%10:02d}' for i in range(1, 101)],
        'Category': ['Electronics', 'Clothing', 'Home', 'Sports'] * 25,
        'Quantity': np.random.randint(1, 10, 100),
        'Sales': np.random.uniform(100, 1000, 100),
        'Profit': np.random.uniform(10, 200, 100),
        'Lead Time (Days)': np.random.randint(1, 15, 100)
    })

    num_inventory_records = 300
    sample_inventory = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30, freq='D').repeat(num_inventory_records // 30),
        'product_id': [f'PROD_{i%10:02d}' for i in range(1, num_inventory_records + 1)],
        'category': ['Electronics', 'Clothing', 'Home', 'Sports'] * (num_inventory_records // 4),
        'stock_level': np.random.randint(10, 200, num_inventory_records),
        'daily_demand': np.random.randint(1, 10, num_inventory_records),
        'fill_rate': np.random.uniform(0.7, 1.0, num_inventory_records),
        'annualized_turnover': np.random.uniform(2, 12, num_inventory_records),
        'stockout_risk': np.random.choice([True, False], num_inventory_records, p=[0.1, 0.9])
    })

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Orders", len(sample_orders))
    col2.metric("⏱️ Average Lead Time", f"{sample_orders['Lead Time (Days)'].mean():.1f} days")
    col3.metric("📈 Fill Rate", f"{sample_inventory['fill_rate'].mean():.1%}")
    col4.metric("🔄 Turnover of Inventory", f"{sample_inventory['annualized_turnover'].mean():.1f}x")

    st.markdown("---")

    # Charts Section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Lead Time Distribution (Bar Chart)")
        lead_time_counts = sample_orders['Lead Time (Days)'].value_counts().sort_index()
        fig = px.bar(
            x=lead_time_counts.index,
            y=lead_time_counts.values,
            labels={'x': 'Lead Time (Days)', 'y': 'Number of Orders'},
            title="Lead Time Distribution",
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📦 Inventory Trends (Area Chart)")
        daily_inventory = sample_inventory.groupby(['date', 'category']).agg({
            'stock_level': 'mean',
            'daily_demand': 'mean'
        }).reset_index()
        fig = px.area(
            daily_inventory,
            x='date',
            y='stock_level',
            color='category',
            title="Daily Stock Levels by Category",
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🏷️ Category Performance (Scatter Plot)")
        category_sales = sample_orders.groupby('Category').agg({
            'Sales': 'sum',
            'Order ID': 'count'
        }).reset_index()
        fig = px.scatter(
            category_sales,
            x='Category',
            y='Sales',
            size='Sales',
            color='Category',
            title="Sales by Category",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 Fill Rate Analysis (Scatter Plot)")
        fill_rate_by_category = sample_inventory.groupby('category')['fill_rate'].mean().reset_index()
        fig = px.scatter(
            fill_rate_by_category,
            x='category',
            y='fill_rate',
            size='fill_rate',
            color='category',
            title="Average Fill Rate by Category",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Fill Rate",
            yaxis_tickformat='.1%'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Alerts
    st.subheader("🚨 Alerts & Notifications")
    alerts = []
    if sample_inventory['stockout_risk'].sum() > 0:
        alerts.append(f"⚠️ {sample_inventory['stockout_risk'].sum()} products at risk of stockout")
    if (sample_orders['Lead Time (Days)'] > 14).sum() > 0:
        alerts.append(f"⚠️ {(sample_orders['Lead Time (Days)'] > 14).sum()} orders with lead time > 14 days")
    if alerts:
        for a in alerts:
            st.warning(a)
    else:
        st.success("✅ All systems operating normally")

    # Tabs
    st.markdown("---")
    st.subheader("📊 Detailed Analytics")
    tab1, tab2, tab3 = st.tabs(["📈 Performance Metrics", "📦 Inventory Analysis", "🚚 Fulfillment"])

    with tab1:
        c1, c2 = st.columns(2)
        c1.metric("Mean Lead Time", f"{sample_orders['Lead Time (Days)'].mean():.1f} days")
        c1.metric("Median Lead Time", f"{sample_orders['Lead Time (Days)'].median():.1f} days")
        c1.metric("Std Dev", f"{sample_orders['Lead Time (Days)'].std():.1f} days")
        c2.metric("Mean Fill Rate", f"{sample_inventory['fill_rate'].mean():.1%}")
        c2.metric("Products at Risk", sample_inventory['stockout_risk'].sum())
        c2.metric("Total Products", len(sample_inventory))

    with tab2:
        c1, c2 = st.columns(2)
        c1.subheader("Inventory Turnover")
        st.dataframe(sample_inventory['annualized_turnover'].describe())
        c2.metric("Products at Risk", f"{sample_inventory['stockout_risk'].sum()} / {len(sample_inventory)}")

    with tab3:
        st.subheader("Fulfillment Performance")
        sample_orders['Order Month'] = sample_orders['Order Date'].dt.to_period('M')
        monthly_lead_time = sample_orders.groupby('Order Month')['Lead Time (Days)'].mean()
        fig = px.line(
            x=monthly_lead_time.index.astype(str),
            y=monthly_lead_time.values,
            title="Monthly Average Lead Time",
            labels={'x': 'Month', 'y': 'Average Lead Time (Days)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Sidebar
    st.sidebar.header("📊 Dashboard Filters")
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(sample_orders['Order Date'].min(), sample_orders['Order Date'].max())
    )
    category_filter = st.sidebar.selectbox("Category", ['All'] + list(sample_orders['Category'].unique()))

    st.sidebar.markdown("---")
    st.sidebar.header("📈 Quick Actions")
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    if st.sidebar.button("📊 Export Report"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"supply_chain_report_{timestamp}.xlsx"
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            pd.DataFrame([{
                'Total Orders': len(sample_orders),
                'Avg Lead Time': sample_orders['Lead Time (Days)'].mean(),
                'Fill Rate': sample_inventory['fill_rate'].mean(),
                'Inventory Turnover': sample_inventory['annualized_turnover'].mean(),
                'Products at Risk': sample_inventory['stockout_risk'].sum()
            }]).to_excel(writer, sheet_name='Summary', index=False)
            sample_orders.to_excel(writer, sheet_name='Orders', index=False)
            sample_inventory.to_excel(writer, sheet_name='Inventory', index=False)
        st.success(f"📊 Report exported: {filename}")
        st.info(f"📁 File saved at: {os.getcwd()}")

if __name__ == "__main__":
    main()
