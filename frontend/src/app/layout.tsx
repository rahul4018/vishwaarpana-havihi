import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import type { ReactNode } from "react";

import "./globals.css";

import { AuthInitializer } from "@/components/auth/AuthInitializer";
import { Toaster } from "@/components/ui/sonner";
import { env } from "@/config/env";
import AppProvider from "@/providers/AppProvider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000"
  ),

  title: {
    default: env.APP_NAME,
    template: `%s | ${env.APP_NAME}`,
  },

  description:
    "Vishwaarpana Havihi - Smart Temple Management Platform",

  applicationName: env.APP_NAME,

  keywords: [
    "Temple",
    "Temple Management",
    "Pooja",
    "Booking",
    "Priest",
    "Hindu",
    "Ritual",
    "Kannada",
    "India",
  ],

  authors: [
    {
      name: "SkillCheckHub IT Solutions Pvt Ltd",
    },
  ],

  creator: "SkillCheckHub IT Solutions Pvt Ltd",

  openGraph: {
    title: env.APP_NAME,
    description:
      "Vishwaarpana Havihi - Smart Temple Management Platform",
    siteName: env.APP_NAME,
    type: "website",
    locale: "en_IN",
  },

  twitter: {
    card: "summary_large_image",
    title: env.APP_NAME,
    description:
      "Vishwaarpana Havihi - Smart Temple Management Platform",
  },

  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
};

interface RootLayoutProps {
  children: ReactNode;
}

export default function RootLayout({
  children,
}: Readonly<RootLayoutProps>) {
  return (
    <html
      lang={env.DEFAULT_LANGUAGE}
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable}`}
    >
      <body className="min-h-screen bg-background font-sans antialiased">
        <AppProvider>
          <AuthInitializer />

          <main className="min-h-screen">
            {children}
          </main>

          <Toaster
            position="top-right"
            richColors
            closeButton
            duration={4000}
          />
        </AppProvider>
      </body>
    </html>
  );
}