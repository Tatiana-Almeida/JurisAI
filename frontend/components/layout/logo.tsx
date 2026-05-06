"use client";

import Image from "next/image";
import Link from "next/link";
import { cn } from "@/lib/utils";

type LogoProps = {
  href?: string;
  size?: "sidebar" | "auth" | "compact";
  className?: string;
  withWordmark?: boolean;
};

const sizes = {
  sidebar: {
    width: 148,
    height: 44,
    className: "h-10 w-auto",
  },
  auth: {
    width: 176,
    height: 52,
    className: "h-12 w-auto",
  },
  compact: {
    width: 124,
    height: 38,
    className: "h-9 w-auto",
  },
} as const;

export function Logo({
  href = "/",
  size = "sidebar",
  className,
  withWordmark = true,
}: LogoProps) {
  const asset = sizes[size];

  return (
    <Link
      href={href}
      className={cn("inline-flex items-center gap-3", className)}
      aria-label="JurisAI"
    >
      <Image
        src="/brand/jurisai-logo.png"
        alt="Logotipo do JurisAI"
        width={asset.width}
        height={asset.height}
        className={asset.className}
        priority
      />
      {!withWordmark ? (
        <span className="sr-only">JurisAI</span>
      ) : null}
    </Link>
  );
}
