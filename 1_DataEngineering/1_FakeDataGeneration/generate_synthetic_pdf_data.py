# Databricks notebook source
# MAGIC %md
# MAGIC # 📚 Synthetic PDF Documentation Generator
# MAGIC 
# MAGIC This notebook generates synthetic PDF files containing:
# MAGIC - Business definitions and glossary
# MAGIC - KPI documentation
# MAGIC - Sample reports and charts
# MAGIC 
# MAGIC Uses Databricks Foundation Model API for content generation.

# COMMAND ----------

# MAGIC %pip install fpdf2
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from fpdf import FPDF
import os

# Configuration
CATALOG = "pedroz_catalog"
SCHEMA = "entertainment_co"
VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/raw_files"
DOCS_PATH = f"{VOLUME_PATH}/documentation"

# Create docs folder
dbutils.fs.mkdirs(DOCS_PATH)

# COMMAND ----------

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, '🎮 Entertainment Co. - Business Documentation', align='C', ln=True)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Document 1: Business Glossary

# COMMAND ----------

def create_glossary_pdf():
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'Business Glossary & Definitions', ln=True, align='C')
    pdf.ln(10)
    
    glossary = {
        "Ticket Revenue": "Total revenue generated from admission tickets sold across all facilities. Includes single-day tickets, multi-day passes, annual passes, and VIP experiences. Calculated as quantity × unit price after discounts.",
        
        "F&B Revenue (Food & Beverage)": "Revenue from all food and beverage sales within facilities. Includes restaurants, quick-service outlets, snack carts, and beverage stations. Key metric for per-capita spending analysis.",
        
        "Retail Revenue": "Revenue from merchandise sales including toys, apparel, accessories, and collectibles. Tracked by IP (Intellectual Property) for licensing performance analysis.",
        
        "Per Capita Spending": "Average spending per visitor calculated as (Ticket + F&B + Retail Revenue) / Total Visitors. Critical metric for facility performance comparison.",
        
        "IP (Intellectual Property)": "Licensed character brands and franchises (e.g., RoboBuddies, MagicPonies). Each IP has associated merchandise, themed areas, and attractions.",
        
        "Licensee/Partner": "Third-party operators licensed to operate entertainment facilities featuring company IPs. Partners submit monthly performance data.",
        
        "Repeat Visitor Rate": "Percentage of visitors who have visited the same facility within the past 12 months. Indicator of customer loyalty and experience quality.",
        
        "Conversion Rate": "Percentage of visitors who make a purchase (F&B or Retail). Calculated separately for each revenue stream.",
        
        "Peak Hours": "Time periods with highest visitor attendance, typically 11am-2pm and 4pm-7pm. Used for staffing and inventory planning.",
        
        "Market": "Geographic region for facility grouping: North America, Europe, Asia Pacific, Latin America. Used for regional performance comparison.",
        
        "YoY (Year over Year)": "Comparison of current period metrics against the same period in the previous year. Primary method for growth analysis.",
        
        "Like-for-Like (LFL)": "Comparison of facilities that have been operating for at least 12 months, excluding newly opened locations for fair comparison."
    }
    
    for term, definition in glossary.items():
        pdf.chapter_title(term)
        pdf.chapter_body(definition)
    
    pdf.output(f"/dbfs{DOCS_PATH}/business_glossary.pdf")
    print("✅ business_glossary.pdf created")

create_glossary_pdf()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Document 2: KPI Definitions

# COMMAND ----------

