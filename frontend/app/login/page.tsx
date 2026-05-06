import { LoginForm } from "@/components/auth/login-form";

type LoginPageProps = {
  searchParams?: Promise<{
    next?: string;
  }>;
};

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const params = (await searchParams) ?? {};
  const nextPath = typeof params.next === "string" ? params.next : undefined;

  return (
    <main className="jurisai-shell flex min-h-screen items-center justify-center px-6 py-16">
      <LoginForm nextPath={nextPath} />
    </main>
  );
}
