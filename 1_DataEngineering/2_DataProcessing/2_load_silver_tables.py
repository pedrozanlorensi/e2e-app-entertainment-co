# Databricks notebook source
# MAGIC %md
# MAGIC # 🥈 Silver Layer: Cleaned & Enriched Data
# MAGIC 
# MAGIC This notebook transforms Bronze tables into Silver tables.
# MAGIC 
# MAGIC **Medallion Architecture - Silver Layer:**
# MAGIC - Data type casting and validation
# MAGIC - Joins with dimension tables for enrichment
# MAGIC - Added calculated columns (year, month, quarter)
# MAGIC 
# MAGIC **Prerequisites:** Run `1_load_sheets_to_bronze_tables.py` first

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pedroz_catalog;
# MAGIC USE SCHEMA entertainment_co;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎫 Silver 1: Ticket Sales with Facility Info

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_ticket_sales AS
# MAGIC SELECT 
# MAGIC     t.transaction_id,
# MAGIC     CAST(t.transaction_date AS DATE) as transaction_date,
# MAGIC     t.facility_id,
# MAGIC     f.facility_name,
# MAGIC     f.partner_name,
# MAGIC     f.market,
# MAGIC     f.experience_type,
# MAGIC     t.ip_name,
# MAGIC     t.ticket_type,
# MAGIC     CAST(t.quantity AS INT) as quantity,
# MAGIC     CAST(t.unit_price AS DECIMAL(10,2)) as unit_price,
# MAGIC     CAST(t.discount_pct AS INT) as discount_pct,
# MAGIC     CAST(t.total_amount AS DECIMAL(10,2)) as total_amount,
# MAGIC     t.customer_id,
# MAGIC     CAST(t.is_repeat_visitor AS BOOLEAN) as is_repeat_visitor,
# MAGIC     CAST(t.visit_hour AS INT) as visit_hour,
# MAGIC     t.channel,
# MAGIC     YEAR(t.transaction_date) as year,
# MAGIC     MONTH(t.transaction_date) as month,
# MAGIC     QUARTER(t.transaction_date) as quarter
# MAGIC FROM bronze_ticket_sales t
# MAGIC LEFT JOIN bronze_dim_facilities f ON t.facility_id = f.facility_id;
# MAGIC 
# MAGIC SELECT 'silver_ticket_sales' as table_name, COUNT(*) as row_count FROM silver_ticket_sales;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🍔 Silver 2: F&B Sales with Facility Info

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_fnb_sales AS
# MAGIC SELECT 
# MAGIC     t.transaction_id,
# MAGIC     CAST(t.transaction_date AS DATE) as transaction_date,
# MAGIC     t.facility_id,
# MAGIC     f.facility_name,
# MAGIC     f.partner_name,
# MAGIC     f.market,
# MAGIC     t.item_name,
# MAGIC     t.item_category,
# MAGIC     CAST(t.unit_price AS DECIMAL(10,2)) as unit_price,
# MAGIC     CAST(t.quantity AS INT) as quantity,
# MAGIC     CAST(t.total_amount AS DECIMAL(10,2)) as total_amount,
# MAGIC     t.customer_id,
# MAGIC     t.outlet_id,
# MAGIC     t.payment_method,
# MAGIC     CAST(t.transaction_hour AS INT) as transaction_hour,
# MAGIC     YEAR(t.transaction_date) as year,
# MAGIC     MONTH(t.transaction_date) as month
# MAGIC FROM bronze_fnb_sales t
# MAGIC LEFT JOIN bronze_dim_facilities f ON t.facility_id = f.facility_id;
# MAGIC 
# MAGIC SELECT 'silver_fnb_sales' as table_name, COUNT(*) as row_count FROM silver_fnb_sales;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🛍️ Silver 3: Retail Sales with Facility Info

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_retail_sales AS
# MAGIC SELECT 
# MAGIC     t.transaction_id,
# MAGIC     CAST(t.transaction_date AS DATE) as transaction_date,
# MAGIC     t.facility_id,
# MAGIC     f.facility_name,
# MAGIC     f.partner_name,
# MAGIC     f.market,
# MAGIC     t.ip_name,
# MAGIC     t.product_name,
# MAGIC     t.product_category,
# MAGIC     CAST(t.unit_price AS DECIMAL(10,2)) as unit_price,
# MAGIC     CAST(t.quantity AS INT) as quantity,
# MAGIC     CAST(t.total_amount AS DECIMAL(10,2)) as total_amount,
# MAGIC     t.customer_id,
# MAGIC     t.store_id,
# MAGIC     CAST(t.is_online AS BOOLEAN) as is_online,
# MAGIC     YEAR(t.transaction_date) as year,
# MAGIC     MONTH(t.transaction_date) as month
# MAGIC FROM bronze_retail_sales t
# MAGIC LEFT JOIN bronze_dim_facilities f ON t.facility_id = f.facility_id;
# MAGIC 
# MAGIC SELECT 'silver_retail_sales' as table_name, COUNT(*) as row_count FROM silver_retail_sales;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏢 Silver 4: Facilities Dimension (cleaned)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_dim_facilities AS
# MAGIC SELECT 
# MAGIC     facility_id,
# MAGIC     facility_name,
# MAGIC     partner_name,
# MAGIC     market,
# MAGIC     country,
# MAGIC     CAST(capacity AS INT) as capacity,
# MAGIC     CAST(opened_date AS DATE) as opened_date,
# MAGIC     experience_type
# MAGIC FROM bronze_dim_facilities;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📢 Silver 5: Campaigns Dimension (cleaned)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_dim_campaigns AS
# MAGIC SELECT 
# MAGIC     campaign_id,
# MAGIC     campaign_name,
# MAGIC     CAST(start_date AS DATE) as start_date,
# MAGIC     CAST(end_date AS DATE) as end_date,
# MAGIC     CAST(budget_usd AS INT) as budget_usd,
# MAGIC     channel,
# MAGIC     target_demographic,
# MAGIC     CAST(is_active AS BOOLEAN) as is_active
# MAGIC FROM bronze_dim_campaigns;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Silver Layer Summary

# COMMAND ----------

print("""
🥈 Silver Layer Complete!

📊 Tables Created:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎫 Transactional (Enriched):
   • silver_ticket_sales
   • silver_fnb_sales
   • silver_retail_sales

📋 Dimensions (Cleaned):
   • silver_dim_facilities
   • silver_dim_campaigns

➡️ Next: Run 3_load_gold_tables.py to create Gold layer
""")
