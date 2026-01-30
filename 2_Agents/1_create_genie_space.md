# 🧞 Create a Genie Space for Data Queries

This guide walks you through creating a Genie space that allows business users to query the gold-level tables using natural language.

---

## Prerequisites

- ✅ Run the ETL notebooks (`1_load_sheets_to_bronze_tables.py` → `2_load_silver_tables.py` → `3_load_gold_tables.py`) to create the gold tables
- ✅ Databricks workspace with Genie enabled
- ✅ Permissions to create Genie spaces

---

## Step 1: Create a New Genie Space

1. Navigate to **Genie** in the left sidebar
2. Click **New** → **Genie space**
3. Configure:
   - **Name**: `🎮 Entertainment Co. Analytics`
   - **Description**: `Ask questions about ticket sales, F&B revenue, retail performance, and visitor analytics across all facilities and partners.`

---

## Step 2: Add Tables to the Genie Space

Add these gold-level tables:

| Table | Description |
|-------|-------------|
| `pedroz_catalog.entertainment_co.gold_daily_revenue` | Daily revenue by facility |
| `pedroz_catalog.entertainment_co.gold_monthly_partner_performance` | Monthly partner KPIs |
| `pedroz_catalog.entertainment_co.gold_ip_performance` | IP/franchise performance |
| `pedroz_catalog.entertainment_co.gold_fnb_item_performance` | F&B item analytics |
| `pedroz_catalog.entertainment_co.gold_hourly_patterns` | Peak time analysis |

---

## Step 3: Add Genie Instructions

Copy and paste these instructions into the Genie space settings:

```
# Entertainment Co. Analytics Assistant

You help business users analyze entertainment facility performance data.

## Key Metrics
- **Total Revenue**: Sum of ticket + F&B + retail revenue
- **Per Capita**: Revenue divided by total visitors
- **Repeat Visit Rate**: (Repeat visitors / Total visitors) × 100

## Time Period Comparisons
- PY = Prior Year (same period last year)
- PM = Prior Month (previous month)
- PQ = Prior Quarter (previous quarter)

## Business Context
- Partners are licensees who operate facilities
- IP refers to toy brand franchises (RoboBuddies, MagicPonies, etc.)
- Markets: North_America, Europe, Asia_Pacific

## Common Questions Format
When asked about "top" items, default to top 10.
When comparing periods, show both values and % change.
Always include the market dimension when relevant.

## Data Freshness
Data is updated monthly.
```

---

## Step 4: Add Sample SQL Queries

Add these certified queries to help users and improve Genie responses:

### Query 1: Total Revenue by Partner (Monthly)
```sql
-- Monthly revenue breakdown by partner
SELECT 
    year,
    month,
    partner_name,
    ROUND(ticket_revenue / 1000000, 2) as ticket_revenue_M,
    ROUND(fnb_revenue / 1000000, 2) as fnb_revenue_M,
    ROUND(retail_revenue / 1000000, 2) as retail_revenue_M,
    ROUND(total_revenue / 1000000, 2) as total_revenue_M,
    total_visitors,
    per_capita_total
FROM pedroz_catalog.entertainment_co.gold_monthly_partner_performance
ORDER BY year, month, total_revenue DESC
```

### Query 2: Top Performing IPs
```sql
-- IP performance ranking
SELECT 
    ip_name,
    market,
    ROUND(SUM(retail_revenue) / 1000000, 2) as total_revenue_M,
    SUM(units_sold) as total_units,
    ROUND(AVG(avg_unit_price), 2) as avg_price
FROM pedroz_catalog.entertainment_co.gold_ip_performance
GROUP BY ip_name, market
ORDER BY total_revenue_M DESC
LIMIT 10
```

### Query 3: Top F&B Items by Revenue
```sql
-- Best selling F&B items
SELECT 
    item_name,
    item_category,
    ROUND(SUM(revenue), 2) as total_revenue,
    SUM(units_sold) as total_units,
    avg_price
FROM pedroz_catalog.entertainment_co.gold_fnb_item_performance
GROUP BY item_name, item_category, avg_price
ORDER BY total_revenue DESC
LIMIT 10
```

### Query 4: Peak Hours Analysis
```sql
-- Busiest hours by facility
SELECT 
    facility_name,
    visit_hour,
    day_type,
    SUM(visitors) as total_visitors,
    ROUND(SUM(revenue), 2) as total_revenue
FROM pedroz_catalog.entertainment_co.gold_hourly_patterns
GROUP BY facility_name, visit_hour, day_type
ORDER BY facility_name, total_visitors DESC
```

### Query 5: Month-over-Month Comparison
```sql
-- MoM revenue comparison by partner
WITH current_month AS (
    SELECT partner_name, total_revenue, total_visitors
    FROM pedroz_catalog.entertainment_co.gold_monthly_partner_performance
    WHERE year = 2025 AND month = 12
),
prior_month AS (
    SELECT partner_name, total_revenue, total_visitors
    FROM pedroz_catalog.entertainment_co.gold_monthly_partner_performance
    WHERE year = 2025 AND month = 11
)
SELECT 
    c.partner_name,
    ROUND(c.total_revenue / 1000000, 2) as current_revenue_M,
    ROUND(p.total_revenue / 1000000, 2) as prior_revenue_M,
    ROUND((c.total_revenue - p.total_revenue) / p.total_revenue * 100, 1) as revenue_change_pct,
    c.total_visitors as current_visitors,
    p.total_visitors as prior_visitors
FROM current_month c
JOIN prior_month p ON c.partner_name = p.partner_name
ORDER BY revenue_change_pct DESC
```

### Query 6: Like-for-Like Market Comparison
```sql
-- Compare similar experience types across markets
SELECT 
    g.market,
    f.experience_type,
    COUNT(DISTINCT g.facility_id) as facility_count,
    ROUND(SUM(g.total_revenue) / 1000000, 2) as total_revenue_M,
    ROUND(AVG(g.total_revenue / NULLIF(g.total_visitors, 0)), 2) as avg_per_capita
FROM pedroz_catalog.entertainment_co.gold_daily_revenue g
JOIN pedroz_catalog.entertainment_co.silver_dim_facilities f 
    ON g.facility_id = f.facility_id
GROUP BY g.market, f.experience_type
ORDER BY total_revenue_M DESC
```

---

## Step 5: Test the Genie Space

Try these natural language questions:

1. **"What was the total revenue last month?"**
2. **"Which partner had the highest per capita spending?"**
3. **"Compare F&B revenue between North America and Europe"**
4. **"What are the top 5 performing IPs by retail revenue?"**
5. **"Show me peak visiting hours for DreamWorld parks"**
6. **"How did November compare to October across all partners?"**
7. **"Which F&B items have the highest revenue? Include prices."**
8. **"What is the repeat visitor rate by market?"**

---

## Step 6: Share the Genie Space

1. Click the **Share** button in the Genie space
2. Add users or groups who need access
3. Set permissions:
   - **Can query**: For business users
   - **Can edit**: For data team members

---

## 🎯 Next Steps

- Proceed to `4_create_multi_agent.md` to create a multi-agent orchestrator
- Use `5_create_aibi_dashboard.md` to build visualizations

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Genie can't find tables | Verify table permissions in Unity Catalog |
| Incorrect results | Add more sample queries to guide Genie |
| Slow responses | Check warehouse size and scaling |
| Missing context | Enhance the instructions section |
