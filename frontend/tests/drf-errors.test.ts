import { describe, expect, it, vi } from "vitest";
import {
  getDRFErrorMessage,
  getNonFieldErrors,
  isDRFValidationError,
  mapDRFErrorsToForm,
} from "@/lib/errors/drf";

describe("drf error helpers", () => {
  const fieldError = {
    response: {
      data: {
        email: ["Este email já existe."],
        non_field_errors: ["Credenciais inválidas."],
      },
    },
  };

  it("detects DRF validation errors", () => {
    expect(isDRFValidationError(fieldError)).toBe(true);
  });

  it("extracts non field errors", () => {
    expect(getNonFieldErrors(fieldError)).toEqual(["Credenciais inválidas."]);
  });

  it("maps DRF errors to RHF", () => {
    const setError = vi.fn();
    mapDRFErrorsToForm(fieldError, setError);

    expect(setError).toHaveBeenCalledWith("email", {
      type: "server",
      message: "Este email já existe.",
    });
    expect(setError).toHaveBeenCalledWith("root", {
      type: "server",
      message: "Credenciais inválidas.",
    });
  });

  it("returns a message from DRF payload", () => {
    expect(getDRFErrorMessage(fieldError)).toBe("Credenciais inválidas.");
  });
});
