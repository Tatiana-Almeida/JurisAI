import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { LoginForm } from "@/components/auth/login-form";
import { apiClient } from "@/lib/api/client";
import { useAuthStore } from "@/stores/auth-store";

const pushMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

vi.mock("sonner", () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

describe("login form", () => {
  beforeEach(() => {
    window.localStorage.clear();
    pushMock.mockReset();
    useAuthStore.setState({
      status: "unauthenticated",
      user: null,
      tokens: null,
      isBootstrapped: true,
    });
  });

  it("validates required fields", async () => {
    render(<LoginForm />);

    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByText("Introduza um email valido.")).toBeInTheDocument();
    expect(
      await screen.findByText("A password deve ter pelo menos 8 caracteres."),
    ).toBeInTheDocument();
  });

  it("calls the login API, bootstraps auth and redirects", async () => {
    const postSpy = vi
      .spyOn(apiClient, "post")
      .mockResolvedValueOnce({ data: { access: "access-token", refresh: "refresh-token" } });
    const getSpy = vi.spyOn(apiClient, "get").mockResolvedValueOnce({
      data: { email: "advogado@example.com", role: "advogado" },
    });

    render(<LoginForm nextPath="/dashboard" />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "advogado@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    await waitFor(() => {
      expect(postSpy).toHaveBeenCalled();
      expect(getSpy).toHaveBeenCalled();
      expect(pushMock).toHaveBeenCalledWith("/dashboard");
    });

    expect(useAuthStore.getState().status).toBe("authenticated");
    expect(useAuthStore.getState().tokens?.access).toBe("access-token");
    expect(useAuthStore.getState().user?.email).toBe("advogado@example.com");
  });
});
