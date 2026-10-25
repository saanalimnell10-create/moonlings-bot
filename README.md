# moonlings-bot
A custom Python Discord bot for Moonlings automation and moderation.⁠

## Welcome & Goodbye control API

The website can manage welcome settings through the authenticated Flask API in `keep_alive.py`. Set a strong `BOT_CONTROL_API_TOKEN` secret on the bot host and configure the exact same token as `NITRO_BOT_CONTROL_API_TOKEN` on the website, with `NITRO_BOT_CONTROL_API_URL` set to this service's HTTPS base URL. Keep the bot's existing `DISCORD_TOKEN` server-side; it is used to fetch text channels. Never expose these values to the browser or commit them.

The API stores settings in `welcome_settings.json`. Configure persistent storage for that file on the bot host so settings survive restarts. Enable Server Members Intent in Discord Developer Portal for join and leave events.
