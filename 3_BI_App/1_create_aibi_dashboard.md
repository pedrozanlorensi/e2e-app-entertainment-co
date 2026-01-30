# 📊 Create an AI/BI Dashboard

This guide walks you through creating an AI/BI Dashboard for visualizing Entertainment Co. analytics.

---

## Prerequisites

- ✅ Gold tables created via the ETL notebooks (`1_load_sheets_to_bronze_tables.py` → `2_load_silver_tables.py` → `3_load_gold_tables.py`)
- ✅ Access to Databricks SQL and AI/BI Dashboards
- ✅ A SQL Warehouse configured

---

## Step 1: Create a New AI/BI Dashboard

1. Navigate to **SQL** → **Dashboards**
2. Click **Create dashboard** → **AI/BI Dashboard**
3. Name it: `🎮 Entertainment Co. Executive Dashboard`

---

## Step 2: Connect to Gold Tables

Add these datasets to your dashboard:

| Dataset Name | Table |
|--------------|-------|
| Daily Revenue | `pedroz_catalog.entertainment_co.gold_daily_revenue` |
| Partner Performance | `pedroz_catalog.entertainment_co.gold_monthly_partner_performance` |
| IP Performance | `pedroz_catalog.entertainment_co.gold_ip_performance` |
| F&B Performance | `pedroz_catalog.entertainment_co.gold_fnb_item_performance` |
| Hourly Patterns | `pedroz_catalog.entertainment_co.gold_hourly_patterns` |

---

## Step 3: Create Visualizations

### 3.1 KPI Cards (Top Row)

Create 4 KPI cards showing:

**Card 1: Total Revenue**
```sql
SELECT 
    CONCAT('$', ROUND(SUM(total_revenue) / 1000000, 1), 'M') as value,
    'Total Revenue' as label
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025 AND month = 12
```

**Card 2: Total Visitors**
```sql
SELECT 
    CONCAT(ROUND(SUM(total_visitors) / 1000000, 2), 'M') as value,
    'Total Visitors' as label
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025 AND month = 12
```

**Card 3: Per Capita Spending**
```sql
SELECT 
    CONCAT('$', ROUND(SUM(total_revenue) / SUM(total_visitors), 2)) as value,
    'Per Capita' as label
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025 AND month = 12
```

**Card 4: Repeat Visit Rate**
```sql
SELECT 
    CONCAT(ROUND(SUM(repeat_visitors) * 100.0 / SUM(total_visitors), 1), '%') as value,
    'Repeat Rate' as label
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025 AND month = 12
```

---

### 3.2 Revenue Trend Chart

**Type**: Line Chart

```sql
SELECT 
    transaction_date,
    SUM(ticket_revenue) as Tickets,
    SUM(fnb_revenue) as "F&B",
    SUM(retail_revenue) as Retail
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025
GROUP BY transaction_date
ORDER BY transaction_date
```

**Configuration**:
- X-axis: `transaction_date`
- Y-axis: `Tickets`, `F&B`, `Retail`
- Enable stacked area view

---

### 3.3 Partner Performance Table

**Type**: Table with conditional formatting

```sql
SELECT 
    partner_name as Partner,
    market as Market,
    CONCAT('$', ROUND(total_revenue / 1000000, 2), 'M') as Revenue,
    CONCAT(ROUND(total_visitors / 1000, 0), 'K') as Visitors,
    CONCAT('$', per_capita_total) as "Per Capita",
    CONCAT(repeat_visit_rate, '%') as "Repeat Rate",
    CASE 
        WHEN per_capita_total > 50 THEN '🟢'
        WHEN per_capita_total > 40 THEN '🟡'
        ELSE '🔴'
    END as Status
FROM pedroz_catalog.entertainment_co.gold_monthly_partner_performance
WHERE year = 2025 AND month = 12
ORDER BY total_revenue DESC
```

---

### 3.4 Top IPs Bar Chart

**Type**: Horizontal Bar Chart

