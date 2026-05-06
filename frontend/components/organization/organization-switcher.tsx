"use client";

import { Building2, ChevronDown } from "lucide-react";
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
  const { activeOrganizationId, availableOrganizations, setActiveOrganization } =
    useOrganizationStore();

  const hasOrganizations = availableOrganizations.length > 0;

  return (
    <Select
      value={activeOrganizationId ?? ""}
      onValueChange={(value) => {
        setActiveOrganization(value);
        const organization = availableOrganizations.find((item) => item.id === value);
        toast.success("Organização ativa atualizada.", {
          description: organization?.name ?? "Tenant atualizado com sucesso.",
        });
        router.replace("/dashboard");
      }}
      disabled={!hasOrganizations}
    >
      <SelectTrigger className="min-w-[220px] rounded-full border-border/70 bg-background/80">
        <div className="flex items-center gap-2">
          <Building2 className="size-4 text-primary" />
          <SelectValue placeholder={hasOrganizations ? "Selecionar organização" : "Tenant pendente"} />
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
  );
}
