import { useEffect, useMemo, useState } from 'react';
import { BarChart3, ExternalLink, RefreshCw } from 'lucide-react';
import { Button } from './ui/button';

interface DashboardPanelProps {
  instanceUrl?: string;
  workspaceId?: string;
  dashboardId?: string;
}

export function DashboardPanel({
  instanceUrl = "https://e2-demo-field-eng.cloud.databricks.com",
  workspaceId = "1444828305810485",
  dashboardId = "01f0fd70293d1fb2b56879b9058116b3",
}: DashboardPanelProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [reloadKey, setReloadKey] = useState(0);

  // Note: `@databricks/aibi-client` isn't available in the public npm registry in your build env.
  // For Databricks Apps (same workspace), embedding via iframe typically works because auth cookies
  // are already present on the same Databricks host.
  const dashboardViewUrl = useMemo(() => {
    const base = instanceUrl.replace(/\/$/, '');
    return `${base}/dashboards/${dashboardId}?o=${encodeURIComponent(workspaceId)}`;
  }, [instanceUrl, dashboardId, workspaceId]);

  const dashboardEmbedUrl = useMemo(() => {
    const base = instanceUrl.replace(/\/$/, '');
    // Databricks AI/BI embed URL format:
    // https://<workspace-host>/embed/dashboardsv3/<dashboardId>?o=<workspaceId>
    return `${base}/embed/dashboardsv3/${dashboardId}?o=${encodeURIComponent(workspaceId)}`;
  }, [instanceUrl, dashboardId, workspaceId]);

  useEffect(() => {
    setIsLoading(true);
  }, [dashboardEmbedUrl, reloadKey]);

  return (
    <div className="flex h-full flex-col bg-background">
      {/* Dashboard Header */}
      <div className="flex items-center justify-between border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5 text-purple-600" />
          <h2 className="font-semibold text-lg">Analytics Dashboard</h2>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            asChild
            className="gap-2"
          >
            <a href={dashboardViewUrl} target="_blank" rel="noreferrer">
              <ExternalLink className="h-4 w-4" />
              <span className="hidden sm:inline">Open</span>
            </a>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setReloadKey((k) => k + 1)}
            className="gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span className="hidden sm:inline">Refresh</span>
          </Button>
        </div>
      </div>

      {/* Dashboard Content */}
      <div className="relative flex-1 overflow-auto">
        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-background/80">
            <div className="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-purple-200 border-t-purple-600" />
            <p className="text-muted-foreground text-sm">Loading dashboard...</p>
          </div>
        )}

        <iframe
          key={reloadKey}
          title="Entertainment Co. Dashboard"
          src={dashboardEmbedUrl}
          className="h-full w-full"
          style={{ minHeight: '500px' }}
          onLoad={() => setIsLoading(false)}
          // Some browsers enforce stricter defaults without an allowlist.
          // If you need downloads/clipboard/etc from inside the iframe, add them here.
          allow="fullscreen"
        />
      </div>
    </div>
  );
}