def create_kpi_pdf():
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'Key Performance Indicators (KPIs)', ln=True, align='C')
    pdf.ln(10)
    
    kpis = [
        ("Total Revenue", "SUM(ticket_revenue + fnb_revenue + retail_revenue)", "Higher is better", "$XXM"),
        ("Total Attendance", "COUNT(DISTINCT visitor_id)", "Track vs capacity", "X.XM visitors"),
        ("Per Capita Total", "Total Revenue / Total Attendance", "> $50 target", "$XX.XX"),
        ("Per Capita F&B", "F&B Revenue / Total Attendance", "> $12 target", "$XX.XX"),
        ("Per Capita Retail", "Retail Revenue / Total Attendance", "> $8 target", "$XX.XX"),
        ("Ticket Yield", "Ticket Revenue / Total Attendance", "Track pricing power", "$XX.XX"),
        ("Repeat Visit Rate", "(Repeat Visitors / Total Visitors) × 100", "> 30% target", "XX%"),
        ("Conversion Rate F&B", "(F&B Transactions / Attendance) × 100", "> 60% target", "XX%"),
        ("Conversion Rate Retail", "(Retail Transactions / Attendance) × 100", "> 25% target", "XX%"),
        ("IP Revenue Share", "(IP Revenue / Total Retail) × 100", "Track IP performance", "XX%"),
    ]
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(100, 150, 200)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 8, "KPI Name", border=1, fill=True)
    pdf.cell(70, 8, "Formula", border=1, fill=True)
    pdf.cell(40, 8, "Target", border=1, fill=True)
    pdf.cell(30, 8, "Format", border=1, fill=True, ln=True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 9)
    
    for kpi in kpis:
        pdf.cell(50, 8, kpi[0], border=1)
        pdf.cell(70, 8, kpi[1][:35], border=1)
        pdf.cell(40, 8, kpi[2], border=1)
        pdf.cell(30, 8, kpi[3], border=1, ln=True)
    
    pdf.ln(15)
    pdf.chapter_title("KPI Reporting Frequency")
    pdf.chapter_body("""
Daily: Attendance, Revenue totals, Per capita metrics
Weekly: Conversion rates, IP performance, Peak hour analysis
Monthly: YoY comparisons, Partner performance, Forecast accuracy
Quarterly: Market comparisons, Strategic KPIs, Executive dashboard
    """)
    
    pdf.output(f"/dbfs{DOCS_PATH}/kpi_definitions.pdf")
    print("✅ kpi_definitions.pdf created")

create_kpi_pdf()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Document 3: Data Dictionary

# COMMAND ----------

def create_data_dictionary_pdf():
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'Data Dictionary', ln=True, align='C')
    pdf.ln(10)
    
    # Ticket Sales Table
    pdf.chapter_title("Table: ticket_sales")
    pdf.chapter_body("""
Source: Partner monthly uploads
Grain: One row per ticket transaction
Refresh: Monthly batch

Columns:
- transaction_id (STRING): Unique identifier for ticket purchase
- transaction_date (DATE): Date of purchase
- facility_id (STRING): Facility where ticket was sold
- ip_name (STRING): Associated IP/franchise
- ticket_type (STRING): Adult, Child, Senior, Family_Pack, VIP, Annual_Pass
- quantity (INT): Number of tickets in transaction
- unit_price (DECIMAL): Price per ticket before discount
- discount_pct (INT): Discount percentage applied
- total_amount (DECIMAL): Final transaction amount
- customer_id (STRING): Customer identifier
- is_repeat_visitor (BOOLEAN): Whether customer visited before
- visit_hour (INT): Hour of day (9-20)
- channel (STRING): Purchase channel
    """)
    
    # F&B Sales Table
    pdf.chapter_title("Table: fnb_sales")
    pdf.chapter_body("""
Source: Partner monthly uploads
Grain: One row per F&B transaction
Refresh: Monthly batch

Columns:
- transaction_id (STRING): Unique identifier
- transaction_date (DATE): Date of purchase
- facility_id (STRING): Facility location
- item_name (STRING): Product name
- item_category (STRING): Main, Snack, Beverage, Dessert
- unit_price (DECIMAL): Item price
- quantity (INT): Quantity purchased
- total_amount (DECIMAL): Transaction total
- customer_id (STRING): Customer identifier
- outlet_id (STRING): F&B outlet identifier
- payment_method (STRING): Payment type
- transaction_hour (INT): Hour of purchase
    """)
    
    # Retail Sales Table
    pdf.chapter_title("Table: retail_sales")
    pdf.chapter_body("""
Source: Partner monthly uploads
Grain: One row per retail transaction
Refresh: Monthly batch

Columns:
- transaction_id (STRING): Unique identifier
- transaction_date (DATE): Date of purchase
- facility_id (STRING): Facility location
- ip_name (STRING): Associated IP/franchise
- product_name (STRING): Merchandise item name
- product_category (STRING): Toys, Apparel, Accessories, etc.
- unit_price (DECIMAL): Product price
- quantity (INT): Quantity purchased
- total_amount (DECIMAL): Transaction total
- customer_id (STRING): Customer identifier
- store_id (STRING): Retail store identifier
- is_online (BOOLEAN): Online vs in-store purchase
    """)
    
    pdf.output(f"/dbfs{DOCS_PATH}/data_dictionary.pdf")
    print("✅ data_dictionary.pdf created")

