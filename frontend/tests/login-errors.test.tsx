import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
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

describe("login errors", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    pushMock.mockReset();
    useAuthStore.setState({
      status: "unauthenticated",
      user: null,
      tokens: null,
      isBootstrapped: true,
    });
  });

  it("shows a clear invalid credentials message", async () => {
    vi.spyOn(apiClient, "post").mockRejectedValueOnce({
      status: 401,
      message: "Sessao expirada ou credenciais invalidas.",
    });

    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "advogado@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(
      await screen.findByText("Credenciais invalidas. Confirme email e password."),
    ).toBeInTheDocument();
  });

  it("shows a friendly offline message when backend is unavailable", async () => {
    vi.spyOn(apiClient, "post").mockRejectedValueOnce({
      status: 0,
      message: "Nao foi possivel contactar a API configurada.",
    });

    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "advogado@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(
      await screen.findByText(
        "Nao foi possivel contactar a API configurada. Confirme staging, rede e CORS.",
      ),
    ).toBeInTheDocument();
  });

  it("disables submit while the first login request is pending", async () => {
    let resolveRequest: ((value: { data: { access: string; refresh: string } }) => void) | undefined;
    vi.spyOn(apiClient, "post").mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          resolveRequest = resolve;
        }) as ReturnType<typeof apiClient.post>,
    );
    vi.spyOn(apiClient, "get").mockResolvedValueOnce({
      data: { email: "advogado@example.com", role: "advogado" },
    });

    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText("Email"), {
      target: { value: "advogado@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Password"), {
      target: { value: "password123" },
    });

    const submitButton = screen.getByRole("button", { name: "Entrar" });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "A entrar..." })).toBeDisabled();
    });

    await act(async () => {
      resolveRequest?.({ data: { access: "token", refresh: "refresh" } });
    });

    await waitFor(() => {
      expect(pushMock).toHaveBeenCalledWith("/dashboard");
    });
  });
});
