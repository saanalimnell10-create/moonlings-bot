import { useState } from "react";
import { Activity, Check, Clipboard, LockKeyhole, Shield, Waves, Zap } from "lucide-react";
import "./safety-quick-actions.css";

const safetyActions = [
  { name: "Check threat level", command: "??threatlevel", note: "See the current mode and threat score.", icon: Activity, admin: false },
  { name: "Turn on Anti-Raid", command: "??antiraid on", note: "Enable join-raid protection.", icon: Waves, admin: true },
  { name: "Turn on Anti-Nuke", command: "??antinuke on", note: "Enable protection against destructive actions.", icon: Shield, admin: true },
  { name: "Enable threat monitoring", command: "??togglethreat on", note: "Start dynamic threat tracking.", icon: Zap, admin: true },
];

export default function SafetyQuickActions() {
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

  return <>
    <div className="bot-prefix-control"><label htmlFor="bot-prefix">YOUR SERVER PREFIX</label><input id="bot-prefix" value={prefix} maxLength={5} onChange={(event) => setPrefix(event.target.value.replace(/\s/g, ""))} aria-describedby="bot-prefix-help"/><span id="bot-prefix-help">Not sure? Run <code>??prefix</code> in your server first.</span></div>
    <div className="safety-action-grid">{safetyActions.map((action) => { const Icon = action.icon; const command = action.command.replace(/^\?\?/, prefix || "??"); return <article className="safety-action-card" key={action.name}><div className="safety-action-icon"><Icon size={18}/></div><div className="safety-action-heading"><h3>{action.name}</h3><span className={action.admin ? "admin-action-tag" : "read-action-tag"}>{action.admin ? "ADMIN ONLY" : "CHECK"}</span></div><p>{action.note}</p><code className="safety-action-command">{command}</code><button className="safety-copy-button" onClick={() => void copyCommand(action.command)}>{copiedCommand === command && !copyFailed ? <><Check size={14}/> Copied</> : <><Clipboard size={14}/> Copy for Discord</>}</button></article>; })}</div>
    <div className={`bot-copy-feedback ${copyFailed ? "copy-error" : ""}`} aria-live="polite">{copiedCommand ? copyFailed ? <>Couldn’t copy automatically. Select and copy <code>{copiedCommand}</code>.</> : <>Copied <code>{copiedCommand}</code>. Paste it into the right server channel to run it.</> : <><LockKeyhole size={14}/> Copying never runs a command. Moonlings checks administrator permissions in Discord.</>}</div>
  </>;
}
