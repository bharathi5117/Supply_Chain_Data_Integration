import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load processed data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_data.csv", parse_dates=["Order Date", "Ship Date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Dashboard Filters")
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

categories = ["All"] + sorted(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("Category", categories)

# Apply filters
mask = (df["Order Date"] >= pd.to_datetime(date_range[0])) & (df["Order Date"] <= pd.to_datetime(date_range[1]))
if selected_category != "All":
    mask &= (df["Category"] == selected_category)
df_filtered = df[mask]

# Quick summary metrics
st.markdown("## 📊 Supply Chain Analytics Dashboard")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Orders", f"{df_filtered['Order ID'].nunique()}")
lead_times = (df_filtered["Ship Date"] - df_filtered["Order Date"]).dt.days
total_fill_rate = df_filtered["Fill Rate"].mean()
col2.metric("⏱️ Avg Lead Time", f"{lead_times.mean():.1f} days")
col3.metric("📈 Fill Rate", f"{total_fill_rate:.1f}%")
col4.metric("🔄 Inventory Turnover", f"{df_filtered['Inventory Turnover'].mean():.1f}x")

# Lead Time Boxplot by Region
st.subheader("📦 Lead Time by Region")
fig_box = px.box(df_filtered, x="Region", y=lead_times, color="Region", points="all", title="Lead Time Distribution by Region")
st.plotly_chart(fig_box, use_container_width=True)

# Inventory Trends Over Time (Area Chart)
st.subheader("📉 Inventory Trends Over Time")
df_time = df_filtered.groupby("Order Date")["Inventory Level"].mean().reset_index()
fig_area = px.area(df_time, x="Order Date", y="Inventory Level", title="Average Inventory Level Over Time")
st.plotly_chart(fig_area, use_container_width=True)

# Category-wise Fill Rate Comparison (Donut Chart)
st.subheader("🏷️ Category Fill Rate Comparison")
df_category = df_filtered.groupby("Category")["Fill Rate"].mean().reset_index()
fig_donut = go.Figure(data=[
    go.Pie(labels=df_category["Category"], values=df_category["Fill Rate"], hole=0.5)
])
fig_donut.update_layout(title="Average Fill Rate by Category")
st.plotly_chart(fig_donut, use_container_width=True)

# Alerts and Notifications
st.subheader("🚨 Alerts & Notifications")
products_at_risk = df_filtered[df_filtered["Stock Level"] < df_filtered["Reorder Point"]]["Product ID"].nunique()
st.warning(f"⚠️ {products_at_risk} products at risk of stockout")

# Detailed Analytics Tabs
st.subheader("📊 Detailed Analytics")
tabs = st.tabs(["📈 Performance Metrics", "📦 Inventory Analysis", "🚚 Fulfillment"])

# Tab 1: Performance Metrics
with tabs[0]:
    st.markdown("### 🔍 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Lead Time", f"{lead_times.mean():.1f} days")
    col2.metric("Median Lead Time", f"{lead_times.median():.1f} days")
    col3.metric("Standard Deviation", f"{lead_times.std():.1f} days")

    col4, col5, col6 = st.columns(3)
    col4.metric("Mean Fill Rate", f"{df_filtered['Fill Rate'].mean():.1f}%")
    col5.metric("Products at Risk", f"{products_at_risk}")
    col6.metric("Total Products", f"{df_filtered['Product ID'].nunique()}")

# Tab 2: Inventory Analysis
with tabs[1]:
    st.markdown("### 📦 Inventory Movement by Sub-Category")
    fig_bar = px.bar(df_filtered, x="Sub-Category", y="Inventory Level", color="Sub-Category",
                    title="Inventory Levels by Sub-Category", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 3: Fulfillment
with tabs[2]:
    st.markdown("### 🚚 Lead Time Trends")
    df_lead = df_filtered.copy()
    df_lead["Lead Time"] = (df_lead["Ship Date"] - df_lead["Order Date"]).dt.days
    df_lead = df_lead.groupby("Order Date")["Lead Time"].mean().reset_index()
    fig_line = px.line(df_lead, x="Order Date", y="Lead Time", title="Average Lead Time Over Time")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### 🔁 Reorder Alert Products")
    alert_df = df_filtered[df_filtered["Stock Level"] < df_filtered["Reorder Point"]][["Product ID", "Product Name", "Stock Level", "Reorder Point"]].drop_duplicates()
    st.dataframe(alert_df, use_container_width=True)

# Optional export/download button
st.sidebar.markdown("---")
st.sidebar.download_button("Download Filtered Data", data=df_filtered.to_csv(index=False), file_name="filtered_data.csv")
