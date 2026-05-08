import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import { useOrganizationStore } from "@/stores/organization-store";

vi.mock("next/navigation", () => ({
  usePathname: () => "/knowledge-base",
  useRouter: () => ({
    replace: vi.fn(),
  }),
}));

vi.mock("@/components/layout/logo", () => ({
  Logo: () => <div>JurisAI</div>,
}));

vi.mock("@/components/layout/theme-toggle", () => ({
  ThemeToggle: () => <button type="button">Tema</button>,
}));

vi.mock("@/components/layout/mobile-nav", () => ({
  MobileNav: () => <button type="button">Menu</button>,
}));

vi.mock("@/hooks/use-active-organization", () => ({
  useActiveOrganization: () => ({
    activeOrganization: { id: "org-1", name: "JurisAI Demo" },
  }),
}));

describe("navigation layout", () => {
  it("renders the JurisAI logo, active navigation and active tenant name", () => {
    useOrganizationStore.setState({
      activeOrganizationId: "org-1",
      availableOrganizations: [{ id: "org-1", name: "JurisAI Demo" }],
      loadStatus: "ready",
      loadError: null,
    });

    render(
      <>
        <Sidebar />
        <Topbar />
      </>,
    );

    expect(screen.getAllByText("JurisAI").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Base de conhecimento").length).toBeGreaterThan(0);
    expect(screen.getByText(/Tenant ativo:/)).toBeInTheDocument();
    expect(screen.getAllByText("JurisAI Demo").length).toBeGreaterThan(0);
    expect(screen.getAllByRole("link", { name: "Base de conhecimento" })[0]).toHaveAttribute(
      "aria-current",
      "page",
    );
  });
});
