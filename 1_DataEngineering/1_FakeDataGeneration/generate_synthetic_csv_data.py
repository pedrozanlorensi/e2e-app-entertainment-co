# Databricks notebook source
# MAGIC %md
# MAGIC # 🎮 Synthetic CSV Data Generator for Entertainment Co.
# MAGIC 
# MAGIC This notebook generates synthetic data for a toy company's analytics platform.
# MAGIC 
# MAGIC **Data includes:**
# MAGIC - Ticket Sales
# MAGIC - F&B (Food & Beverage) Revenue
# MAGIC - Retail Revenue
# MAGIC - Visitor Analytics
# MAGIC - Campaign Performance

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create catalog and schema
# MAGIC CREATE CATALOG IF NOT EXISTS pedroz_catalog;
# MAGIC USE CATALOG pedroz_catalog;
# MAGIC CREATE SCHEMA IF NOT EXISTS entertainment_co;
# MAGIC USE SCHEMA entertainment_co;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create Volume for raw files
# MAGIC CREATE VOLUME IF NOT EXISTS pedroz_catalog.entertainment_co.raw_files;

# COMMAND ----------

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Configuration
CATALOG = "pedroz_catalog"
SCHEMA = "entertainment_co"
VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/raw_files"

# Partners (Licensees)
PARTNERS = ["DreamWorld_Parks", "FunZone_Entertainment", "ToyLand_Adventures", "PlayNation_Centers", "KidVenture_Group"]

# IP (Intellectual Properties)
IPS = ["RoboBuddies", "MagicPonies", "SpaceRangers", "DinoSquad", "FairyKingdom", "SuperBlocks", "ActionHeroes"]

# Facilities by Partner
FACILITIES = {
    "DreamWorld_Parks": ["DW_Orlando", "DW_California", "DW_Tokyo"],
    "FunZone_Entertainment": ["FZ_NewYork", "FZ_Chicago", "FZ_Miami"],
    "ToyLand_Adventures": ["TL_London", "TL_Paris", "TL_Berlin"],
    "PlayNation_Centers": ["PN_Sydney", "PN_Melbourne", "PN_Brisbane"],
    "KidVenture_Group": ["KV_Toronto", "KV_Vancouver", "KV_Montreal"]
}

# Markets
MARKETS = ["North_America", "Europe", "Asia_Pacific", "Latin_America"]

# Date range for 6 months of data
START_DATE = datetime(2025, 7, 1)
END_DATE = datetime(2025, 12, 31)

# COMMAND ----------

def generate_ticket_sales(partner, month, num_rows=170000):
    """Generate ticket sales data for a partner and month"""
    np.random.seed(hash(f"{partner}_{month}") % 2**32)
    
    facilities = FACILITIES[partner]
    dates = pd.date_range(start=f"2025-{month:02d}-01", periods=28, freq='D')
    
    data = {
        "transaction_id": [f"TKT_{partner[:3]}_{month}_{i:06d}" for i in range(num_rows)],
        "transaction_date": np.random.choice(dates, num_rows),
        "facility_id": np.random.choice(facilities, num_rows),
        "ip_name": np.random.choice(IPS, num_rows),
        "ticket_type": np.random.choice(["Adult", "Child", "Senior", "Family_Pack", "VIP", "Annual_Pass"], num_rows, p=[0.3, 0.35, 0.1, 0.15, 0.05, 0.05]),
        "quantity": np.random.randint(1, 6, num_rows),
        "unit_price": np.round(np.random.uniform(25, 150, num_rows), 2),
        "discount_pct": np.random.choice([0, 5, 10, 15, 20, 25], num_rows, p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05]),
        "customer_id": [f"CUST_{np.random.randint(1, 500000):06d}" for _ in range(num_rows)],
        "is_repeat_visitor": np.random.choice([True, False], num_rows, p=[0.35, 0.65]),
        "visit_hour": np.random.choice(range(9, 21), num_rows),
        "channel": np.random.choice(["Online", "Box_Office", "Mobile_App", "Partner_Site"], num_rows, p=[0.45, 0.25, 0.2, 0.1]),
    }
    
    df = pd.DataFrame(data)
    df["total_amount"] = np.round(df["quantity"] * df["unit_price"] * (1 - df["discount_pct"]/100), 2)
    return df

