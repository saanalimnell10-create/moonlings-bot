import { defineHandler } from "nitro";
import { noStore, readDiscordSession } from "../../../../utils/discord-session";

export default defineHandler((event) => {
  noStore(event);
  const session = readDiscordSession(event);
  if (!session) return { authenticated: false, user: null };
  return { authenticated: true, user: session.user };
});
