import { Activity, Building2, Gauge, Stethoscope, type LucideIcon } from "lucide-react";

export type DashboardPath =
  | "/hospital-overview"
  | "/patient-flow"
  | "/clinical-analytics"
  | "/resource-utilization";

export interface Dashboard {
  path: DashboardPath;
  number: string;
  title: string;
  icon: LucideIcon;
  summary: string;
  focusAreas: string[];
  /**
   * Paste the Tableau Public share link here (either the /views/... link or the
   * /app/profile/.../viz/... link). Leave empty to show the placeholder.
   */
  tableauUrl: string;
}

export const DASHBOARDS: Dashboard[] = [
  {
    path: "/hospital-overview",
    number: "01",
    title: "Hospital Overview",
    icon: Building2,
    summary:
      "A high-level view of the hospital's operations, bringing the headline indicators from the dataset together in one place.",
    focusAreas: ["Headline indicators", "Department breakdown", "Trends over time"],
    tableauUrl:
      "https://public.tableau.com/views/MEDTRACK_DV_Hospital_Analytics/HospitalOverview?:showVizHome=no",
  },
  {
    path: "/patient-flow",
    number: "02",
    title: "Patient Flow",
    icon: Activity,
    summary:
      "Follows how patients move through the hospital — from admission and waiting through to treatment and discharge.",
    focusAreas: ["Admissions & discharges", "Waiting times", "Peak periods"],
    tableauUrl:
      "https://public.tableau.com/views/MEDTRACK_DV_Hospital_Analytics/PatientFlow?:showVizHome=no",
  },
  {
    path: "/clinical-analytics",
    number: "03",
    title: "Clinical Analytics",
    icon: Stethoscope,
    summary:
      "Explores clinical patterns in the dataset, such as diagnoses, treatments and outcomes across patient groups.",
    focusAreas: ["Diagnosis patterns", "Treatment outcomes", "Patient demographics"],
    tableauUrl:
      "https://public.tableau.com/views/MEDTRACK_DV_Hospital_Analytics/ClinicalAnalytics?:showVizHome=no",
  },
  {
    path: "/resource-utilization",
    number: "04",
    title: "Resource Utilization",
    icon: Gauge,
    summary:
      "Looks at how hospital resources such as beds, staff and equipment are used, to highlight capacity and efficiency.",
    focusAreas: ["Bed occupancy", "Staff allocation", "Equipment usage"],
    tableauUrl:
      "https://public.tableau.com/views/MEDTRACK_DV_Hospital_Analytics/ResourceUtilization?:showVizHome=no",
  },
];

export function getDashboard(path: DashboardPath): Dashboard {
  const found = DASHBOARDS.find((d) => d.path === path);
  if (!found) throw new Error(`Unknown dashboard: ${path}`);
  return found;
}

/**
 * Turns a Tableau Public share link into an embeddable URL.
 * Returns null when the link is empty or not a Tableau Public link.
 */
export function toTableauEmbedUrl(raw: string): string | null {
  const value = raw.trim();
  if (!value) return null;

  let url: URL;
  try {
    url = new URL(value);
  } catch {
    return null;
  }

  if (url.hostname !== "public.tableau.com") return null;

  let workbook: string | undefined;
  let sheet: string | undefined;

  const parts = url.pathname.split("/").filter(Boolean);
  const vizIndex = parts.indexOf("viz");
  const viewsIndex = parts.indexOf("views");

  if (viewsIndex !== -1) {
    workbook = parts[viewsIndex + 1];
    sheet = parts[viewsIndex + 2];
  } else if (vizIndex !== -1) {
    workbook = parts[vizIndex + 1];
    sheet = parts[vizIndex + 2];
  }

  if (!workbook || !sheet) return null;

  return `https://public.tableau.com/views/${workbook}/${sheet}?:showVizHome=no&:embed=true&:toolbar=yes&:tabs=no`;
}