# COMMAND ----------

def generate_fnb_sales(partner, month, num_rows=170000):
    """Generate Food & Beverage sales data"""
    np.random.seed(hash(f"fnb_{partner}_{month}") % 2**32)
    
    facilities = FACILITIES[partner]
    dates = pd.date_range(start=f"2025-{month:02d}-01", periods=28, freq='D')
    
    fnb_items = [
        ("Burger_Combo", 12.99), ("Pizza_Slice", 6.99), ("Hot_Dog", 5.99),
        ("Chicken_Nuggets", 8.99), ("Ice_Cream", 4.99), ("Cotton_Candy", 3.99),
        ("Popcorn_Large", 7.99), ("Soda_Large", 3.99), ("Churros", 5.99),
        ("Pretzel", 4.99), ("Nachos", 9.99), ("Funnel_Cake", 8.99),
        ("Frozen_Lemonade", 5.99), ("Turkey_Leg", 14.99), ("Fruit_Cup", 6.99)
    ]
    
    items = [random.choice(fnb_items) for _ in range(num_rows)]
    
    data = {
        "transaction_id": [f"FNB_{partner[:3]}_{month}_{i:06d}" for i in range(num_rows)],
        "transaction_date": np.random.choice(dates, num_rows),
        "facility_id": np.random.choice(facilities, num_rows),
        "item_name": [item[0] for item in items],
        "item_category": np.random.choice(["Main", "Snack", "Beverage", "Dessert"], num_rows, p=[0.3, 0.25, 0.25, 0.2]),
        "unit_price": [item[1] for item in items],
        "quantity": np.random.randint(1, 5, num_rows),
        "customer_id": [f"CUST_{np.random.randint(1, 500000):06d}" for _ in range(num_rows)],
        "outlet_id": [f"OUTLET_{np.random.randint(1, 50):03d}" for _ in range(num_rows)],
        "payment_method": np.random.choice(["Credit_Card", "Debit_Card", "Cash", "Mobile_Pay"], num_rows, p=[0.4, 0.25, 0.15, 0.2]),
        "transaction_hour": np.random.choice(range(10, 22), num_rows),
    }
    
    df = pd.DataFrame(data)
    df["total_amount"] = np.round(df["quantity"] * df["unit_price"], 2)
    return df

# COMMAND ----------

def generate_retail_sales(partner, month, num_rows=170000):
    """Generate Retail merchandise sales data"""
    np.random.seed(hash(f"retail_{partner}_{month}") % 2**32)
    
    facilities = FACILITIES[partner]
    dates = pd.date_range(start=f"2025-{month:02d}-01", periods=28, freq='D')
    
    retail_items = [
        ("Plush_Toy_Small", 14.99), ("Plush_Toy_Large", 29.99), ("Action_Figure", 19.99),
        ("T_Shirt_Kids", 24.99), ("T_Shirt_Adult", 29.99), ("Cap_Hat", 19.99),
        ("Keychain", 9.99), ("Mug", 14.99), ("Poster", 12.99),
        ("Board_Game", 34.99), ("Puzzle", 19.99), ("Backpack", 39.99),
        ("Water_Bottle", 16.99), ("Lunchbox", 22.99), ("Blanket", 44.99)
    ]
    
    items = [random.choice(retail_items) for _ in range(num_rows)]
    
    data = {
        "transaction_id": [f"RTL_{partner[:3]}_{month}_{i:06d}" for i in range(num_rows)],
        "transaction_date": np.random.choice(dates, num_rows),
        "facility_id": np.random.choice(facilities, num_rows),
        "ip_name": np.random.choice(IPS, num_rows),
        "product_name": [item[0] for item in items],
        "product_category": np.random.choice(["Toys", "Apparel", "Accessories", "Collectibles", "Home"], num_rows),
        "unit_price": [item[1] for item in items],
        "quantity": np.random.randint(1, 4, num_rows),
        "customer_id": [f"CUST_{np.random.randint(1, 500000):06d}" for _ in range(num_rows)],
        "store_id": [f"STORE_{np.random.randint(1, 30):03d}" for _ in range(num_rows)],
        "is_online": np.random.choice([True, False], num_rows, p=[0.2, 0.8]),
    }
    
    df = pd.DataFrame(data)
    df["total_amount"] = np.round(df["quantity"] * df["unit_price"], 2)
    return df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate and Save Partner Data (6 months each)

