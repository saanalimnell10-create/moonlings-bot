import { defineHandler } from "nitro";
import { createError, getQuery } from "nitro/h3";
import { z } from "zod";
import { noStore, requireAdminGuild, statusApiConfig } from "../../../utils/discord-session";

const threatStatusSchema = z.object({
  level: z.string().min(1).max(80),
  mode: z.string().max(80).optional(),
  protections: z.record(z.boolean()).default({}),
  updatedAt: z.string().optional(),
  recentEvents: z.array(z.object({
    id: z.string().optional(),
    message: z.string().min(1).max(180),
    at: z.string().optional(),
  })).max(10).default([]),
});

export default defineHandler(async (event) => {
  noStore(event);
  const query = getQuery(event);
  const guildId = typeof query.guildId === "string" ? query.guildId : "";
  const { guild } = await requireAdminGuild(event, guildId);
  const { apiUrl, apiToken } = statusApiConfig();
  const parsedUrl = new URL(apiUrl);
  const isLocalDevelopment = parsedUrl.hostname === "localhost" || parsedUrl.hostname === "127.0.0.1";
  if (parsedUrl.protocol !== "https:" && !isLocalDevelopment) {
    throw createError({ statusCode: 503, statusMessage: "The bot status endpoint must use HTTPS." });
  }

  let response: Response;
  try {
    response = await fetch(`${apiUrl.replace(/\/$/, "")}/guilds/${guildId}/threat-status`, {
      headers: { Authorization: `Bearer ${apiToken}`, Accept: "application/json" },
      signal: AbortSignal.timeout(8000),
    });
  } catch {
    throw createError({ statusCode: 502, statusMessage: "Could not connect to the Moonlings bot status service." });
  }
  if (!response.ok) {
    throw createError({
      statusCode: response.status === 404 ? 404 : 502,
      statusMessage: response.status === 404 ? "Moonlings has no threat status for this server yet." : "The Moonlings bot status service is unavailable.",
    });
  }

  const payload = await response.json().catch(() => null);
  const parsed = threatStatusSchema.safeParse(payload);
  if (!parsed.success) {
    throw createError({ statusCode: 502, statusMessage: "The bot status response did not match the expected format." });
  }
  return {
    guild,
    level: parsed.data.level,
    mode: parsed.data.mode ?? null,
    protections: parsed.data.protections,
    updatedAt: parsed.data.updatedAt ?? null,
    recentEvents: parsed.data.recentEvents,
  };
});
