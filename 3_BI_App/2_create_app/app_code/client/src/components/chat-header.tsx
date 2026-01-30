import { useNavigate } from 'react-router-dom';
import { useWindowSize } from 'usehooks-ts';

import { SidebarToggle } from '@/components/sidebar-toggle';
import { Button } from '@/components/ui/button';
import { useSidebar } from './ui/sidebar';
import { PlusIcon, CloudOffIcon, MessageSquare } from 'lucide-react';
import { useConfig } from '@/hooks/use-config';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

export function ChatHeader() {
  const navigate = useNavigate();
  const { open } = useSidebar();
  const { chatHistoryEnabled } = useConfig();

  const { width: windowWidth } = useWindowSize();

  return (
    <header className="sticky top-0 flex items-center gap-2 border-b bg-background px-2 py-2 md:px-3">
      <SidebarToggle />

      <div className="flex items-center gap-2">
        <MessageSquare className="h-4 w-4 text-blue-600" />
        <span className="font-medium text-sm">AI Assistant</span>
      </div>

      {(!open || windowWidth < 768) && (
        <Button
          variant="outline"
          className="order-2 ml-auto h-8 px-2 md:order-1 md:ml-0 md:h-fit md:px-2"
          onClick={() => {
            navigate('/');
          }}
        >
          <PlusIcon />
          <span className="md:sr-only">New Chat</span>
        </Button>
      )}

      {!chatHistoryEnabled && (
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="ml-auto flex items-center gap-1.5 rounded-full bg-muted px-2 py-1 text-muted-foreground text-xs">
                <CloudOffIcon className="h-3 w-3" />
                <span className="hidden sm:inline">Ephemeral</span>
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>Chat history disabled - conversations are not saved</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      )}
    </header>
  );
}
