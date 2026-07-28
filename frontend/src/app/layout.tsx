import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import "./globals.css";

import AppProvider from "@/providers/AppProvider";
import { env } from "@/config/env";
import { Toaster } from "@/components/ui/sonner";
import { AuthInitializer } from "@/components/auth/AuthInitializer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: env.APP_NAME,
    template: `%s | ${env.APP_NAME}`,
  },
  description:
    "Vishwaarpana Havihi - Smart Temple Management Platform",
  applicationName: env.APP_NAME,
  keywords: [
    "Temple",
    "Pooja",
    "Booking",
    "Priest",
    "Hindu",
    "Ritual",
    "Kannada",
    "India",
  ],
};

interface RootLayoutProps {
  children: React.ReactNode;
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

          {children}

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