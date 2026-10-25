import { defineConfig } from "nitro";

export default defineConfig({
  serverDir: "./server",
  runtimeConfig: {
    discordClientId: "1562025850755616870",
    discordClientSecret: "",
    discordRedirectUri: "",
    authSessionSecret: "",
    botStatusApiUrl: "",
    botStatusApiToken: "",
  },
});
