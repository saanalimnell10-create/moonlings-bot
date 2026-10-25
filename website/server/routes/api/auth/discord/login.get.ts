import { defineHandler } from "nitro";
import { sendRedirect } from "nitro/h3";
import { randomBytes } from "node:crypto";
import { oauthConfig, saveOAuthState } from "../../../../utils/discord-session";

export default defineHandler((event) => {
  const { clientId, redirectUri } = oauthConfig();
  const state = randomBytes(32).toString("base64url");
  saveOAuthState(event, state);
  const authorizeUrl = new URL("https://discord.com/oauth2/authorize");
  authorizeUrl.search = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: "identify guilds",
    state,
  }).toString();
  return sendRedirect(event, authorizeUrl.toString(), 302);
});
