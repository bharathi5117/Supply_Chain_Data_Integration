# Supply-Chain-Data-Integration-System
welcome to suplly chain project 

# 📦 Supply Chain Data Integration System

A real-time Python pipeline that integrates supply chain data from both Excel and API sources, processes KPIs, and visualizes results through a Streamlit dashboard.

---

## 🎯 Objective

To automate the ingestion, processing, warehousing, and visualization of supply chain data to support smarter decision-making and better operational visibility.

---

## 🛠️ Key Features

- Integration of static Excel and live API data
- Inventory simulation and KPI computation
- Google BigQuery as a cloud data warehouse
- Streamlit dashboard showing real-time metrics
- Clean modular structure for scalability

---

## 📂 Folder Structure

SUPPLY_CHAIN_PRO/
│
├── dashboard/
│ └── app.py # (Legacy or test dashboard file)
│
├── data_connectors/
│ ├── api_connector.py # Pulls product/inventory data from API
│ └── excel_connector.py # Reads static sales data from Excel
│
├── processing_files/
│ └── (Calculates metrics like lead time, fill rate, turnover)
│
├── warehousing/
│ └── (Stores processed data in BigQuery)
│
├── utils/
│ └── logger.py # Logs pipeline activity and errors
│
├── config.py # Holds constants, API keys, and BQ settings
├── main.py # Orchestrates the pipeline: extract → transform → load
├── output.py # Streamlit dashboard app
├── requirements.txt # Project dependencies
├── README.md # Documentation
├── .gitignore # Files to exclude from Git
├── 05 Supply Chain Data... # Excel dataset (Global Superstore)
├── supply_chain_report_... # Possibly generated reports


---

## ⚙️ Technologies Used

| Area             | Tools / Libraries          |
|------------------|-----------------------------|
| Language         | Python                      |
| Data Processing  | Pandas, NumPy               |
| API Access       | Requests                    |
| Excel Handling   | OpenPyXL                    |
| Dashboard        | Streamlit, Plotly           |
| Cloud Storage    | Google BigQuery             |
| Logging          | logging module              |
| Env Management   | python-dotenv               |

---

## 🚀 How to Run

### 1. Install dependencies

pip install -r requirements.txt
2. Run the data pipeline

python main.py
3. Launch the Streamlit dashboard
 -m streamlit run output.py

 
📊 Dataset
Source: Sales Forecasting Dataset - Kaggle

Static data: Global Superstore Excel (~9,800 rows, 2011–2014)

Dynamic data: Live product/inventory data from Fake Store API

🔮 Future Enhancements
Add ML-based demand forecasting

Alert system for low inventory (SMS/Email)

Automate pipeline using Airflow or Prefect

More APIs for supplier/shipping metrics

👤 Author
Nadigeni Bharathi
🗓️ August 2025
