## Create a Databricks App (brief overview)

This project is deployed as a **Databricks App** using the Databricks CLI. The app source code is defined by `app.yaml` in this folder.

### Prerequisites

- Databricks workspace access with permissions to create/deploy Apps
- Databricks CLI installed and authenticated

```bash
brew install databricks
databricks auth login
```

### 1) Create the app (one-time)

Create a new app in your workspace (UI or CLI). In the UI:

- Go to **Databricks Apps** → **Create app**
- Name it (example: `entertainment-co`)

### 2) Sync this repo folder to your workspace

From `3_BI_App/2_create_app/`:

```bash
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/entertainment-co"
```

This uploads your local files to:

- `/Workspace/Users/<your-username>/entertainment-co`

### 3) Deploy the app from the workspace path

```bash
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks apps deploy entertainment-co \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/entertainment-co"
```

Tip: this repo also includes a helper script you can run instead:

```bash
sh scripts/deploy.sh
```

### 4) Watch logs / troubleshoot

```bash
databricks apps logs entertainment-co --tail-lines 300
```

Common causes of deploy failures:

- **Dependency install failures**: confirm `package.json` / `package-lock.json` are valid and consistent
- **Embedding dashboards**: ensure the dashboard is published and workspace settings allow iframe embedding