```sql
SELECT 
    ip_name as IP,
    ROUND(SUM(retail_revenue) / 1000000, 2) as revenue_millions
FROM pedroz_catalog.entertainment_co.gold_ip_performance
WHERE year = 2025
GROUP BY ip_name
ORDER BY revenue_millions DESC
LIMIT 7
```

**Configuration**:
- X-axis: `revenue_millions`
- Y-axis: `IP`
- Color by IP

---

### 3.5 Market Comparison Pie Chart

**Type**: Pie/Donut Chart

```sql
SELECT 
    market as Market,
    ROUND(SUM(total_revenue) / 1000000, 2) as Revenue
FROM pedroz_catalog.entertainment_co.gold_daily_revenue
WHERE year = 2025
GROUP BY market
```

---

### 3.6 Peak Hours Heatmap

**Type**: Heatmap

```sql
SELECT 
    visit_hour as Hour,
    day_type as "Day Type",
    SUM(visitors) as Visitors
FROM pedroz_catalog.entertainment_co.gold_hourly_patterns
WHERE year = 2025 AND month = 12
GROUP BY visit_hour, day_type
ORDER BY visit_hour
```

**Configuration**:
- X-axis: `Hour`
- Y-axis: `Day Type`
- Color intensity: `Visitors`

---

### 3.7 Top F&B Items

**Type**: Table

```sql
SELECT 
    item_name as Item,
    item_category as Category,
    CONCAT('$', avg_price) as Price,
    CONCAT('$', ROUND(SUM(revenue) / 1000, 0), 'K') as Revenue,
    SUM(units_sold) as "Units Sold"
FROM pedroz_catalog.entertainment_co.gold_fnb_item_performance
WHERE year = 2025
GROUP BY item_name, item_category, avg_price
ORDER BY SUM(revenue) DESC
LIMIT 10
```

---

## Step 4: Add Filters

Add these dashboard-level filters:

| Filter | Type | Column |
|--------|------|--------|
| Year | Single Select | `year` |
| Month | Multi Select | `month` |
| Market | Multi Select | `market` |
| Partner | Multi Select | `partner_name` |

---

## Step 5: Configure Layout

Suggested layout:

```
┌─────────┬─────────┬─────────┬─────────┐
│  KPI 1  │  KPI 2  │  KPI 3  │  KPI 4  │
├─────────┴─────────┴─────────┴─────────┤
│         Revenue Trend Chart           │
├──────────────────┬────────────────────┤
│  Partner Table   │   Market Pie       │
├──────────────────┼────────────────────┤
│   IP Bar Chart   │   Peak Heatmap     │
├──────────────────┴────────────────────┤
│         Top F&B Items Table           │
└───────────────────────────────────────┘
```

---

## Step 6: Enable AI Features

1. Click on **AI Assistant** icon in the dashboard
2. Enable **Natural Language Queries**
3. Users can now ask:
   - "Show me revenue by partner"
   - "What were the peak hours last week?"
   - "Compare November to December"

---

## Step 7: Schedule Refresh

1. Go to Dashboard Settings → **Refresh Schedule**
2. Set to refresh daily at 6:00 AM
3. Enable email notifications for stakeholders

---

## Step 8: Publish & Share

1. Click **Publish** to save the dashboard
2. Click **Share** to add viewers
3. Generate an embed link for the app:
   - Click **⋮** menu → **Embed**
   - Copy the iframe code

Example embed code:
```html
<iframe
  src="https://e2-demo-field-eng.cloud.databricks.com/embed/dashboardsv3/01f0e0376f8d1dceb14d5659f8f1e298?o=1444828305810485"
  width="100%"
  height="600"
  frameborder="0">
</iframe>
```

---

## 🎯 Next Steps

- Create the Databricks App with `6_create_app.md`
- Share with users via `7_sharing_with_users.md`

---

## Tips for Great Dashboards

1. **Keep it focused**: One dashboard per audience/use case
2. **KPIs at top**: Most important metrics first
3. **Consistent colors**: Use the same colors for the same dimensions
4. **Mobile-friendly**: Test on different screen sizes
5. **Context matters**: Add titles and descriptions to charts
