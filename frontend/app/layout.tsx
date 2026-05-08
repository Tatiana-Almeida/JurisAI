import type { Metadata } from "next";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Providers } from "@/app/providers";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "JurisAI",
    template: "%s | JurisAI",
  },
  description:
    "Frontend MVP foundation for the JurisAI multi-tenant legal SaaS platform.",
  applicationName: "JurisAI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-PT" suppressHydrationWarning className="h-full antialiased">
      <body className="min-h-full">
        <Providers>
          <TooltipProvider>{children}</TooltipProvider>
        </Providers>
      </body>
    </html>
  );
}
