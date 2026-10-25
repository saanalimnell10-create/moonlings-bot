import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, ArrowRight, LockKeyhole, RefreshCw, Shield, Sparkles, Waves } from "lucide-react";
import LiveStatusPanel from "@/components/threat-center/LiveStatusPanel";
import ThreatMoon from "@/components/threat-center/ThreatMoon";
import "../threat-center.css";

const inviteUrl = "https://discord.com/oauth2/authorize?client_id=1562025850755616870&permissions=8&integration_type=0&scope=bot";
const sampleLevels = ["Quiet waters", "Watchful", "Heightened", "Protective"];

export default function ThreatCenter() {
  const [sampleLevel, setSampleLevel] = useState(1);
  const [sampleEnabled, setSampleEnabled] = useState(true);

  return <main className="threat-page">
    <header className="site-header threat-header">
      <Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i /></span><span>moonlings</span></Link>
      <nav className="nav-links threat-nav"><Link to="/">Why Moonlings</Link><Link to="/#commands">Commands</Link><Link to="/bot">Bot Dashboard</Link><Link className="threat-nav-active" to="/threat-center">Threat Center</Link></nav>
      <Link className="header-invite" to="/">Back to home <ArrowLeft size={15}/></Link>
    </header>

    <section className="threat-hero">
      <div className="threat-hero-content"><span className="eyebrow"><Sparkles size={14}/> A CALMER KIND OF SECURITY</span><h1>Know your waters.<br/><em>Keep your community safe.</em></h1><p>A gentle overview of Moonlings threat tools, a safe sample to explore, and a private live dashboard for server administrators.</p><div className="threat-hero-actions"><a href="#live-status" className="threat-button">Live server status <ArrowRight size={16}/></a><a href="#demo" className="threat-text-link">Explore the demo <Waves size={15}/></a></div></div>
      <div className="threat-orbit-art" aria-hidden="true"><span className="threat-orbit-ring"/><span className="threat-moon">☾</span><span className="threat-art-star star-a">✦</span><span className="threat-art-star star-b">✧</span><span className="threat-art-bubble">🪼</span></div>
    </section>

    <section className="threat-content" id="live-status">
      <div className="threat-section-heading"><div><span className="eyebrow"><LockKeyhole size={13}/> PRIVATE TO YOUR SERVER</span><h2>Live server status</h2><p>Real data, scoped to a server you administer. This dashboard is read-only.</p></div></div>
      <LiveStatusPanel />
      <div className="live-help-row"><span><Shield size={16}/> Need Moonlings in your server?</span><a href={inviteUrl} target="_blank" rel="noreferrer">Invite Moonlings <ArrowRight size={14}/></a><span className="live-help-note">Only servers where you have administrator or Manage Server permissions are available.</span></div>
    </section>

    <section className="threat-content guide-section" id="guide">
      <div className="threat-section-heading"><div><span className="eyebrow"><Waves size={14}/> UNDERSTAND THE SIGNALS</span><h2>Threat tools, explained</h2><p>Use the bot’s commands for full details and configuration.</p></div></div>
      <div className="guide-grid"><article className="guide-card"><span className="guide-number">01</span><div className="guide-icon guide-icon-pink"><Shield size={19}/></div><h3>Threat level</h3><p>Use <code>??threatlevel</code> in your server to check its current threat level. The live dashboard shows the bot’s reported value without inventing severity thresholds.</p><span className="guide-foot">The bot’s response is authoritative</span></article><article className="guide-card"><span className="guide-number">02</span><div className="guide-icon guide-icon-blue"><Waves size={19}/></div><h3>Threat system</h3><p><code>??togglethreat [on/off]</code> controls the threat security system. Review changes with trusted administrators.</p><span className="guide-foot">Manage this setting in Discord</span></article><article className="guide-card"><span className="guide-number">03</span><div className="guide-icon guide-icon-lilac"><RefreshCw size={19}/></div><h3>Response mode</h3><p><code>??setthreatmode [mode]</code> sets the server’s threat response mode. Ask the bot for supported modes before choosing one.</p><span className="guide-foot">No severity thresholds are assumed</span></article></div>
      <div className="guide-note"><Sparkles size={16}/><p><strong>Useful related protections:</strong> Moonlings also lists <code>??antinuke [on/off]</code> and <code>??antiraid [on/off]</code>. Their exact behavior and configuration are managed through Discord.</p></div>
    </section>

    <section className="demo-section" id="demo"><div className="demo-inner"><div className="threat-section-heading"><div><span className="eyebrow"><Sparkles size={14}/> A SAFE LITTLE SANDBOX</span><h2>Explore the demo</h2><p>Sample values only. Nothing here connects to Discord or changes a real server.</p></div><span className="sample-chip">✦ SAMPLE DATA · NOT LIVE</span></div>
      <div className="demo-layout"><article className="demo-status-card"><div className="demo-card-top"><span><Waves size={15}/> TIDAL STAR GUILD</span><span className="sample-mini">SAMPLE</span></div><div className="demo-level-row"><div><span className="status-caption">SAMPLE THREAT LEVEL</span><h3>{sampleLevels[sampleLevel]}</h3></div><ThreatMoon level={sampleLevel} label={sampleLevels[sampleLevel]} /></div><div className="demo-meter" aria-label={`Demo sample level ${sampleLevel + 1} of 4`}>{sampleLevels.map((level, i) => <i key={level} className={i <= sampleLevel ? `filled fill-${i}` : ""}/>)}</div><div className="demo-protections"><div><span className="protection-dot protection-on"/><span>Threat protection</span><b>{sampleEnabled ? "On" : "Off"}</b></div><div><span className="protection-dot protection-on"/><span>Anti-raid</span><b>On</b></div><div><span className="protection-dot protection-off"/><span>Anti-nuke</span><b>Off</b></div></div><div className="demo-mode"><span>RESPONSE MODE</span><strong>Sample · observe</strong></div><small className="demo-updated">Illustrative snapshot · not a real guild</small></article>
      <div className="demo-controls"><h3>Try a level change</h3><p>Use the controls to see how a dashboard might respond. All values stay in this page.</p><div className="demo-select-row"><label htmlFor="sample-level">Sample level</label><select id="sample-level" value={sampleLevel} onChange={(event) => setSampleLevel(Number(event.target.value))}>{sampleLevels.map((level, index) => <option key={level} value={index}>{level}</option>)}</select></div><button className={`demo-toggle ${sampleEnabled ? "enabled" : ""}`} onClick={() => setSampleEnabled(!sampleEnabled)}><span className="toggle-track"><i/></span> Threat protection: {sampleEnabled ? "On" : "Off"}</button><div className="demo-privacy"><LockKeyhole size={15}/><span>Demo controls never call the bot, API, or Discord.</span></div></div></div>
    </div></section>
    <footer className="threat-footer"><Link className="brand" to="/"><span className="brand-mark"><span>☾</span><i/></span><span>moonlings</span></Link><span>Thoughtful tools for calmer communities.</span><Link to="/">Back to Moonlings <ArrowRight size={14}/></Link></footer>
  </main>;
}
