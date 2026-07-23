/**
 * Application Environment Configuration
 * Centralized access to environment variables.
 */

const requiredEnv = (value: string | undefined, key: string): string => {
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }

  return value;
};

export const env = {
  APP_NAME:
    process.env.NEXT_PUBLIC_APP_NAME ?? "Vishwaarpana Havihi",

  APP_ENV:
    process.env.NEXT_PUBLIC_APP_ENV ?? "development",

  API_BASE_URL: requiredEnv(
    process.env.NEXT_PUBLIC_API_BASE_URL,
    "NEXT_PUBLIC_API_BASE_URL"
  ),

  API_TIMEOUT: Number(
    process.env.NEXT_PUBLIC_API_TIMEOUT ?? 30000
  ),

  DEFAULT_LANGUAGE:
    process.env.NEXT_PUBLIC_DEFAULT_LANGUAGE ?? "en",

  SUPPORTED_LANGUAGES: ["en", "kn"] as const,

  ENABLE_QUERY_DEVTOOLS:
    process.env.NEXT_PUBLIC_ENABLE_QUERY_DEVTOOLS === "true",
};

export type SupportedLanguage =
  typeof env.SUPPORTED_LANGUAGES[number];