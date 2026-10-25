import { defineHandler } from "nitro";
import { createError, getQuery } from "nitro/h3";
import { z } from "zod";
import { noStore, requireAdminGuild } from "../../../utils/discord-session";
import { requestBotControl } from "../../../utils/bot-control";

const channelsSchema = z.object({
  channels: z.array(z.object({ id: z.string(), name: z.string() })),
});

export default defineHandler(async (event) => {
  noStore(event);
  const guildId = getQuery(event).guildId;
  if (typeof guildId !== "string") {
    throw createError({ statusCode: 400, statusMessage: "A server ID is required." });
  }
  const { guild } = await requireAdminGuild(event, guildId);
  const result = await requestBotControl<unknown>(`/api/admin/guilds/${guild.id}/channels`, "GET");
  const parsed = channelsSchema.safeParse(result);
  if (!parsed.success) {
    throw createError({ statusCode: 502, statusMessage: "The bot returned an invalid channel list." });
  }
  return { guild, channels: parsed.data.channels };
});
