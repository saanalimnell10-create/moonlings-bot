# Moonlings website

## Secure Threat Center setup

The Discord OAuth client secret, encrypted-session key, and bot API token are server-only Nitro runtime variables. Set them in the deployment environment; do not place real values in client code or commit them. The Discord application's OAuth2 redirect URI must exactly match `NITRO_DISCORD_REDIRECT_URI`.

Required variables are listed in `.env.example`. Generate a unique, high-entropy `NITRO_AUTH_SESSION_SECRET` (at least 32 characters). The Discord client ID is prefilled from Moonlings' bot invite, but can be overridden.

The live-status proxy requires a trusted HTTPS bot API and bearer token. `NITRO_BOT_STATUS_API_URL` is its base URL (for example `https://bot-api.example/api`). The proxy calls:

```text
GET {NITRO_BOT_STATUS_API_URL}/guilds/{guildId}/threat-status
Authorization: Bearer {NITRO_BOT_STATUS_API_TOKEN}
```

The endpoint should return JSON in this shape:

```json
{
  "level": "Watchful",
  "mode": "observe",
  "protections": { "threat": true, "antiRaid": true, "antiNuke": false },
  "updatedAt": "2026-01-01T12:00:00.000Z",
  "recentEvents": [{ "id": "evt-1", "message": "Example event", "at": "2026-01-01T11:59:00.000Z" }]
}
```

Only signed-in Discord users with Administrator or Manage Server permission for the requested guild can reach the status proxy. The browser receives no OAuth token or bot API credential. Live data is never cached, and the separate interactive demo is labeled as sample-only.
