import { Link } from "@tanstack/react-router";
import { ArrowLeft, ArrowRight } from "lucide-react";

import { PageHeader } from "@/components/page-header";
import { TableauEmbed } from "@/components/tableau-embed";
import { DASHBOARDS, getDashboard, type DashboardPath } from "@/lib/dashboards";

export function DashboardView({ path }: { path: DashboardPath }) {
  const dashboard = getDashboard(path);
  const index = DASHBOARDS.findIndex((d) => d.path === path);
  const prev = DASHBOARDS[index - 1];
  const next = DASHBOARDS[index + 1];

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow={`Dashboard ${dashboard.number}`}
        title={dashboard.title}
        description={dashboard.summary}
      >
        <div className="mt-5 flex flex-wrap gap-2">
          {dashboard.focusAreas.map((area) => (
            <span
              key={area}
              className="rounded-full bg-accent px-3 py-1 text-xs font-medium text-accent-foreground"
            >
              {area}
            </span>
          ))}
        </div>
      </PageHeader>

      <TableauEmbed title={dashboard.title} url={dashboard.tableauUrl} />

      <nav className="grid gap-4 sm:grid-cols-2">
        {prev ? (
          <Link
            to={prev.path}
            className="group flex items-center gap-3 rounded-xl border bg-card p-4 shadow-card transition hover:border-primary/40"
          >
            <ArrowLeft className="size-4 text-primary transition group-hover:-translate-x-0.5" />
            <span>
              <span className="block text-xs text-muted-foreground">Previous</span>
              <span className="font-medium text-foreground">{prev.title}</span>
            </span>
          </Link>
        ) : (
          <span />
        )}
        {next && (
          <Link
            to={next.path}
            className="group flex items-center justify-end gap-3 rounded-xl border bg-card p-4 text-right shadow-card transition hover:border-primary/40"
          >
            <span>
              <span className="block text-xs text-muted-foreground">Next</span>
              <span className="font-medium text-foreground">{next.title}</span>
            </span>
            <ArrowRight className="size-4 text-primary transition group-hover:translate-x-0.5" />
          </Link>
        )}
      </nav>
    </div>
  );
}
