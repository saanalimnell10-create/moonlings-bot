import { timingSafeEqual } from "node:crypto";
import { defineHandler } from "nitro";
import { createError, getQuery, sendRedirect } from "nitro/h3";
import {
  clearOAuthState,
  exchangeDiscordCode,
  fetchDiscordUser,
  oauthConfig,
  readOAuthState,
  saveDiscordSession,
} from "../../../../utils/discord-session";

export default defineHandler(async (event) => {
  const query = getQuery(event);
  const code = typeof query.code === "string" ? query.code : "";
  const state = typeof query.state === "string" ? query.state : "";
  const savedState = readOAuthState(event) || "";
  clearOAuthState(event);

  const supplied = Buffer.from(state);
  const expected = Buffer.from(savedState);
  if (!code || !state || supplied.length !== expected.length || !timingSafeEqual(supplied, expected)) {
    throw createError({ statusCode: 400, statusMessage: "Discord sign-in could not be verified. Please try again." });
  }

  const config = oauthConfig();
  const token = await exchangeDiscordCode(code, config.clientSecret, config.clientId, config.redirectUri);
  const user = await fetchDiscordUser(token.access_token);
  saveDiscordSession(event, {
    accessToken: token.access_token,
    expiresAt: Date.now() + token.expires_in * 1000,
    user,
  });

  return sendRedirect(event, "/threat-center?connected=1", 302);
});
