import { defineHandler } from "nitro";
import { createError, getQuery } from "nitro/h3";
import { z } from "zod";
import { noStore, requireAdminGuild } from "../../../utils/discord-session";
import { requestBotControl } from "../../../utils/bot-control";

const settingsSchema = z.object({
  welcomeChannelId: z.string().nullable(),
  welcomeText: z.string(),
  goodbyeChannelId: z.string().nullable(),
  goodbyeText: z.string(),
});

export default defineHandler(async (event) => {
  noStore(event);
  const guildId = getQuery(event).guildId;
  if (typeof guildId !== "string") {
    throw createError({ statusCode: 400, statusMessage: "A server ID is required." });
  }
  const { guild } = await requireAdminGuild(event, guildId);
  const result = await requestBotControl<unknown>(`/api/admin/guilds/${guild.id}/welcome`, "GET");
  const parsed = settingsSchema.safeParse(result);
  if (!parsed.success) {
    throw createError({ statusCode: 502, statusMessage: "The bot returned invalid welcome settings." });
  }
  return { guild, settings: parsed.data };
});
