import { NextResponse, type NextRequest } from "next/server";

const PUBLIC_ROUTES = new Set(["/", "/login"]);
const PRIVATE_PREFIXES = [
  "/dashboard",
  "/cases",
  "/clients",
  "/documents",
  "/ocr",
  "/knowledge-base",
  "/deadlines",
  "/calendar",
  "/finance",
  "/billing",
  "/settings",
  "/client-portal",
];

function isProtectedPath(pathname: string) {
  return PRIVATE_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSessionHint = request.cookies.get("jurisai-has-session")?.value === "1";

  if (PUBLIC_ROUTES.has(pathname) && pathname === "/login" && hasSessionHint) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  if (isProtectedPath(pathname) && !hasSessionHint) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("next", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|brand|.*\\..*).*)"],
};
