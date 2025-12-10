# Argentina Education & Employment Analysis 🇦🇷📊

A Data Engineering and Analytics project correlating educational infrastructure with the productive matrix of Argentine provinces using official government data.

## 📌 Project Overview
This project investigates the relationship between the number of educational establishments and employment rates across different departments in Argentina. It involves a complete data pipeline from raw data ingestion to insights generation.

## ⚙️ Methodology & Pipeline
1. **ETL & Data Cleaning:** - Normalized messy datasets (CSV/Excel) from government sources using Pandas.
   - Standardized geographic codes and handled inconsistencies in department IDs (e.g., aligning CABA vs. Buenos Aires standards).
2. **Database Modeling:** - Designed a Relational Model normalized to the **Third Normal Form (3FN)** to ensure data integrity and optimize queries.
3. **Quality Assurance (GQM):** - Applied the **Goal-Question-Metric (GQM)** methodology to audit data quality, identifying and quantifying specific error rates in location codes to validate reliability.
4. **Analysis:** - Executed complex **SQL queries (DuckDB)** to aggregate employment and education metrics by region and sector.

## 🛠️ Technologies
- **Python:** Pandas, Matplotlib, Seaborn.
- **SQL:** DuckDB (for high-performance analytical queries).
- **Data Quality:** GQM Methodology.

## 📈 Key Insights
- **Employment Concentration:** A strong correlation was found between population density and employment, but educational infrastructure varies significantly by region, often independently of economic indicators.
- **Sector Analysis:** Identified specific economic sectors (CLAE6) with significantly higher female employment participation, particularly in social services and health sectors.

## 📂 Repository Structure
- `main.py`: Script performing the ETL, database creation, SQL queries, and visualization generation.
- `informe.pdf`: Full academic report including the Entity-Relationship Diagram (DER), relational schema, and detailed conclusions.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the script:
   ```bash
   python main.py
