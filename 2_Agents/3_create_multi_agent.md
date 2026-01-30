# 🤖 Create a Multi-Agent Orchestrator

This guide walks you through creating a multi-agent system that combines the Knowledge Assistant and Genie space into a unified conversational experience.

---

## Prerequisites

- ✅ Knowledge Assistant deployed (see `2_create_knowledge_assistant.md`)
- ✅ Genie Space created (see `3_create_genie_space.md`)
- ✅ Access to Agent Bricks in your workspace

---

## Architecture Overview

```
                    ┌─────────────────────┐
                    │   User Question     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Supervisor Agent  │
                    │   (Orchestrator)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐  ┌───▼───┐  ┌────────▼────────┐
    │   Knowledge       │  │ Genie │  │   Direct LLM    │
    │   Assistant       │  │ Agent │  │   Response      │
    └───────────────────┘  └───────┘  └─────────────────┘
    
    "What is Per Capita?"  "Show me revenue"  "Hello, how are you?"
```

---

## Step 1: Create the Supervisor Agent

1. Navigate to **Machine Learning** → **Playground**
2. Click **Create Agent** → **Multi-Agent System**
3. Configure:
   - **Name**: `Entertainment_Co_Supervisor`
   - **Description**: `Orchestrates between knowledge and data queries for Entertainment Co.`

---

## Step 2: Configure Child Agents

### Add Knowledge Assistant
```yaml
agent_name: knowledge_assistant
endpoint: entertainment_knowledge_assistant_endpoint
description: |
  Answers questions about business definitions, KPIs, data dictionary,
  and analysis best practices. Use this agent when the user asks:
  - What is [term]?
  - How do I calculate [metric]?
  - What does [column] mean?
  - What are the best practices for [analysis type]?
```

### Add Genie Agent
```yaml
agent_name: genie_data_agent
genie_space_id: <your-genie-space-id>
description: |
  Queries the gold-level data tables to answer analytical questions.
  Use this agent when the user asks:
  - Show me [metric] by [dimension]
  - What is the [metric] for [entity]?
  - Compare [period A] to [period B]
  - Which [entity] has the highest [metric]?
  - Top N [items] by [metric]
```

---

## Step 3: Configure the Supervisor System Prompt

```
You are a helpful supervisor agent for Entertainment Co., a toy and entertainment company.

Your job is to route user questions to the appropriate specialized agent:

## Agent Selection Rules

### Route to KNOWLEDGE_ASSISTANT when:
- User asks about definitions ("What is...", "What does... mean?")
- User asks about KPI formulas or targets
- User asks about data schemas or table structures
- User asks about best practices or guidelines
- User needs documentation or reference material

### Route to GENIE_DATA_AGENT when:
- User asks for specific numbers or metrics
- User wants to see data (revenue, visitors, performance)
- User asks for comparisons between periods or entities
- User asks for rankings (top/bottom performers)
- User asks about trends or patterns

### Handle DIRECTLY when:
- User says hello or greets you
- User asks about your capabilities
- User's question is unclear (ask for clarification)
- User's request doesn't fit either agent

## Response Guidelines

1. ALWAYS identify which agent you're routing to
2. If using Genie, let the user know data is being queried
3. If the answer requires both agents, call them in sequence:
   - First get the definition from Knowledge Assistant
   - Then get the data from Genie

## Example Routing

User: "What is Per Capita spending?"
→ Route to: KNOWLEDGE_ASSISTANT (definition question)

User: "What was our Per Capita last month?"
→ Route to: GENIE_DATA_AGENT (needs actual data)

User: "Explain Per Capita and show me the trend"
→ Route to: KNOWLEDGE_ASSISTANT first, then GENIE_DATA_AGENT

User: "Hello!"
→ Handle directly: "Hello! I'm your Entertainment Co. analytics assistant..."
```

---

## Step 4: Configure Agent Tools

In the Agent configuration, add these tools:

### Tool 1: Knowledge Lookup
```python
@tool
def knowledge_lookup(question: str) -> str:
    """
    Look up business definitions, KPIs, or documentation.
    Use for: definitions, formulas, best practices, data dictionary.
    """
    # This connects to the Knowledge Assistant endpoint
    pass
```

### Tool 2: Data Query
```python
@tool
def data_query(question: str) -> str:
    """
    Query the data warehouse for metrics and analytics.
    Use for: revenue, visitors, comparisons, rankings, trends.
    """
    # This connects to the Genie space
    pass
```

---

## Step 5: Test the Multi-Agent System

### Test Routing Logic

| Question | Expected Route |
|----------|----------------|
| "What is the definition of Repeat Visit Rate?" | Knowledge Assistant |
| "What was our repeat visit rate in November?" | Genie |
| "Explain Per Capita and show me last month's numbers" | Both (sequential) |
| "Hi there!" | Direct response |
| "Top 5 F&B items by revenue" | Genie |
| "How should I compare facilities?" | Knowledge Assistant |

### Sample Conversation Flow

```
User: What is Per Capita spending and how are we performing?

Supervisor: I'll help you with that! Let me first get the definition 
and then pull the latest numbers.

[Calls Knowledge Assistant]
Per Capita Spending is the average spending per visitor, calculated 
as (Ticket + F&B + Retail Revenue) / Total Visitors.

[Calls Genie]
Here's our recent Per Capita performance:
| Partner | Nov 2025 | Dec 2025 | Change |
|---------|----------|----------|--------|
| DreamWorld | $52.34 | $58.12 | +11.0% |
| FunZone | $48.90 | $51.23 | +4.8% |
...

The holiday season is driving higher per capita spending across 
all partners!
```

---

## Step 6: Deploy the Supervisor Agent

1. Click **Deploy** in the Agent editor
2. Configure:
   - **Endpoint Name**: `entertainment_co_supervisor_endpoint`
   - **Compute Size**: Medium (handles routing + sub-agent calls)
3. Click **Deploy**

---

## Step 7: Integration Options

### Python SDK
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

response = w.serving_endpoints.query(
    name="entertainment_co_supervisor_endpoint",
    inputs=[{"question": "What was our total revenue last month?"}]
)

print(response.predictions[0])
```

### REST API
```bash
curl -X POST \
  https://<workspace-url>/serving-endpoints/entertainment_co_supervisor_endpoint/invocations \
  -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": [{"question": "Show me top performing IPs"}]}'
```

---

## 🎯 Next Steps

- Create a dashboard with `5_create_aibi_dashboard.md`
- Build an app to surface the agent with `6_create_app.md`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong agent selected | Refine the system prompt routing rules |
| Slow responses | Check child agent endpoint latency |
| Genie not returning data | Verify Genie space permissions |
| Knowledge gaps | Add more documents to Vector Search |
