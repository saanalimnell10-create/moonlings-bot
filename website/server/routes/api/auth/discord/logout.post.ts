import { defineHandler } from "nitro";
import { clearDiscordSession, noStore } from "../../../../utils/discord-session";

export default defineHandler((event) => {
  noStore(event);
  clearDiscordSession(event);
  return { ok: true };
});
