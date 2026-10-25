import { useState } from "react";
import { Link } from "react-router-dom";
import { Activity, ArrowLeft, ArrowRight, Check, Clipboard, LockKeyhole, Shield, Sparkles, Waves, Zap } from "lucide-react";
import LiveStatusPanel from "@/components/threat-center/LiveStatusPanel";
import "../threat-center.css";
import "../bot-dashboard.css";

const safetyActions = [
  { name: "Check threat level", command: "??threatlevel", note: "See the current mode and threat score.", icon: Activity, admin: false },
  { name: "Turn on Anti-Raid", command: "??antiraid on", note: "Enable join-raid protection.", icon: Waves, admin: true },
  { name: "Turn on Anti-Nuke", command: "??antinuke on", note: "Enable protection against destructive actions.", icon: Shield, admin: true },
  { name: "Enable threat monitoring", command: "??togglethreat on", note: "Start dynamic threat tracking.", icon: Zap, admin: true },
];

const inviteUrl = "https://discord.com/oauth2/authorize?client_id=1562025850755616870&permissions=8&integration_type=0&scope=bot";

export default function BotDashboard() {
  const [prefix, setPrefix] = useState("??");
  const [copiedCommand, setCopiedCommand] = useState("");
  const [copyFailed, setCopyFailed] = useState(false);

  const copyCommand = async (command: string) => {
    const actualCommand = command.replace(/^\?\?/, prefix || "??");
    try {
      await navigator.clipboard.writeText(actualCommand);
      setCopiedCommand(actualCommand);
      setCopyFailed(false);
    } catch {
      setCopiedCommand(actualCommand);
      setCopyFailed(true);
    }
  };

  return <main className="threat-page bot-dashboard-page">
    <header className="site-header threat-header">
      <Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i /></span><span>moonlings</span></Link>
      <nav className="nav-links threat-nav"><Link to="/">Why Moonlings</Link><Link to="/#commands">Commands</Link><Link to="/threat-center">Threat Center</Link><Link className="threat-nav-active" to="/bot">Bot dashboard</Link></nav>
      <Link className="header-invite" to="/">Back to home <ArrowLeft size={15}/></Link>
    </header>

    <section className="bot-hero">
      <div className="bot-hero-copy"><span className="eyebrow"><Sparkles size={14}/> YOUR LITTLE COMMAND CENTER</span><h1>Moonlings, <em>at the ready.</em></h1><p>Check your server’s protected status and grab the right safety commands without leaving the dashboard.</p><a className="bot-hero-button" href="#bot-status">Check bot status <ArrowRight size={15}/></a></div>
      <div className="bot-hero-art" aria-hidden="true"><div className="bot-planet-orbit orbit-a"><i>✦</i></div><div className="bot-planet-orbit orbit-b"><i>✧</i></div><div className="bot-planet">☾</div><span className="bot-art-spark spark-a">✦</span><span className="bot-art-spark spark-b">✧</span><span className="bot-art-bubble">🪼</span></div>
    </section>

    <section className="bot-dashboard-section" id="bot-status">
      <div className="threat-section-heading"><div><span className="eyebrow"><LockKeyhole size={13}/> PRIVATE SERVER CHECK</span><h2>Bot &amp; server status</h2><p>Sign in with Discord to check the live status for a server you manage.</p></div><span className="bot-refresh-note"><Activity size={14}/> Refreshes every 20 seconds</span></div>
      <LiveStatusPanel />
    </section>

    <section className="bot-dashboard-section bot-actions-section" id="safety-actions">
      <div className="threat-section-heading"><div><span className="eyebrow"><Shield size={14}/> SMALL STEPS, STRONGER SHIELDS</span><h2>Quick safety toolkit</h2><p>Prepare trusted Moonlings commands for Discord. Nothing runs from this page.</p></div></div>
      <div className="bot-prefix-control"><label htmlFor="bot-prefix">YOUR SERVER PREFIX</label><input id="bot-prefix" value={prefix} maxLength={5} onChange={(event) => setPrefix(event.target.value.replace(/\s/g, ""))} aria-describedby="bot-prefix-help"/><span id="bot-prefix-help">Not sure? Run <code>??prefix</code> in your server first.</span></div>
      <div className="safety-action-grid">{safetyActions.map((action) => { const Icon = action.icon; const command = action.command.replace(/^\?\?/, prefix || "??"); return <article className="safety-action-card" key={action.name}><div className="safety-action-icon"><Icon size={18}/></div><div className="safety-action-heading"><h3>{action.name}</h3><span className={action.admin ? "admin-action-tag" : "read-action-tag"}>{action.admin ? "ADMIN ONLY" : "CHECK"}</span></div><p>{action.note}</p><code className="safety-action-command">{command}</code><button className="safety-copy-button" onClick={() => void copyCommand(action.command)}>{copiedCommand === command && !copyFailed ? <><Check size={14}/> Copied</> : <><Clipboard size={14}/> Copy for Discord</>}</button></article>; })}</div>
      <div className={`bot-copy-feedback ${copyFailed ? "copy-error" : ""}`} aria-live="polite">{copiedCommand ? copyFailed ? <>Couldn’t copy automatically. Select and copy <code>{copiedCommand}</code>.</> : <>Copied <code>{copiedCommand}</code>. Paste it into the right server channel to run it.</> : <><LockKeyhole size={14}/> Copying never runs a command. Moonlings checks administrator permissions in Discord.</>}</div>
    </section>

    <section className="bot-setup-note"><div className="bot-setup-icon"><Sparkles size={19}/></div><div><h3>Keep your bot ready</h3><p>Make sure Moonlings is in your server and has only the permissions your setup needs. For full live threat status, the secure bot status connection must be configured.</p></div><a href={inviteUrl} target="_blank" rel="noreferrer">Invite Moonlings <ArrowRight size={14}/></a></section>

    <footer className="threat-footer"><Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i/></span><span>moonlings</span></Link><span>A cozy command center for safer communities.</span><Link to="/threat-center">Threat Center <ArrowRight size={14}/></Link></footer>
  </main>;
}
