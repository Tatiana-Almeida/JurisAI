import {
  BriefcaseBusiness,
  CalendarDays,
  CircleDollarSign,
  FileText,
  FolderSearch,
  Gauge,
  Landmark,
  LayoutDashboard,
  ScanSearch,
  Settings,
  ShieldCheck,
  Users,
} from "lucide-react";

export const NAVIGATION_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/cases", label: "Processos", icon: BriefcaseBusiness },
  { href: "/clients", label: "Clientes", icon: Users },
  { href: "/documents", label: "Documentos", icon: FileText },
  { href: "/ocr", label: "OCR", icon: ScanSearch },
  { href: "/knowledge-base", label: "Knowledge Base", icon: FolderSearch },
  { href: "/deadlines", label: "Prazos", icon: ShieldCheck },
  { href: "/calendar", label: "Calendário", icon: CalendarDays },
  { href: "/finance", label: "Financeiro", icon: CircleDollarSign },
  { href: "/billing", label: "Billing", icon: Landmark },
  { href: "/client-portal", label: "Portal do Cliente", icon: Gauge },
  { href: "/settings", label: "Configurações", icon: Settings },
] as const;
