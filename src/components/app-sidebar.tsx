import { Link, useRouterState } from "@tanstack/react-router";
import { BookOpen, FlaskConical, HeartPulse, LayoutDashboard } from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { DASHBOARDS } from "@/lib/dashboards";

const projectLinks = [
  { title: "About Project", url: "/about", icon: BookOpen },
  { title: "Methodology & Limitations", url: "/methodology", icon: FlaskConical },
] as const;

export function AppSidebar() {
  const { state, isMobile, setOpenMobile } = useSidebar();
  const collapsed = state === "collapsed" && !isMobile;
  const currentPath = useRouterState({ select: (r) => r.location.pathname });
  const close = () => isMobile && setOpenMobile(false);

  return (
    <Sidebar collapsible="icon" className="border-r-0">
      <div className="flex h-full flex-col bg-gradient-sidebar">
        <SidebarHeader className="px-3 pt-5 pb-4">
          <Link to="/" onClick={close} className="flex items-center gap-3">
            <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-sidebar-primary text-sidebar-primary-foreground shadow-elegant">
              <HeartPulse className="size-5" />
            </span>
            {!collapsed && (
              <span className="flex flex-col leading-tight">
                <span className="font-display text-lg font-semibold tracking-tight text-sidebar-foreground">
                  MedTrack_DV
                </span>
                <span className="text-xs text-sidebar-muted">Healthcare Analytics</span>
              </span>
            )}
          </Link>
        </SidebarHeader>

        <SidebarContent className="px-1">
          <SidebarGroup>
            <SidebarGroupContent>
              <SidebarMenu>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    asChild
                    isActive={currentPath === "/"}
                    tooltip="Home"
                    className="h-10"
                  >
                    <Link to="/" onClick={close}>
                      <LayoutDashboard />
                      <span>Home</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>

          <SidebarGroup>
            <SidebarGroupLabel className="text-sidebar-muted">Dashboards</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {DASHBOARDS.map((d) => (
                  <SidebarMenuItem key={d.path}>
                    <SidebarMenuButton
                      asChild
                      isActive={currentPath === d.path}
                      tooltip={d.title}
                      className="h-10"
                    >
                      <Link to={d.path} onClick={close}>
                        <d.icon />
                        <span>{d.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>

          <SidebarGroup>
            <SidebarGroupLabel className="text-sidebar-muted">Project</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {projectLinks.map((item) => (
                  <SidebarMenuItem key={item.url}>
                    <SidebarMenuButton
                      asChild
                      isActive={currentPath === item.url}
                      tooltip={item.title}
                      className="h-10"
                    >
                      <Link to={item.url} onClick={close}>
                        <item.icon />
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
      </div>
    </Sidebar>
  );
}
