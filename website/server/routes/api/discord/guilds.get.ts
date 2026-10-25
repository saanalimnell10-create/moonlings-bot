import { defineHandler } from "nitro";
import { createError } from "nitro/h3";
import { fetchAdminGuilds, noStore, requireDiscordSession } from "../../../utils/discord-session";

export default defineHandler(async (event) => {
  noStore(event);
  const session = requireDiscordSession(event);
  try {
    return { guilds: await fetchAdminGuilds(session) };
  } catch (error) {
    if (error && typeof error === "object" && "statusCode" in error && error.statusCode === 401) {
      throw createError({ statusCode: 401, statusMessage: "Your Discord session expired. Please sign in again." });
    }
    throw error;
  }
});
