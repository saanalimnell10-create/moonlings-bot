import { createCipheriv, createDecipheriv, createHash, randomBytes } from "node:crypto";
import { useRuntimeConfig } from "nitro/runtime-config";
import { createError, deleteCookie, getCookie, getRequestURL, setCookie, type H3Event } from "nitro/h3";

const sessionCookieName = "moonlings_discord_session";
const stateCookieName = "moonlings_discord_oauth_state";
const discordApi = "https://discord.com/api/v10";

export type DiscordUser = {
  id: string;
  username: string;
  avatar: string | null;
};

export type DiscordSession = {
  accessToken: string;
  expiresAt: number;
  user: DiscordUser;
};

export type AdminGuild = {
  id: string;
  name: string;
  icon: string | null;
};

function sessionKey(secret: string) {
  return createHash("sha256").update(secret).digest();
}

function seal(value: DiscordSession, secret: string) {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", sessionKey(secret), iv);
  const ciphertext = Buffer.concat([cipher.update(JSON.stringify(value)), cipher.final()]);
  return [iv, cipher.getAuthTag(), ciphertext].map((part) => part.toString("base64url")).join(".");
}

function unseal(value: string, secret: string): DiscordSession | null {
  try {
    const [ivValue, tagValue, ciphertextValue] = value.split(".");
    if (!ivValue || !tagValue || !ciphertextValue) return null;
    const decipher = createDecipheriv("aes-256-gcm", sessionKey(secret), Buffer.from(ivValue, "base64url"));
    decipher.setAuthTag(Buffer.from(tagValue, "base64url"));
    const plaintext = Buffer.concat([
      decipher.update(Buffer.from(ciphertextValue, "base64url")),
      decipher.final(),
    ]).toString("utf8");
    const session = JSON.parse(plaintext) as DiscordSession;
    if (!session.accessToken || !session.user?.id || !session.expiresAt || session.expiresAt <= Date.now()) return null;
    return session;
  } catch {
    return null;
  }
}

export function oauthConfig() {
  const config = useRuntimeConfig();
  const clientId = String(config.discordClientId || "");
  const clientSecret = String(config.discordClientSecret || "");
  const redirectUri = String(config.discordRedirectUri || "");
  const sessionSecret = String(config.authSessionSecret || "");
  if (!clientId || !clientSecret || !redirectUri || sessionSecret.length < 32) {
    throw createError({ statusCode: 503, statusMessage: "Discord sign-in is not configured on the server." });
  }
  return { clientId, clientSecret, redirectUri, sessionSecret };
}

export function readDiscordSession(event: H3Event) {
  const rawCookie = getCookie(event, sessionCookieName);
  const secret = String(useRuntimeConfig().authSessionSecret || "");
  if (!rawCookie || secret.length < 32) return null;
  const session = unseal(rawCookie, secret);
  if (!session) deleteCookie(event, sessionCookieName, { path: "/" });
  return session;
}

export function requireDiscordSession(event: H3Event) {
  const session = readDiscordSession(event);
  if (!session) throw createError({ statusCode: 401, statusMessage: "Sign in with Discord to continue." });
  return session;
}

function secureCookie(event: H3Event) {
  return getRequestURL(event).protocol === "https:" || process.env.NODE_ENV === "production";
}

export function saveDiscordSession(event: H3Event, session: DiscordSession) {
  const { sessionSecret } = oauthConfig();
  const maxAge = Math.max(0, Math.floor((session.expiresAt - Date.now()) / 1000));
  setCookie(event, sessionCookieName, seal(session, sessionSecret), {
    httpOnly: true,
    secure: secureCookie(event),
    sameSite: "lax",
    path: "/",
    maxAge,
  });
}

export function clearDiscordSession(event: H3Event) {
  deleteCookie(event, sessionCookieName, { path: "/" });
}

export function saveOAuthState(event: H3Event, state: string) {
  setCookie(event, stateCookieName, state, {
    httpOnly: true,
    secure: getRequestURL(event).protocol === "https:",
    sameSite: "lax",
    path: "/api/auth/discord/callback",
    maxAge: 600,
  });
}

export function readOAuthState(event: H3Event) {
  return getCookie(event, stateCookieName);
}

export function clearOAuthState(event: H3Event) {
  deleteCookie(event, stateCookieName, { path: "/api/auth/discord/callback" });
}

export async function fetchAdminGuilds(session: DiscordSession): Promise<AdminGuild[]> {
  const response = await fetch(`${discordApi}/users/@me/guilds`, {
    headers: { Authorization: `Bearer ${session.accessToken}` },
    signal: AbortSignal.timeout(8000),
  });
  if (!response.ok) {
    throw createError({ statusCode: response.status === 401 ? 401 : 502, statusMessage: "Could not verify Discord server permissions." });
  }
  const guilds = await response.json() as Array<{ id: string; name: string; icon: string | null; permissions: string }>;
  const adminBits = 8n | 32n;
  return guilds
    .filter((guild) => (BigInt(guild.permissions) & adminBits) !== 0n)
    .map(({ id, name, icon }) => ({ id, name, icon }));
}

export async function requireAdminGuild(event: H3Event, guildId: string) {
  if (!/^\d{17,20}$/.test(guildId)) {
    throw createError({ statusCode: 400, statusMessage: "A valid Discord server ID is required." });
  }
  const session = requireDiscordSession(event);
  const guilds = await fetchAdminGuilds(session);
  const guild = guilds.find((item) => item.id === guildId);
  if (!guild) throw createError({ statusCode: 403, statusMessage: "You need administrator or Manage Server permission for this server." });
  return { session, guild };
}

export async function exchangeDiscordCode(code: string, clientSecret: string, clientId: string, redirectUri: string) {
  const response = await fetch(`${discordApi}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      grant_type: "authorization_code",
      code,
      redirect_uri: redirectUri,
    }),
    signal: AbortSignal.timeout(8000),
  });
  if (!response.ok) throw createError({ statusCode: 502, statusMessage: "Discord sign-in could not be completed." });
  return response.json() as Promise<{ access_token: string; expires_in: number; token_type: string }>;
}

export async function fetchDiscordUser(accessToken: string): Promise<DiscordUser> {
  const response = await fetch(`${discordApi}/users/@me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
    signal: AbortSignal.timeout(8000),
  });
  if (!response.ok) throw createError({ statusCode: 502, statusMessage: "Discord account could not be verified." });
  const user = await response.json() as DiscordUser;
  return { id: user.id, username: user.username, avatar: user.avatar ?? null };
}

export function noStore(event: H3Event) {
  event.node.res.setHeader("Cache-Control", "private, no-store, max-age=0");
  event.node.res.setHeader("Vary", "Cookie");
}

export function statusApiConfig() {
  const config = useRuntimeConfig();
  const apiUrl = String(config.botStatusApiUrl || "");
  const apiToken = String(config.botStatusApiToken || "");
  if (!apiUrl || !apiToken) {
    throw createError({ statusCode: 503, statusMessage: "The Moonlings bot status endpoint is not configured." });
  }
  return { apiUrl, apiToken };
}
