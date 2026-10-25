export type DiscordUser = {
  id: string;
  username: string;
  avatar: string | null;
};

export type DiscordSession = {
  authenticated: boolean;
  user: DiscordUser | null;
};

export type AdminGuild = {
  id: string;
  name: string;
  icon: string | null;
};

export type ThreatStatus = {
  guild: AdminGuild;
  level: string;
  mode: string | null;
  protections: Record<string, boolean>;
  updatedAt: string | null;
  recentEvents: Array<{ id?: string; message: string; at?: string }>;
};

export type WelcomeSettings = {
  welcomeChannelId: string | null;
  welcomeText: string;
  goodbyeChannelId: string | null;
  goodbyeText: string;
};

export type WelcomeChannel = {
  id: string;
  name: string;
};

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    credentials: "same-origin",
    headers: { Accept: "application/json", ...init?.headers },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(body?.statusMessage || body?.message || "The Threat Center request failed.");
  }
  return body as T;
}

export function getDiscordSession() {
  return apiRequest<DiscordSession>("/api/auth/discord/session");
}

export async function getAdminGuilds() {
  const result = await apiRequest<{ guilds: AdminGuild[] }>("/api/discord/guilds");
  return result.guilds;
}

export function getThreatStatus(guildId: string) {
  return apiRequest<ThreatStatus>(`/api/threat/status?${new URLSearchParams({ guildId })}`);
}

export function logoutDiscord() {
  return apiRequest<{ ok: boolean }>("/api/auth/discord/logout", { method: "POST" });
}

export function getWelcomeChannels(guildId: string) {
  return apiRequest<{ guild: AdminGuild; channels: WelcomeChannel[] }>(
    "/api/welcome/channels?" + new URLSearchParams({ guildId }),
  );
}

export function getWelcomeSettings(guildId: string) {
  return apiRequest<{ guild: AdminGuild; settings: WelcomeSettings }>(
    "/api/welcome/settings?" + new URLSearchParams({ guildId }),
  );
}

export function saveWelcomeSettings(guildId: string, settings: WelcomeSettings) {
  return apiRequest<{ ok: boolean }>("/api/welcome/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guildId, ...settings }),
  });
}
