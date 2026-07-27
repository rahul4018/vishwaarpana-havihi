import { Card, CardContent } from "@/components/ui/card";
import { ReactNode } from "react";

interface AuthCardProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export default function AuthCard({
  title,
  subtitle,
  children,
}: AuthCardProps) {
  return (
    <Card className="w-full max-w-md border shadow-xl">
      <CardContent className="space-y-6 p-8">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold tracking-tight">
            {title}
          </h1>

          {subtitle && (
            <p className="text-muted-foreground text-sm">
              {subtitle}
            </p>
          )}
        </div>

        {children}
      </CardContent>
    </Card>
  );
}