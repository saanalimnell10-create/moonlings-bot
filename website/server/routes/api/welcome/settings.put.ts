import { defineHandler } from "nitro";
import { createError, readBody } from "nitro/h3";
import { z } from "zod";
import { noStore, requireAdminGuild } from "../../../utils/discord-session";
import { requestBotControl } from "../../../utils/bot-control";

const settingsInputSchema = z.object({
  guildId: z.string().regex(/^\d{17,20}$/),
  welcomeChannelId: z.string().regex(/^\d{17,20}$/),
  welcomeText: z.string().trim().min(1).max(1800),
  goodbyeChannelId: z.string().regex(/^\d{17,20}$/),
  goodbyeText: z.string().trim().min(1).max(1800),
});

export default defineHandler(async (event) => {
  noStore(event);
  const body = await readBody<unknown>(event);
  const parsed = settingsInputSchema.safeParse(body);
  if (!parsed.success) {
    throw createError({ statusCode: 400, statusMessage: "Choose channels and enter messages under 1,800 characters." });
  }
  const { guild } = await requireAdminGuild(event, parsed.data.guildId);
  const result = await requestBotControl<{ ok: boolean }>(`/api/admin/guilds/${guild.id}/welcome`, "PUT", {
    welcomeChannelId: parsed.data.welcomeChannelId,
    welcomeText: parsed.data.welcomeText,
    goodbyeChannelId: parsed.data.goodbyeChannelId,
    goodbyeText: parsed.data.goodbyeText,
  });
  return result;
});
