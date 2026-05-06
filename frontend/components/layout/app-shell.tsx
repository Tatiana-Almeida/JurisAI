import { ProtectedRoute } from "@/components/auth/protected-route";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";

type AppShellProps = {
  children: React.ReactNode;
  allowedRoles?: string[];
  portalOnly?: boolean;
};

export function AppShell({ children, allowedRoles, portalOnly }: AppShellProps) {
  return (
    <ProtectedRoute allowedRoles={allowedRoles} portalOnly={portalOnly}>
      <div className="min-h-screen bg-transparent lg:grid lg:grid-cols-[18rem_1fr]">
        <Sidebar />
        <div className="min-h-screen">
          <Topbar />
          <main className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
}