# COMMAND ----------

# Generate data for each partner (6 months)
months = [7, 8, 9, 10, 11, 12]  # July to December 2025

for partner in PARTNERS:
    print(f"🎯 Generating data for {partner}...")
    
    # Create partner folder
    partner_path = f"{VOLUME_PATH}/partners/{partner}"
    dbutils.fs.mkdirs(partner_path)
    
    for month in months:
        # Ticket Sales
        ticket_df = generate_ticket_sales(partner, month)
        ticket_df.to_csv(f"/{partner_path}/ticket_sales_{month:02d}_2025.csv", index=False)
        
        # F&B Sales
        fnb_df = generate_fnb_sales(partner, month)
        fnb_df.to_csv(f"/{partner_path}/fnb_sales_{month:02d}_2025.csv", index=False)
        
        # Retail Sales
        retail_df = generate_retail_sales(partner, month)
        retail_df.to_csv(f"/{partner_path}/retail_sales_{month:02d}_2025.csv", index=False)
        
        print(f"  ✅ Month {month} - Generated ~510K records (tickets + F&B + retail)")

print("\n🎉 All partner data generated!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Dimension Tables

# COMMAND ----------

# Create dimensions folder
dim_path = f"{VOLUME_PATH}/dimensions"
dbutils.fs.mkdirs(dim_path)

# COMMAND ----------

# Dimension: Campaigns
campaigns = []
campaign_names = [
    "Summer_Splash", "Back_to_School", "Halloween_Spooktacular", 
    "Holiday_Magic", "Spring_Break_Blast", "Birthday_Bonanza"
]

for i, name in enumerate(campaign_names):
    campaigns.append({
        "campaign_id": f"CAMP_{i+1:03d}",
        "campaign_name": name,
        "start_date": (START_DATE + timedelta(days=i*30)).strftime("%Y-%m-%d"),
        "end_date": (START_DATE + timedelta(days=(i+1)*30-1)).strftime("%Y-%m-%d"),
        "budget_usd": random.randint(100000, 500000),
        "channel": random.choice(["TV", "Digital", "Social", "Print", "Multi-Channel"]),
        "target_demographic": random.choice(["Families", "Kids_5-12", "Teens", "All_Ages"]),
        "is_active": i >= 3  # Last 3 campaigns are active
    })

pd.DataFrame(campaigns).to_csv(f"/{dim_path}/dim_campaigns.csv", index=False)
print("✅ dim_campaigns.csv created")

# COMMAND ----------

# Dimension: Products (for retail)
products = []
product_list = [
    ("Plush_Toy_Small", "Toys", "RoboBuddies"), ("Plush_Toy_Large", "Toys", "MagicPonies"),
    ("Action_Figure", "Toys", "SpaceRangers"), ("T_Shirt_Kids", "Apparel", "DinoSquad"),
    ("T_Shirt_Adult", "Apparel", "SuperBlocks"), ("Cap_Hat", "Accessories", "ActionHeroes"),
    ("Keychain", "Accessories", "FairyKingdom"), ("Mug", "Home", "RoboBuddies"),
    ("Board_Game", "Toys", "SpaceRangers"), ("Backpack", "Accessories", "DinoSquad")
]

for i, (name, category, ip) in enumerate(product_list):
    products.append({
        "product_id": f"PROD_{i+1:04d}",
        "product_name": name,
        "category": category,
        "ip_name": ip,
        "base_price": round(random.uniform(9.99, 49.99), 2),
        "cost": round(random.uniform(3.99, 19.99), 2),
        "supplier": random.choice(["ToyMaster_Inc", "GlobalGoods", "QualityPlush", "ApparelPro"]),
        "launch_date": "2024-01-15"
    })

pd.DataFrame(products).to_csv(f"/{dim_path}/dim_products.csv", index=False)
print("✅ dim_products.csv created")

# COMMAND ----------

# Dimension: Facilities
facilities_dim = []
for partner, facs in FACILITIES.items():
    for fac in facs:
        market = "North_America" if "Orlando" in fac or "California" in fac or "NewYork" in fac or "Chicago" in fac or "Miami" in fac or "Toronto" in fac or "Vancouver" in fac or "Montreal" in fac else \
                 "Europe" if "London" in fac or "Paris" in fac or "Berlin" in fac else \
                 "Asia_Pacific"
        facilities_dim.append({
            "facility_id": fac,
            "facility_name": fac.replace("_", " "),
            "partner_name": partner,
            "market": market,
            "country": fac.split("_")[1] if "_" in fac else "Unknown",
            "capacity": random.randint(5000, 25000),
            "opened_date": f"20{random.randint(15, 23)}-0{random.randint(1,9)}-01",
            "experience_type": random.choice(["Theme_Park", "Indoor_Center", "Hybrid"])
        })

pd.DataFrame(facilities_dim).to_csv(f"/{dim_path}/dim_facilities.csv", index=False)
print("✅ dim_facilities.csv created")

# COMMAND ----------

# Dimension: Customers (sample)
customers = []
for i in range(10000):
    customers.append({
        "customer_id": f"CUST_{i:06d}",
        "customer_segment": random.choice(["Frequent_Visitor", "Annual_Pass", "Occasional", "First_Time", "VIP"]),
        "age_group": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
        "family_size": random.randint(1, 6),
        "home_market": random.choice(MARKETS),
        "signup_date": (START_DATE - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
        "loyalty_tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"])
    })

