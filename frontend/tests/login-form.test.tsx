import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { LoginForm } from "@/components/auth/login-form";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe("login form", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("validates required fields", async () => {
    render(<LoginForm />);

    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByText("Introduza um email válido.")).toBeInTheDocument();
    expect(
      await screen.findByText("A password deve ter pelo menos 8 caracteres."),
    ).toBeInTheDocument();
  });
});
