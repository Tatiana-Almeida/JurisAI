export const APP_NAME =
  process.env.NEXT_PUBLIC_APP_NAME?.trim() || "JurisAI";

export const FRONTEND_STATUS = {
  backend: "advanced",
  frontend: "environment setup",
  billing: "pending",
  ai: "partial",
  staging: "partial",
} as const;