pd.DataFrame(customers).to_csv(f"/{dim_path}/dim_customers.csv", index=False)
print("✅ dim_customers.csv created")

# COMMAND ----------

# Dimension: Date (calendar)
dates = []
current = START_DATE
while current <= END_DATE:
    dates.append({
        "date": current.strftime("%Y-%m-%d"),
        "year": current.year,
        "quarter": (current.month - 1) // 3 + 1,
        "month": current.month,
        "month_name": current.strftime("%B"),
        "week_of_year": current.isocalendar()[1],
        "day_of_week": current.strftime("%A"),
        "is_weekend": current.weekday() >= 5,
        "is_holiday": current.month == 12 and current.day in [24, 25, 31],
        "season": "Summer" if current.month in [6,7,8] else "Fall" if current.month in [9,10,11] else "Winter"
    })
    current += timedelta(days=1)

pd.DataFrame(dates).to_csv(f"/{dim_path}/dim_dates.csv", index=False)
print("✅ dim_dates.csv created")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary

# COMMAND ----------

# List all generated files
print("📁 Generated Files Summary:")
print("\n📂 Partner Data (6 months × 3 file types × 5 partners = 90 files):")
for partner in PARTNERS:
    files = dbutils.fs.ls(f"{VOLUME_PATH}/partners/{partner}")
    print(f"  └── {partner}: {len(files)} files")

print("\n📂 Dimension Tables:")
dim_files = dbutils.fs.ls(f"{VOLUME_PATH}/dimensions")
for f in dim_files:
    print(f"  └── {f.name}")

print("\n✅ Data generation complete! Ready for ETL processing.")
