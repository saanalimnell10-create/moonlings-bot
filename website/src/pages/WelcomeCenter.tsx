import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { ArrowLeft, ArrowRight, Check, Heart, LockKeyhole, MessageCircleHeart, Sparkles, Users, Waves } from "lucide-react";
import { getAdminGuilds, getDiscordSession, getWelcomeChannels, getWelcomeSettings, saveWelcomeSettings, type WelcomeSettings } from "@/lib/threat-center-api";
import "../threat-center.css";
import "../welcome-center.css";

const initialSettings: WelcomeSettings = {
  welcomeChannelId: null,
  welcomeText: "Welcome to {server}, {user}! We’re so glad you’re here. ✨",
  goodbyeChannelId: null,
  goodbyeText: "Goodbye, {user}. We’ll miss you around {server}! 👋",
};

function messagePreview(text: string, user: string) {
  return text.split("{user}").join(user).split("{server}").join("Your server");
}

export default function WelcomeCenter() {
  const queryClient = useQueryClient();
  const [guildId, setGuildId] = useState("");
  const [settings, setSettings] = useState<WelcomeSettings>(initialSettings);
  const session = useQuery({ queryKey: ["discord-session"], queryFn: getDiscordSession, retry: false });
  const guilds = useQuery({
    queryKey: ["admin-guilds"],
    queryFn: getAdminGuilds,
    enabled: session.data?.authenticated === true,
    retry: false,
  });
  const channels = useQuery({
    queryKey: ["welcome-channels", guildId],
    queryFn: () => getWelcomeChannels(guildId),
    enabled: Boolean(guildId) && session.data?.authenticated === true,
    retry: false,
  });
  const savedSettings = useQuery({
    queryKey: ["welcome-settings", guildId],
    queryFn: () => getWelcomeSettings(guildId),
    enabled: Boolean(guildId) && session.data?.authenticated === true,
    retry: false,
  });
  const saveSettings = useMutation({
    mutationFn: () => saveWelcomeSettings(guildId, settings),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["welcome-settings", guildId] });
    },
  });

  useEffect(() => {
    if (!guildId && guilds.data?.length) setGuildId(guilds.data[0].id);
    if (guildId && guilds.data && !guilds.data.some((guild) => guild.id === guildId)) setGuildId(guilds.data[0]?.id || "");
  }, [guildId, guilds.data]);

  useEffect(() => {
    if (savedSettings.data?.guild.id === guildId) setSettings(savedSettings.data.settings);
  }, [guildId, savedSettings.data]);

  const updateSetting = <K extends keyof WelcomeSettings>(key: K, value: WelcomeSettings[K]) => {
    setSettings((current) => ({ ...current, [key]: value }));
    saveSettings.reset();
  };

  return <main className="threat-page welcome-page">
    <header className="site-header threat-header">
      <Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i /></span><span>moonlings</span></Link>
      <nav className="nav-links threat-nav"><Link to="/">Why Moonlings</Link><Link to="/#commands">Commands</Link><Link to="/threat-center">Threat Center</Link><Link className="threat-nav-active" to="/welcome">Welcome &amp; Goodbye</Link></nav>
      <Link className="header-invite" to="/">Back to home <ArrowLeft size={15}/></Link>
    </header>

    <section className="welcome-hero">
      <div className="welcome-hero-copy"><span className="eyebrow"><Sparkles size={14}/> A SOFTER HELLO, A LOVELY GOODBYE</span><h1>Make every arrival<br/><em>feel like home.</em></h1><p>Write both messages once, choose their channels, and Moonlings will post automatically when a member joins or leaves.</p><a href="#welcome-settings" className="welcome-hero-button">Set up messages <ArrowRight size={15}/></a></div>
      <div className="welcome-hero-art" aria-hidden="true"><div className="welcome-art-orbit"><i>✦</i></div><div className="welcome-art-moon">☾</div><span className="welcome-art-heart">♡</span><span className="welcome-art-star">✧</span><span className="welcome-art-wave">〰</span></div>
    </section>

    <section className="welcome-content" id="welcome-settings">
      <div className="threat-section-heading"><div><span className="eyebrow"><LockKeyhole size={13}/> ADMIN-ONLY SETTINGS</span><h2>Your welcome &amp; goodbye messages</h2><p>Changes save directly to Moonlings and apply to the next member event.</p></div><span className="welcome-live-tag"><span/> AUTOMATIC ON JOIN &amp; LEAVE</span></div>

      {session.isPending && <div className="welcome-notice"><Heart size={19}/> Checking your secure Discord sign-in…</div>}
      {!session.isPending && !session.data?.authenticated && <div className="welcome-notice"><LockKeyhole size={19}/><div><strong>Sign in with Discord to get started</strong><p>Only server administrators or members with Manage Server permission can edit these messages.</p><a href="/api/auth/discord/login" className="welcome-login-button">Continue with Discord <ArrowRight size={14}/></a></div></div>}
      {session.data?.authenticated && guilds.isPending && <div className="welcome-notice"><Users size={19}/> Finding servers you can manage…</div>}
      {session.data?.authenticated && guilds.isError && <div className="welcome-notice error-notice"><MessageCircleHeart size={19}/><div><strong>Couldn’t verify your Discord servers</strong><p>{guilds.error.message}</p></div></div>}
      {session.data?.authenticated && !guilds.isPending && !guilds.isError && !guilds.data?.length && <div className="welcome-notice"><Users size={19}/><div><strong>No administrator-access servers found</strong><p>Use a Discord account with Administrator or Manage Server permission in a server where Moonlings is installed.</p></div></div>}

      {session.data?.authenticated && Boolean(guilds.data?.length) && <>
        <div className="welcome-server-select"><label htmlFor="welcome-server">SERVER</label><select id="welcome-server" value={guildId} onChange={(event) => { setGuildId(event.target.value); setSettings(initialSettings); saveSettings.reset(); }}>{guilds.data?.map((guild) => <option key={guild.id} value={guild.id}>{guild.name}</option>)}</select><span>Settings are saved separately for each server.</span></div>
        {channels.isError && <div className="welcome-notice error-notice"><MessageCircleHeart size={19}/><div><strong>Couldn’t load server channels</strong><p>{channels.error.message}</p></div></div>}
        {savedSettings.isError && <div className="welcome-notice error-notice"><MessageCircleHeart size={19}/><div><strong>Welcome settings aren’t connected yet</strong><p>{savedSettings.error.message}</p></div></div>}
        {!channels.isError && !savedSettings.isError && (channels.isPending || savedSettings.isPending) && <div className="welcome-notice"><Waves size={19}/> Connecting to Moonlings…</div>}
        {channels.data && savedSettings.data?.guild.id === guildId && <form className="welcome-settings-form" onSubmit={(event) => { event.preventDefault(); saveSettings.mutate(); }}>
          <div className="welcome-message-grid">
            <article className="welcome-message-card join-card">
              <div className="welcome-card-heading"><div className="welcome-card-icon"><Users size={18}/></div><div><span>WHEN SOMEONE JOINS</span><h3>Welcome message</h3></div></div>
              <label className="welcome-field-label" htmlFor="welcome-channel">POST IN</label>
              <select id="welcome-channel" value={settings.welcomeChannelId || ""} onChange={(event) => updateSetting("welcomeChannelId", event.target.value || null)} required><option value="" disabled>Choose a text channel</option>{channels.data.channels.map((channel) => <option value={channel.id} key={channel.id}>#{channel.name}</option>)}</select>
              <label className="welcome-field-label" htmlFor="welcome-text">YOUR MESSAGE</label>
              <textarea id="welcome-text" value={settings.welcomeText} maxLength={1800} onChange={(event) => updateSetting("welcomeText", event.target.value)} required placeholder="Welcome to {server}, {user}!" />
              <div className="welcome-hint-row"><span>Use <code>{"{user}"}</code> and <code>{"{server}"}</code></span><span>{settings.welcomeText.length}/1800</span></div>
              <div className="welcome-preview"><span>PREVIEW</span><p>{messagePreview(settings.welcomeText, "@New Moonling")}</p></div>
            </article>
            <article className="welcome-message-card goodbye-card">
              <div className="welcome-card-heading"><div className="welcome-card-icon"><Heart size={18}/></div><div><span>WHEN SOMEONE LEAVES</span><h3>Goodbye message</h3></div></div>
              <label className="welcome-field-label" htmlFor="goodbye-channel">POST IN</label>
              <select id="goodbye-channel" value={settings.goodbyeChannelId || ""} onChange={(event) => updateSetting("goodbyeChannelId", event.target.value || null)} required><option value="" disabled>Choose a text channel</option>{channels.data.channels.map((channel) => <option value={channel.id} key={channel.id}>#{channel.name}</option>)}</select>
              <label className="welcome-field-label" htmlFor="goodbye-text">YOUR MESSAGE</label>
              <textarea id="goodbye-text" value={settings.goodbyeText} maxLength={1800} onChange={(event) => updateSetting("goodbyeText", event.target.value)} required placeholder="Goodbye, {user}. We’ll miss you!" />
              <div className="welcome-hint-row"><span>Use <code>{"{user}"}</code> and <code>{"{server}"}</code></span><span>{settings.goodbyeText.length}/1800</span></div>
              <div className="welcome-preview goodbye-preview"><span>PREVIEW</span><p>{messagePreview(settings.goodbyeText, "Moonling friend")}</p></div>
            </article>
          </div>
          <div className="welcome-save-row"><span className="welcome-save-feedback" aria-live="polite">{saveSettings.isSuccess ? <><Check size={15}/> Saved! New joins and leaves will use these messages.</> : saveSettings.isError ? saveSettings.error.message : <><LockKeyhole size={14}/> Only admins can save settings. Messages post automatically after you save.</>}</span><button className="welcome-save-button" type="submit" disabled={saveSettings.isPending || channels.isPending || savedSettings.isPending}>{saveSettings.isPending ? "Saving…" : "Save both messages"} <ArrowRight size={15}/></button></div>
        </form>}
      </>}
    </section>

    <section className="welcome-tips"><div className="welcome-tip-icon"><Sparkles size={18}/></div><div><h3>A little placeholder magic</h3><p><code>{"{user}"}</code> becomes the member’s name in goodbye messages and a mention in welcome messages. <code>{"{server}"}</code> becomes your server’s name. The bot only sends after the settings are saved.</p></div></section>
    <footer className="threat-footer"><Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i/></span><span>moonlings</span></Link><span>Every little hello makes a community.</span><Link to="/threat-center">Threat Center <ArrowRight size={14}/></Link></footer>
  </main>;
}
