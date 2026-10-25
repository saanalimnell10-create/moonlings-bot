import { useEffect, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertCircle, CheckCircle2, Clock3, LockKeyhole, LogOut, RefreshCw, Shield } from "lucide-react";
import { getAdminGuilds, getDiscordSession, getThreatStatus, logoutDiscord } from "@/lib/threat-center-api";
import ThreatMoon from "@/components/threat-center/ThreatMoon";
import "./live-status.css";

function formatUpdatedAt(value: string | null) {
  if (!value || Number.isNaN(Date.parse(value))) return "Timestamp not supplied by bot";
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function threatMoonLevel(status: string): number | null {
  const normalized = status.toLowerCase();
  if (/lockdown|critical|emergency|protective/.test(normalized)) return 3;
  if (/elevated|heightened|high/.test(normalized)) return 2;
  if (/watchful|moderate/.test(normalized)) return 1;
  if (/normal|quiet|low|safe/.test(normalized)) return 0;
  return null;
}

export default function LiveStatusPanel() {
  const queryClient = useQueryClient();
  const [guildId, setGuildId] = useState("");
  const session = useQuery({ queryKey: ["discord-session"], queryFn: getDiscordSession, retry: false });
  const guilds = useQuery({
    queryKey: ["admin-guilds"],
    queryFn: getAdminGuilds,
    enabled: session.data?.authenticated === true,
    retry: false,
  });
  const threatStatus = useQuery({
    queryKey: ["threat-status", guildId],
    queryFn: () => getThreatStatus(guildId),
    enabled: Boolean(guildId) && session.data?.authenticated === true,
    refetchInterval: 20_000,
    retry: false,
  });
  const liveMoonLevel = threatStatus.data ? threatMoonLevel(threatStatus.data.level) : null;

  useEffect(() => {
    if (!guildId && guilds.data?.length) setGuildId(guilds.data[0].id);
    if (guildId && guilds.data && !guilds.data.some((guild) => guild.id === guildId)) setGuildId(guilds.data[0]?.id || "");
  }, [guildId, guilds.data]);

  const handleLogout = async () => {
    await logoutDiscord();
    setGuildId("");
    await queryClient.invalidateQueries({ queryKey: ["discord-session"] });
    await queryClient.removeQueries({ queryKey: ["admin-guilds"] });
    await queryClient.removeQueries({ queryKey: ["threat-status"] });
  };

  if (session.isPending) {
    return <div className="live-unavailable"><div className="live-lock-icon"><RefreshCw size={21}/></div><div className="live-copy"><h3>Checking your secure connection</h3><p>Looking for an active Discord sign-in.</p></div></div>;
  }

  if (!session.data?.authenticated) {
    return <div className="live-unavailable"><div className="live-lock-icon"><LockKeyhole size={22}/></div><div className="live-copy"><h3>Sign in to see your server’s status</h3><p>Discord sign-in is required. The server checks use your Discord permissions, and only administrators or members with Manage Server access can view status.</p><div className="live-next-steps"><span><CheckCircle2 size={15}/> Your Discord token stays encrypted in an HTTP-only server cookie</span><span><Shield size={15}/> The server verifies permissions on every status request</span></div><a className="live-action-button" href="/api/auth/discord/login">Continue with Discord <LockKeyhole size={15}/></a></div></div>;
  }

  if (guilds.isPending) {
    return <div className="live-unavailable"><div className="live-lock-icon"><RefreshCw size={21}/></div><div className="live-copy"><h3>Finding your servers</h3><p>Checking which servers you can administer.</p></div></div>;
  }

  if (guilds.isError) {
    return <div className="live-unavailable"><div className="live-lock-icon"><AlertCircle size={21}/></div><div className="live-copy"><h3>Couldn’t verify your Discord servers</h3><p>{guilds.error.message} Sign out and reconnect to try again.</p><button className="live-action-button secondary" onClick={() => void handleLogout()}>Sign out <LogOut size={15}/></button></div></div>;
  }

  if (!guilds.data?.length) {
    return <div className="live-unavailable"><div className="live-lock-icon"><Shield size={21}/></div><div className="live-copy"><h3>No administrator-access servers found</h3><p>Sign in with a Discord account that has Administrator or Manage Server permission in a server where Moonlings is installed.</p><button className="live-action-button secondary" onClick={() => void handleLogout()}>Use another Discord account <LogOut size={15}/></button></div></div>;
  }

  return <>
    <div className="live-toolbar"><label htmlFor="threat-server-select">SERVER</label><select id="threat-server-select" value={guildId} onChange={(event) => setGuildId(event.target.value)}>{guilds.data.map((guild) => <option key={guild.id} value={guild.id}>{guild.name}</option>)}</select><button className="live-refresh-button" onClick={() => void threatStatus.refetch()} disabled={threatStatus.isFetching}><RefreshCw size={14} className={threatStatus.isFetching ? "refresh-spinning" : ""}/> Refresh</button><button className="live-signout-button" onClick={() => void handleLogout()}><LogOut size={14}/> Sign out</button></div>
    {threatStatus.isPending && <div className="live-unavailable"><div className="live-lock-icon"><RefreshCw size={21}/></div><div className="live-copy"><h3>Connecting to Moonlings</h3><p>Fetching this server’s real threat status over the protected bot connection.</p></div></div>}
    {threatStatus.isError && <div className="live-unavailable"><div className="live-lock-icon"><AlertCircle size={21}/></div><div className="live-copy"><h3>Live status is unavailable</h3><p>{threatStatus.error.message} Demo values are not shown in this live panel.</p><button className="live-action-button secondary" onClick={() => void threatStatus.refetch()}>Try again <RefreshCw size={14}/></button></div></div>}
    {threatStatus.data && !threatStatus.isError && <article className="real-status-card"><div className="real-status-top"><div><span className="real-status-kicker"><span className="connection-dot"/> SECURE BOT CONNECTION</span><h3>{threatStatus.data.guild.name}</h3></div><span className="live-chip connected-chip"><i/> LIVE · REFRESHES EVERY 20 SEC</span></div><div className="real-threat-level">{liveMoonLevel !== null ? <ThreatMoon level={liveMoonLevel} label={threatStatus.data.level} /> : <div className="real-level-icon"><Shield size={25}/></div>}<div><span className="status-caption">CURRENT THREAT LEVEL</span><strong>{threatStatus.data.level}</strong></div></div><div className="real-status-grid"><div><span>Threat mode</span><strong>{threatStatus.data.mode || "Not reported"}</strong></div>{Object.entries(threatStatus.data.protections).map(([name, enabled]) => <div key={name}><span>{name}</span><strong className={enabled ? "protection-enabled" : "protection-disabled"}>{enabled ? "Enabled" : "Disabled"}</strong></div>)}</div><div className="real-status-updated"><Clock3 size={14}/> Last updated: {formatUpdatedAt(threatStatus.data.updatedAt)}</div>{threatStatus.data.recentEvents.length > 0 && <div className="real-events"><h4>Recent signals</h4>{threatStatus.data.recentEvents.map((event, index) => <div className="real-event" key={event.id || `${event.message}-${index}`}><span className="event-bullet"/><span>{event.message}</span><time>{event.at ? formatUpdatedAt(event.at) : ""}</time></div>)}</div>}</article>}
  </>;
}
