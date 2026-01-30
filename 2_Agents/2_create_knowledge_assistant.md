# 📚 Create a Knowledge Assistant with Agent Bricks

This guide walks you through creating a Knowledge Assistant agent that can answer questions about your business documentation (glossary, KPIs, data dictionary).

---

## Prerequisites

- ✅ Run `0_generate_synthetic_pdf_data.py` to generate documentation PDFs
- ✅ Databricks workspace with Unity Catalog enabled
- ✅ Access to a Vector Search endpoint

---

## Step 1: Create a Vector Search Endpoint

1. Navigate to **Catalog** → **Vector Search**
2. Click **Create endpoint**
3. Configure:
   - **Name**: `entertainment_co_vs_endpoint`
   - **Type**: Standard
4. Click **Create**

> ⏳ Wait for the endpoint to be ready (takes ~5 minutes)

---

## Step 2: Create a Vector Search Index

1. Go to your Volume: `pedroz_catalog.entertainment_co.raw_files`
2. Navigate to the `documentation` folder
3. Right-click → **Create Vector Search Index**

Or use SQL:

```sql
-- Create a table from the PDF content (if not already parsed)
CREATE OR REPLACE TABLE pedroz_catalog.entertainment_co.documentation_chunks AS
SELECT 
    file_name,
    chunk_id,
    chunk_text,
    ai_embed(chunk_text) as embedding
FROM (
    SELECT 
        _metadata.file_name as file_name,
        posexplode(ai_parse_document(content, 'chunk')) as (chunk_id, chunk_text)
    FROM read_files('/Volumes/pedroz_catalog/entertainment_co/raw_files/documentation/*.pdf')
);

-- Create the vector index
CREATE VECTOR SEARCH INDEX IF NOT EXISTS entertainment_docs_index
ON TABLE pedroz_catalog.entertainment_co.documentation_chunks
(embedding)
USING DELTA_SYNC
WITH (
    endpoint_name = 'entertainment_co_vs_endpoint',
    embedding_dimension = 1024,
    embedding_model = 'databricks-gte-large-en'
);
```

---

## Step 3: Create the Knowledge Assistant using Agent Bricks

1. Navigate to **Machine Learning** → **Playground**
2. Click **Create Agent** → **Knowledge Assistant**
3. Configure the agent:

### Basic Settings
- **Name**: `Entertainment_Knowledge_Assistant`
- **Description**: `Answers questions about business definitions, KPIs, and data dictionary for Entertainment Co.`

### Knowledge Source
- **Vector Search Index**: Select `entertainment_docs_index`
- **Retrieval Settings**:
  - Top K: `5`
  - Score Threshold: `0.7`

### System Prompt
```
You are a helpful Knowledge Assistant for Entertainment Co., a toy and entertainment company.

Your role is to answer questions about:
- Business terminology and definitions
- KPI formulas and targets
- Data dictionary and table schemas
- Analysis best practices

When answering:
1. Always cite which document the information comes from
2. Be concise but thorough
3. If you're unsure, say so rather than making up information
4. Use bullet points for clarity

Available documentation:
- Business Glossary: Definitions of key terms
- KPI Definitions: Metrics, formulas, and targets
- Data Dictionary: Table and column descriptions
- Analysis Guidelines: Best practices for reporting
```

### Model Settings
- **Model**: `databricks-meta-llama-3-1-70b-instruct`
- **Temperature**: `0.1` (for more factual responses)

4. Click **Create Agent**

---

## Step 4: Test the Agent

Try these sample questions:

1. **"What is Per Capita Spending?"**
2. **"How do I calculate the Repeat Visit Rate?"**
3. **"What columns are in the ticket_sales table?"**
4. **"How should I compare facilities across markets?"**
5. **"What is the target for F&B conversion rate?"**

---

## Step 5: Deploy the Agent

1. In the Agent editor, click **Deploy**
2. Configure:
   - **Serving Endpoint Name**: `entertainment_knowledge_assistant_endpoint`
   - **Compute Size**: Small
3. Click **Deploy**

The endpoint will be available at:
```
https://<workspace-url>/serving-endpoints/entertainment_knowledge_assistant_endpoint/invocations
```

---

## 🎯 Next Steps

- Proceed to `3_create_genie_space.md` to create a Genie space for data queries
- Then use `4_create_multi_agent.md` to combine both agents

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results returned | Lower the score threshold to 0.5 |
| Slow responses | Check Vector Search endpoint status |
| Missing documents | Re-run the PDF generation notebook |
