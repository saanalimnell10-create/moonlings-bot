import { useRuntimeConfig } from "nitro/runtime-config";
import { createError } from "nitro/h3";

export function botControlConfig() {
  const config = useRuntimeConfig();
  const apiUrl = String(config.botControlApiUrl || "").replace(/\/+$/, "");
  const apiToken = String(config.botControlApiToken || "");
  if (!apiUrl || apiToken.length < 32) {
    throw createError({ statusCode: 503, statusMessage: "Welcome settings are not connected to the Moonlings bot yet." });
  }
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(apiUrl);
  } catch {
    throw createError({ statusCode: 503, statusMessage: "The Moonlings bot control URL is invalid." });
  }
  if (parsedUrl.protocol !== "https:" && !["localhost", "127.0.0.1"].includes(parsedUrl.hostname)) {
    throw createError({ statusCode: 503, statusMessage: "The Moonlings bot control endpoint must use HTTPS." });
  }
  return { apiUrl, apiToken };
}

export async function requestBotControl<T>(path: string, method: "GET" | "PUT", body?: unknown): Promise<T> {
  const { apiUrl, apiToken } = botControlConfig();
  let response: Response;
  try {
    response = await fetch(`${apiUrl}${path}`, {
      method,
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${apiToken}`,
        ...(body ? { "Content-Type": "application/json" } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
      signal: AbortSignal.timeout(8000),
    });
  } catch {
    throw createError({ statusCode: 502, statusMessage: "Could not reach the Moonlings bot service." });
  }
  const result = await response.json().catch(() => null);
  if (!response.ok) {
    const statusCode = [400, 403, 404].includes(response.status) ? response.status : 502;
    throw createError({ statusCode, statusMessage: result?.error || "The Moonlings bot could not process this request." });
  }
  return result as T;
}
