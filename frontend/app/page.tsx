import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ShieldCheck, Sparkles, Scale } from "lucide-react";
import { Button } from "@/components/ui/button";

const highlights = [
  {
    title: "Multi-tenancy segura",
    description: "Base preparada para isolamento por organização desde a fundação.",
    icon: ShieldCheck,
  },
  {
    title: "Fluxos jurídicos orientados",
    description: "Processos, documentos, OCR e knowledge base já mapeados no backend.",
    icon: Scale,
  },
  {
    title: "IA assistida com governança",
    description: "Camada pronta para evoluir com fontes, limites por plano e opt-in por tenant.",
    icon: Sparkles,
  },
];

export default function Home() {
  return (
    <main className="jurisai-shell min-h-screen">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col justify-center gap-16 px-6 py-16 lg:px-10">
        <div className="grid items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="space-y-8">
            <div className="inline-flex items-center rounded-full border border-primary/15 bg-primary/5 px-4 py-2 text-sm font-medium text-primary">
              Frontend MVP environment setup
            </div>
            <div className="space-y-5">
              <Image
                src="/brand/jurisai-logo.png"
                alt="JurisAI"
                width={180}
                height={180}
                priority
                className="h-16 w-auto"
              />
              <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
                JurisAI
                <span className="block text-balance text-primary">
                  Frontend SaaS jurídico em preparação.
                </span>
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-muted-foreground">
                Esta branch prepara 100% do ambiente técnico do Frontend MVP sem
                prometer telas finais antes da fundação estar pronta.
              </p>
            </div>
            <div className="flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg" className="rounded-full px-6">
                <Link href="/login">
                  Entrar
                  <ArrowRight className="ml-2 size-4" />
                </Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="rounded-full border-primary/20 bg-white/70 px-6"
              >
                <Link href="/dashboard">Ver foundation dashboard</Link>
              </Button>
            </div>
          </div>
          <div className="jurisai-panel rounded-[2rem] p-6 sm:p-8">
            <div className="grid gap-4">
              {highlights.map(({ title, description, icon: Icon }) => (
                <div
                  key={title}
                  className="rounded-2xl border border-border/60 bg-background/85 p-5"
                >
                  <div className="mb-3 inline-flex rounded-2xl bg-primary/10 p-3 text-primary">
                    <Icon className="size-5" />
                  </div>
                  <h2 className="text-lg font-semibold">{title}</h2>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    {description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
