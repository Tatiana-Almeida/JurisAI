"use client";

import { AlertCircle, Building2, ChevronDown } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useOrganizationStore } from "@/stores/organization-store";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function OrganizationSwitcher() {
  const router = useRouter();
  const {
    activeOrganizationId,
    availableOrganizations,
    loadError,
    loadStatus,
    setActiveOrganization,
  } = useOrganizationStore();

  const activeOrganization = availableOrganizations.find((item) => item.id === activeOrganizationId);

  if (loadStatus === "error") {
    return (
      <div className="flex min-w-[240px] items-center gap-2 rounded-2xl border border-destructive/25 bg-destructive/5 px-3 py-2 text-sm text-destructive">
        <AlertCircle className="size-4 shrink-0" />
        <span className="line-clamp-2">{loadError ?? "Falha ao carregar organizacoes."}</span>
      </div>
    );
  }

  if (availableOrganizations.length === 0) {
    return (
      <div className="flex min-w-[240px] items-center gap-2 rounded-2xl border border-border/70 bg-background/80 px-3 py-2 text-sm text-muted-foreground">
        <Building2 className="size-4 shrink-0 text-primary" />
        <span className="line-clamp-2">
          Nenhuma organizacao ativa. Confirme memberships no backend ou no Django Admin.
        </span>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      <Select
        value={activeOrganizationId ?? ""}
        onValueChange={(value) => {
          if (value === activeOrganizationId) {
            return;
          }

          setActiveOrganization(value);
          const organization = availableOrganizations.find((item) => item.id === value);
          toast.success("Organizacao ativa atualizada.", {
            description: organization?.name ?? "Tenant atualizado com sucesso.",
          });
          router.replace("/dashboard");
        }}
      >
        <SelectTrigger className="min-w-[220px] rounded-full border-border/70 bg-background/80">
          <div className="flex items-center gap-2">
            <Building2 className="size-4 text-primary" />
            <SelectValue placeholder="Selecionar organizacao" />
          </div>
          <ChevronDown className="size-4 opacity-60" />
        </SelectTrigger>
        <SelectContent>
          {availableOrganizations.map((organization) => (
            <SelectItem key={organization.id} value={organization.id}>
              {organization.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <p className="px-3 text-xs text-muted-foreground">
        Organizacao atual: {activeOrganization?.name ?? "por selecionar"}
      </p>
    </div>
  );
}
