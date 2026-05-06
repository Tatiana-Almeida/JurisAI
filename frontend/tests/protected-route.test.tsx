import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ProtectedRoute } from "@/components/auth/protected-route";
import { useAuthStore } from "@/stores/auth-store";

const replaceMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    replace: replaceMock,
  }),
  usePathname: () => "/dashboard",
}));

describe("protected route", () => {
  beforeEach(() => {
    replaceMock.mockReset();
    useAuthStore.setState({
      status: "idle",
      user: null,
      tokens: null,
      isBootstrapped: false,
    });
  });

  it("shows a loading screen while auth is bootstrapping", () => {
    render(
      <ProtectedRoute>
        <div>Área privada</div>
      </ProtectedRoute>,
    );

    expect(screen.getByText("A preparar sessão")).toBeInTheDocument();
  });

  it("redirects unauthenticated users to login", async () => {
    useAuthStore.setState({
      status: "unauthenticated",
      user: null,
      tokens: null,
      isBootstrapped: true,
    });

    render(
      <ProtectedRoute>
        <div>Área privada</div>
      </ProtectedRoute>,
    );

    await waitFor(() => {
      expect(replaceMock).toHaveBeenCalledWith("/login?next=%2Fdashboard");
    });
  });

  it("renders children for authenticated users", () => {
    useAuthStore.setState({
      status: "authenticated",
      user: { email: "advogado@example.com", role: "advogado" },
      tokens: { access: "access" },
      isBootstrapped: true,
    });

    render(
      <ProtectedRoute>
        <div>Área privada</div>
      </ProtectedRoute>,
    );

    expect(screen.getByText("Área privada")).toBeInTheDocument();
  });
});
