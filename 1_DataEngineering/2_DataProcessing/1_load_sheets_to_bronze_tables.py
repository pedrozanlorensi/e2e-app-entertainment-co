# Databricks notebook source
# MAGIC %md
# MAGIC # 🥉 Bronze Layer: Raw Data Ingestion
# MAGIC 
# MAGIC This notebook ingests raw CSV files from the Volume into Bronze tables.
# MAGIC 
# MAGIC **Medallion Architecture - Bronze Layer:**
# MAGIC - Raw data ingestion from CSV files
# MAGIC - Adds metadata (source file, ingestion timestamp)
# MAGIC - No transformations applied

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pedroz_catalog;
# MAGIC USE SCHEMA entertainment_co;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📦 Ingest Transactional Data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze: Ticket Sales (all partners, all months)
# MAGIC CREATE OR REPLACE TABLE bronze_ticket_sales AS
# MAGIC SELECT 
# MAGIC     *,
# MAGIC     _metadata.file_path as source_file,
# MAGIC     current_timestamp() as ingestion_timestamp
# MAGIC FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/partners/*/ticket_sales_*.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC SELECT 'bronze_ticket_sales' as table_name, COUNT(*) as row_count FROM bronze_ticket_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze: F&B Sales
# MAGIC CREATE OR REPLACE TABLE bronze_fnb_sales AS
# MAGIC SELECT 
# MAGIC     *,
# MAGIC     _metadata.file_path as source_file,
# MAGIC     current_timestamp() as ingestion_timestamp
# MAGIC FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/partners/*/fnb_sales_*.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC SELECT 'bronze_fnb_sales' as table_name, COUNT(*) as row_count FROM bronze_fnb_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze: Retail Sales
# MAGIC CREATE OR REPLACE TABLE bronze_retail_sales AS
# MAGIC SELECT 
# MAGIC     *,
# MAGIC     _metadata.file_path as source_file,
# MAGIC     current_timestamp() as ingestion_timestamp
# MAGIC FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/partners/*/retail_sales_*.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC SELECT 'bronze_retail_sales' as table_name, COUNT(*) as row_count FROM bronze_retail_sales;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📦 Ingest Dimension Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze: Dimension Tables
# MAGIC CREATE OR REPLACE TABLE bronze_dim_facilities AS
# MAGIC SELECT * FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/dimensions/dim_facilities.csv',
# MAGIC     format => 'csv', header => true, inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE bronze_dim_campaigns AS
# MAGIC SELECT * FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/dimensions/dim_campaigns.csv',
# MAGIC     format => 'csv', header => true, inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE bronze_dim_customers AS
# MAGIC SELECT * FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/dimensions/dim_customers.csv',
# MAGIC     format => 'csv', header => true, inferSchema => true
# MAGIC );
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE bronze_dim_dates AS
# MAGIC SELECT * FROM read_files(
# MAGIC     '/Volumes/pedroz_catalog/entertainment_co/raw_files/dimensions/dim_dates.csv',
# MAGIC     format => 'csv', header => true, inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Bronze Layer Summary

# COMMAND ----------

print("""
🥉 Bronze Layer Complete!

📊 Tables Created:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎫 Transactional:
   • bronze_ticket_sales
   • bronze_fnb_sales
   • bronze_retail_sales

📋 Dimensions:
   • bronze_dim_facilities
   • bronze_dim_campaigns
   • bronze_dim_customers
   • bronze_dim_dates

➡️ Next: Run 2_load_silver_tables.py to create Silver layer
""")
