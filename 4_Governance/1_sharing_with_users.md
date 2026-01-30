# 👥 Sharing with End Users

This guide explains how to share your apps, dashboards, and data with end users in the simplest way possible.

---

## 🎯 Key Principle: Unity Catalog is Your Friend

Unity Catalog provides a **single, unified governance layer** for all your data assets. Instead of managing permissions in multiple places, everything flows through Unity Catalog.

```
Unity Catalog
    └── pedroz_catalog
        └── entertainment_co (schema)
            ├── Tables (gold_*, silver_*)
            ├── Volumes (raw_files)
            ├── Models (if any)
            └── Functions
```

---

## 1️⃣ Sharing Tables

### Grant Access to Specific Tables

```sql
-- Grant SELECT on gold tables to a group
GRANT SELECT ON TABLE pedroz_catalog.entertainment_co.gold_daily_revenue 
TO `analytics_users`;

GRANT SELECT ON TABLE pedroz_catalog.entertainment_co.gold_monthly_partner_performance 
TO `analytics_users`;

-- Or grant on all tables in schema
GRANT SELECT ON SCHEMA pedroz_catalog.entertainment_co 
TO `analytics_users`;
```

### Create Views for Simplified Access

```sql
-- Create a simplified view for business users
CREATE OR REPLACE VIEW pedroz_catalog.entertainment_co.v_executive_summary AS
SELECT 
    partner_name,
    market,
    ROUND(total_revenue / 1000000, 2) as revenue_millions,
    total_visitors,
    per_capita_total,
    repeat_visit_rate
FROM pedroz_catalog.entertainment_co.gold_monthly_partner_performance
WHERE year = YEAR(CURRENT_DATE());

-- Grant access to the view
GRANT SELECT ON VIEW pedroz_catalog.entertainment_co.v_executive_summary 
TO `executives`;
```

---

## 2️⃣ Sharing Dashboards

### Direct Sharing

1. Open the dashboard
2. Click **Share** button
3. Add users/groups:
   - **Can view**: See the dashboard
   - **Can edit**: Modify the dashboard
   - **Can manage**: Full control

### Embed in External Sites

1. Click **⋮** menu → **Embed**
2. Copy the iframe code:
```html
<iframe
  src="https://your-workspace.cloud.databricks.com/embed/dashboardsv3/YOUR_DASHBOARD_ID"
  width="100%"
  height="600"
  frameborder="0">
</iframe>
```
3. Paste into your internal portal or app

### Scheduled Email Reports

1. Dashboard → **Schedule**
2. Set frequency (daily, weekly, monthly)
3. Add recipients
4. Choose format (PDF, image)

---

## 3️⃣ Sharing Apps

### App Permissions

1. Navigate to **Compute** → **Apps**
2. Select your app
3. Click **Permissions**
4. Add users/groups with **Can Run** permission

### App URL

Share the direct URL:
```
https://your-workspace.cloud.databricks.com/apps/entertainment-co-analytics
```

Users with permission can access directly without additional setup.

---

## 4️⃣ Sharing Genie Spaces

### Add Users to Genie Space

1. Open the Genie space
2. Click **Share**
3. Add users with:
   - **Can query**: Ask questions
   - **Can edit**: Modify instructions and queries

### Best Practices

- Create **separate Genie spaces** for different audiences
- Add **certified queries** for common questions
- Keep **instructions** up to date

---

## 🌟 Databricks One: The Friendliest Way to Share

**Databricks One** is a new experience designed specifically for business users who don't need the full Databricks workspace.

### What is Databricks One?

- **Simplified interface** focused on consumption
- **Personalized homepage** with relevant assets
- **Search across** dashboards, apps, and Genie spaces
- **No SQL knowledge required**

### How to Enable

1. Go to **Admin Console** → **Databricks One**
2. Enable for your workspace
3. Add users who should use this experience

### User Experience in Databricks One

```
┌─────────────────────────────────────────────────┐
│  🏠 Home                                        │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Your Dashboards                             │
│  ├── Executive Dashboard                        │
│  └── Partner Performance                        │
│                                                 │
│  🧞 Your Genie Spaces                           │
│  └── Entertainment Analytics                    │
│                                                 │
│  📱 Your Apps                                   │
│  └── Analytics Portal                           │
│                                                 │
│  🔍 Search: "What was revenue last month?"      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Benefits of Databricks One

| Feature | Traditional | Databricks One |
|---------|-------------|----------------|
| Interface | Full workspace | Simplified |
| Learning curve | Steep | Minimal |
| Target user | Data team | Business user |
| Setup required | High | Low |
| Cost | Full license | Consumption-based |

---

## 📋 Quick Reference: Permission Levels

### Tables & Views
| Level | Can Do |
|-------|--------|
| SELECT | Read data |
| MODIFY | Insert/Update/Delete |
| ALL PRIVILEGES | Full control |

### Dashboards
| Level | Can Do |
|-------|--------|
| Can view | See dashboard |
| Can edit | Modify widgets |
| Can manage | Share + delete |

### Apps
| Level | Can Do |
|-------|--------|
| Can run | Use the app |
| Can manage | Configure + delete |

### Genie Spaces
| Level | Can Do |
|-------|--------|
| Can query | Ask questions |
| Can edit | Modify space |

---

## 🔒 Security Best Practices

1. **Use groups, not individuals**
   - Create groups like `analytics_users`, `executives`
   - Assign permissions to groups
   - Add/remove users from groups as needed

2. **Principle of least privilege**
   - Start with minimal access
   - Add more as needed
   - Review permissions quarterly

3. **Row-level security** (if needed)
   ```sql
   CREATE OR REPLACE VIEW v_partner_data AS
   SELECT * FROM gold_daily_revenue
   WHERE partner_name = CURRENT_USER_PARTNER();
   ```

4. **Audit access**
   - Use Unity Catalog audit logs
   - Monitor who accesses what
   - Set up alerts for unusual activity

---

## 🚀 Getting Started Checklist

- [ ] Create user groups in your identity provider
- [ ] Sync groups to Databricks via SCIM
- [ ] Grant schema-level SELECT to analytics group
- [ ] Share dashboard with relevant users
- [ ] Share app with business users
- [ ] Enable Databricks One for non-technical users
- [ ] Set up scheduled reports for executives
- [ ] Document access request process

---

## 🎉 Summary

| Asset | Share Via | Best For |
|-------|-----------|----------|
| Tables | Unity Catalog grants | Data team, analysts |
| Dashboards | Share button, embed | Executives, stakeholders |
| Apps | App permissions | All users |
| Genie | Space sharing | Business users |
| Everything | Databricks One | Non-technical users |

**Remember**: Unity Catalog is the foundation. Set up permissions there, and everything else flows naturally! 🎮✨
