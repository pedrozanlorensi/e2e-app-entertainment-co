import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import { AppSidebar } from '@/components/app-sidebar';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { useSession } from '@/contexts/SessionContext';
import { DashboardPanel } from '@/components/dashboard-panel';
import { MessageSquare, BarChart3, PanelLeftClose, PanelLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ChatLayout() {
  const { session, loading } = useSession();
  const isCollapsed = localStorage.getItem('sidebar:state') !== 'true';
  const [activePanel, setActivePanel] = useState<'chat' | 'dashboard' | 'both'>('both');

  // Wait for session to load
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    );
  }

  // No guest mode - redirect if no session
  if (!session?.user) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <img 
            src="/entertainment_co_logo.png" 
            alt="Entertainment Co." 
            className="mx-auto mb-6 h-16 w-auto"
          />
          <h1 className="mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text font-bold text-3xl text-transparent">
            Entertainment Co.
          </h1>
          <h2 className="mb-4 font-semibold text-xl">Authentication Required</h2>
          <p className="text-muted-foreground">
            Please authenticate using Databricks to access this application.
          </p>
        </div>
      </div>
    );
  }

  // Get preferred username from session (if available from headers)
  const preferredUsername = session.user.preferredUsername ?? null;

  return (
    <SidebarProvider defaultOpen={!isCollapsed}>
      <AppSidebar user={session.user} preferredUsername={preferredUsername} />
      <SidebarInset className="flex flex-col">
        {/* Panel Toggle Bar */}
        <div className="flex items-center justify-center gap-1 border-b bg-muted/30 px-2 py-1">
          <div className="flex items-center rounded-lg bg-background p-1 shadow-sm">
            <Button
              variant={activePanel === 'chat' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActivePanel('chat')}
              className="gap-2"
            >
              <MessageSquare className="h-4 w-4" />
              <span className="hidden sm:inline">Chat</span>
            </Button>
            <Button
              variant={activePanel === 'both' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActivePanel('both')}
              className="gap-2"
            >
              <PanelLeft className="h-4 w-4" />
              <span className="hidden sm:inline">Both</span>
            </Button>
            <Button
              variant={activePanel === 'dashboard' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActivePanel('dashboard')}
              className="gap-2"
            >
              <BarChart3 className="h-4 w-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </Button>
          </div>
        </div>

        {/* Two Panel Layout */}
        <div className="flex flex-1 overflow-hidden">
          {/* Chat Panel */}
          <div 
            className={`flex-1 overflow-hidden transition-all duration-300 ${
              activePanel === 'dashboard' ? 'hidden lg:hidden' : ''
            } ${
              activePanel === 'both' ? 'lg:w-1/2 lg:border-r' : 'w-full'
            }`}
          >
            <Outlet />
          </div>

          {/* Dashboard Panel */}
          <div 
            className={`flex-1 overflow-hidden transition-all duration-300 ${
              activePanel === 'chat' ? 'hidden lg:hidden' : ''
            } ${
              activePanel === 'both' ? 'hidden lg:block lg:w-1/2' : 'w-full'
            }`}
          >
            <DashboardPanel />
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