create_data_dictionary_pdf()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Document 4: Analysis Guidelines

# COMMAND ----------

def create_analysis_guidelines_pdf():
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'Analysis Guidelines & Best Practices', ln=True, align='C')
    pdf.ln(10)
    
    pdf.chapter_title("1. Period Comparisons")
    pdf.chapter_body("""
When comparing performance across time periods:

Prior Year (PY): Compare current month/quarter to same period last year
- Use for: Seasonal businesses, YoY growth tracking
- Consideration: Account for calendar shifts (holidays, weekends)

Prior Month (PM): Compare to immediately preceding month
- Use for: Trend identification, short-term performance
- Consideration: Seasonal adjustments may be needed

Prior Quarter (PQ): Compare to previous quarter
- Use for: Quarterly business reviews, medium-term trends
- Consideration: Q4 vs Q1 comparisons need holiday context
    """)
    
    pdf.chapter_title("2. Like-for-Like Analysis")
    pdf.chapter_body("""
For fair facility comparisons:

Same Market: Compare facilities in the same geographic market first
- North America facilities compared to North America peers
- Controls for economic conditions and seasonality

Similar Experience Type: Group by Theme_Park, Indoor_Center, or Hybrid
- Accounts for different operating models and cost structures

Maturity: Only compare facilities open 12+ months
- New facilities have ramp-up period affecting metrics
    """)
    
    pdf.chapter_title("3. IP Performance Analysis")
    pdf.chapter_body("""
When analyzing Intellectual Property performance:

Revenue Attribution: Track retail sales by IP
- Top performers indicate licensing opportunities
- Underperformers may need marketing support

Cross-Facility Comparison: Same IP across different markets
- Identifies regional preferences
- Informs localization decisions

Product Mix: Analyze which product categories perform best per IP
- Toys vs Apparel vs Accessories breakdown
- Guides inventory and merchandising decisions
    """)
    
    pdf.chapter_title("4. Peak Time Analysis")
    pdf.chapter_body("""
Understanding visitor patterns:

Daily Peaks: Typically 11am-2pm (lunch) and 4pm-7pm (after work/school)
- Staff scheduling optimization
- F&B inventory planning

Weekly Peaks: Weekends significantly higher than weekdays
- Pricing strategies (dynamic pricing)
- Special event scheduling

Seasonal Peaks: School holidays, summer, winter break
- Capacity management
- Marketing campaign timing
    """)
    
    pdf.output(f"/dbfs{DOCS_PATH}/analysis_guidelines.pdf")
    print("✅ analysis_guidelines.pdf created")

create_analysis_guidelines_pdf()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary

# COMMAND ----------

print("📚 Documentation PDFs Generated:")
print("=" * 50)
docs = dbutils.fs.ls(DOCS_PATH)
for doc in docs:
    print(f"  📄 {doc.name}")

print("\n✅ All documentation ready for Knowledge Assistant ingestion!")
