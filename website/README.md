# Moonlings website

## Discord sign-in and live Threat Center

The Discord OAuth client secret, encrypted-session key, and bot API token are server-only Nitro runtime variables. Set them in the deployment environment; do not place real values in client code or commit them. The Discord application's OAuth2 redirect URI must exactly match `NITRO_DISCORD_REDIRECT_URI`.

Required OAuth and live-status variables are listed in `.env.example`. Generate a unique, high-entropy `NITRO_AUTH_SESSION_SECRET` (at least 32 characters). The Discord client ID is prefilled from Moonlings' bot invite, but can be overridden.

The live-status proxy requires a trusted HTTPS bot API and bearer token. `NITRO_BOT_STATUS_API_URL` is its base URL. The proxy calls `GET {NITRO_BOT_STATUS_API_URL}/guilds/{guildId}/threat-status` with `NITRO_BOT_STATUS_API_TOKEN`. The status endpoint returns `level`, optional `mode`, `protections`, `updatedAt`, and `recentEvents` as JSON.

Only signed-in Discord users with Administrator or Manage Server permission for the requested guild can reach the status proxy. The browser receives no OAuth token or bot API credential. Live data is never cached, and the separate interactive demo is labeled as sample-only.

## Welcome & Goodbye settings page

The `/welcome` page lets Discord server administrators choose text channels and edit the messages Moonlings sends when members join or leave. It writes to the same per-server settings used by `cogs/welcome.py`.

For the page to connect to the bot, configure these server-side values:

- Website: `NITRO_BOT_CONTROL_API_URL` — the HTTPS base URL of the bot service running `keep_alive.py` (for example `https://moonlings.example.com`).
- Website: `NITRO_BOT_CONTROL_API_TOKEN` — a strong random secret.
- Bot service: `BOT_CONTROL_API_TOKEN` — the exact same secret as the website value.
- The bot service must also have its existing `DISCORD_TOKEN` configured.

The website proxy calls `/api/admin/guilds/{guildId}/channels` and `/api/admin/guilds/{guildId}/welcome` on the bot service. Requests from the browser are authenticated with the Discord session and rechecked for Administrator or Manage Server permission before being proxied. The bot service additionally requires the shared bearer token.

The bot writes settings to `welcome_settings.json`. Use persistent storage for that file on the bot host so settings survive restarts or redeploys. Enable the Discord Server Members intent in the Developer Portal; the bot code also enables `intents.members` for join/leave events.

Welcome and goodbye messages support `{user}` and `{server}`. The editor limits message text to 1,800 characters. Saving settings applies them to future member join/leave events without restarting the bot.
