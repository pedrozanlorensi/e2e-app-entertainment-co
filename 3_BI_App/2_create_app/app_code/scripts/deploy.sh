DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/entertainment-co" --exclude-from .gitignore
databricks apps deploy entertainment-co --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/entertainment-co"
