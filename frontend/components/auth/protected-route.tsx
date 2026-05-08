"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { LoadingScreen } from "@/components/shared/loading-screen";
import { ForbiddenState } from "@/components/shared/forbidden-state";
import { UnauthorizedState } from "@/components/shared/unauthorized-state";
import { useAuthStore } from "@/stores/auth-store";

type ProtectedRouteProps = {
  children: React.ReactNode;
  allowedRoles?: string[];
  portalOnly?: boolean;
};

export function ProtectedRoute({
  children,
  allowedRoles,
  portalOnly = false,
}: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const status = useAuthStore((state) => state.status);
  const user = useAuthStore((state) => state.user);
  const isBootstrapped = useAuthStore((state) => state.isBootstrapped);

  useEffect(() => {
    if (isBootstrapped && status === "unauthenticated") {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [isBootstrapped, pathname, router, status]);

  if (!isBootstrapped || status === "idle" || status === "loading") {
    return <LoadingScreen />;
  }

  if (status !== "authenticated" || !user) {
    return <UnauthorizedState />;
  }

  if (portalOnly && user.role !== "cliente") {
    return <ForbiddenState />;
  }

  if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(user.role ?? "")) {
    return <ForbiddenState />;
  }

  return <>{children}</>;
}
