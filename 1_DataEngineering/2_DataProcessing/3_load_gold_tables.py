# Databricks notebook source
# MAGIC %md
# MAGIC # 🥇 Gold Layer: Aggregated & Business-Ready
# MAGIC 
# MAGIC This notebook transforms Silver tables into Gold tables.
# MAGIC 
# MAGIC **Medallion Architecture - Gold Layer:**
# MAGIC - Aggregated metrics for reporting
# MAGIC - Business-ready tables for Genie and Dashboards
# MAGIC - AI_FORECAST for revenue predictions
# MAGIC 
# MAGIC **Prerequisites:** Run `2_load_silver_tables.py` first

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG pedroz_catalog;
# MAGIC USE SCHEMA entertainment_co;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Gold 1: Daily Revenue Summary by Facility

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_daily_revenue AS
# MAGIC SELECT 
# MAGIC     COALESCE(t.transaction_date, f.transaction_date, r.transaction_date) as transaction_date,
# MAGIC     COALESCE(t.facility_id, f.facility_id, r.facility_id) as facility_id,
# MAGIC     COALESCE(t.facility_name, f.facility_name, r.facility_name) as facility_name,
# MAGIC     COALESCE(t.partner_name, f.partner_name, r.partner_name) as partner_name,
# MAGIC     COALESCE(t.market, f.market, r.market) as market,
# MAGIC     COALESCE(t.ticket_revenue, 0) as ticket_revenue,
# MAGIC     COALESCE(t.ticket_transactions, 0) as ticket_transactions,
# MAGIC     COALESCE(t.total_visitors, 0) as total_visitors,
# MAGIC     COALESCE(t.repeat_visitors, 0) as repeat_visitors,
# MAGIC     COALESCE(f.fnb_revenue, 0) as fnb_revenue,
# MAGIC     COALESCE(f.fnb_transactions, 0) as fnb_transactions,
# MAGIC     COALESCE(r.retail_revenue, 0) as retail_revenue,
# MAGIC     COALESCE(r.retail_transactions, 0) as retail_transactions,
# MAGIC     (COALESCE(t.ticket_revenue, 0) + COALESCE(f.fnb_revenue, 0) + COALESCE(r.retail_revenue, 0)) as total_revenue,
# MAGIC     YEAR(COALESCE(t.transaction_date, f.transaction_date, r.transaction_date)) as year,
# MAGIC     MONTH(COALESCE(t.transaction_date, f.transaction_date, r.transaction_date)) as month
# MAGIC FROM (
# MAGIC     SELECT 
# MAGIC         transaction_date, facility_id, facility_name, partner_name, market,
# MAGIC         SUM(total_amount) as ticket_revenue,
# MAGIC         COUNT(*) as ticket_transactions,
# MAGIC         SUM(quantity) as total_visitors,
# MAGIC         SUM(CASE WHEN is_repeat_visitor THEN quantity ELSE 0 END) as repeat_visitors
# MAGIC     FROM silver_ticket_sales
# MAGIC     GROUP BY transaction_date, facility_id, facility_name, partner_name, market
# MAGIC ) t
# MAGIC FULL OUTER JOIN (
# MAGIC     SELECT 
# MAGIC         transaction_date, facility_id, facility_name, partner_name, market,
# MAGIC         SUM(total_amount) as fnb_revenue,
# MAGIC         COUNT(*) as fnb_transactions
# MAGIC     FROM silver_fnb_sales
# MAGIC     GROUP BY transaction_date, facility_id, facility_name, partner_name, market
# MAGIC ) f ON t.transaction_date = f.transaction_date AND t.facility_id = f.facility_id
# MAGIC FULL OUTER JOIN (
# MAGIC     SELECT 
# MAGIC         transaction_date, facility_id, facility_name, partner_name, market,
# MAGIC         SUM(total_amount) as retail_revenue,
# MAGIC         COUNT(*) as retail_transactions
# MAGIC     FROM silver_retail_sales
# MAGIC     GROUP BY transaction_date, facility_id, facility_name, partner_name, market
# MAGIC ) r ON COALESCE(t.transaction_date, f.transaction_date) = r.transaction_date 
# MAGIC        AND COALESCE(t.facility_id, f.facility_id) = r.facility_id;
# MAGIC 
# MAGIC SELECT 'gold_daily_revenue' as table_name, COUNT(*) as row_count FROM gold_daily_revenue;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📈 Gold 2: Monthly Partner Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_monthly_partner_performance AS
# MAGIC SELECT 
# MAGIC     year,
# MAGIC     month,
# MAGIC     partner_name,
# MAGIC     market,
# MAGIC     SUM(ticket_revenue) as ticket_revenue,
# MAGIC     SUM(fnb_revenue) as fnb_revenue,
# MAGIC     SUM(retail_revenue) as retail_revenue,
# MAGIC     SUM(total_revenue) as total_revenue,
# MAGIC     SUM(total_visitors) as total_visitors,
# MAGIC     SUM(repeat_visitors) as repeat_visitors,
# MAGIC     ROUND(SUM(repeat_visitors) * 100.0 / NULLIF(SUM(total_visitors), 0), 2) as repeat_visit_rate,
# MAGIC     ROUND(SUM(total_revenue) / NULLIF(SUM(total_visitors), 0), 2) as per_capita_total,
# MAGIC     ROUND(SUM(fnb_revenue) / NULLIF(SUM(total_visitors), 0), 2) as per_capita_fnb,
# MAGIC     ROUND(SUM(retail_revenue) / NULLIF(SUM(total_visitors), 0), 2) as per_capita_retail,
# MAGIC     COUNT(DISTINCT facility_id) as facility_count
# MAGIC FROM gold_daily_revenue
# MAGIC GROUP BY year, month, partner_name, market
# MAGIC ORDER BY year, month, partner_name;
# MAGIC 
# MAGIC SELECT 'gold_monthly_partner_performance' as table_name, COUNT(*) as row_count FROM gold_monthly_partner_performance;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎮 Gold 3: IP Performance Summary

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_ip_performance AS
# MAGIC SELECT 
# MAGIC     ip_name,
# MAGIC     market,
# MAGIC     year,
# MAGIC     month,
# MAGIC     SUM(total_amount) as retail_revenue,
# MAGIC     COUNT(*) as transactions,
# MAGIC     SUM(quantity) as units_sold,
# MAGIC     ROUND(AVG(unit_price), 2) as avg_unit_price,
# MAGIC     COUNT(DISTINCT facility_id) as facilities_with_sales
# MAGIC FROM silver_retail_sales
# MAGIC GROUP BY ip_name, market, year, month
# MAGIC ORDER BY year, month, retail_revenue DESC;
# MAGIC 
# MAGIC SELECT 'gold_ip_performance' as table_name, COUNT(*) as row_count FROM gold_ip_performance;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🍔 Gold 4: Top F&B Items Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_fnb_item_performance AS
# MAGIC SELECT 
# MAGIC     item_name,
# MAGIC     item_category,
# MAGIC     market,
# MAGIC     year,
# MAGIC     month,
# MAGIC     SUM(total_amount) as revenue,
# MAGIC     COUNT(*) as transactions,
# MAGIC     SUM(quantity) as units_sold,
# MAGIC     ROUND(AVG(unit_price), 2) as avg_price,
# MAGIC     COUNT(DISTINCT facility_id) as facilities_with_sales
# MAGIC FROM silver_fnb_sales
# MAGIC GROUP BY item_name, item_category, market, year, month
# MAGIC ORDER BY year, month, revenue DESC;
# MAGIC 
# MAGIC SELECT 'gold_fnb_item_performance' as table_name, COUNT(*) as row_count FROM gold_fnb_item_performance;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⏰ Gold 5: Hourly Traffic Patterns (Peak Time Analysis)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_hourly_patterns AS
# MAGIC SELECT 
# MAGIC     facility_id,
# MAGIC     facility_name,
# MAGIC     partner_name,
# MAGIC     market,
# MAGIC     visit_hour,
# MAGIC     DAYOFWEEK(transaction_date) as day_of_week,
# MAGIC     CASE WHEN DAYOFWEEK(transaction_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END as day_type,
# MAGIC     year,
# MAGIC     month,
# MAGIC     COUNT(*) as transactions,
# MAGIC     SUM(quantity) as visitors,
# MAGIC     SUM(total_amount) as revenue
# MAGIC FROM silver_ticket_sales
# MAGIC GROUP BY facility_id, facility_name, partner_name, market, visit_hour, 
# MAGIC          DAYOFWEEK(transaction_date), year, month
# MAGIC ORDER BY facility_id, visit_hour;
# MAGIC 
# MAGIC SELECT 'gold_hourly_patterns' as table_name, COUNT(*) as row_count FROM gold_hourly_patterns;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔮 Revenue Forecasting with AI_FORECAST

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Step 1: Create base table for forecasting (by partner)
# MAGIC CREATE OR REPLACE TABLE gold_daily_revenue_ts AS
# MAGIC SELECT 
# MAGIC     transaction_date,
# MAGIC     partner_name,
# MAGIC     SUM(total_revenue) as total_revenue
# MAGIC FROM gold_daily_revenue
# MAGIC GROUP BY transaction_date, partner_name
# MAGIC ORDER BY partner_name, transaction_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Step 2: Generate 30-day forecast by partner
# MAGIC CREATE OR REPLACE TABLE gold_revenue_forecast AS
# MAGIC SELECT * FROM AI_FORECAST(
# MAGIC     TABLE(gold_daily_revenue_ts),
# MAGIC     horizon => DATE_ADD(CURRENT_DATE(), 30),
# MAGIC     time_col => 'transaction_date',
# MAGIC     value_col => 'total_revenue',
# MAGIC     group_col => 'partner_name'
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Gold Layer Summary

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Display all tables created
# MAGIC SHOW TABLES IN pedroz_catalog.entertainment_co;

# COMMAND ----------

print("""
🥇 Gold Layer Complete!

📊 Tables Created:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Business Aggregations:
   • gold_daily_revenue
   • gold_monthly_partner_performance
   • gold_ip_performance
   • gold_fnb_item_performance
   • gold_hourly_patterns

🔮 Forecasting:
   • gold_revenue_forecast

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 ETL Pipeline Complete!

Full Medallion Architecture:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥉 BRONZE (Raw):
   • bronze_ticket_sales
   • bronze_fnb_sales
   • bronze_retail_sales
   • bronze_dim_facilities
   • bronze_dim_campaigns
   • bronze_dim_customers
   • bronze_dim_dates

🥈 SILVER (Cleaned & Enriched):
   • silver_ticket_sales
   • silver_fnb_sales
   • silver_retail_sales
   • silver_dim_facilities
   • silver_dim_campaigns

🥇 GOLD (Aggregated & Business-Ready):
   • gold_daily_revenue
   • gold_monthly_partner_performance
   • gold_ip_performance
   • gold_fnb_item_performance
   • gold_hourly_patterns
   • gold_revenue_forecast

✅ Ready for Genie Space and Dashboard creation!
""")
