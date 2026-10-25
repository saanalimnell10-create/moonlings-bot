import "./threat-moon.css";

type ThreatMoonProps = {
  level: number;
  label: string;
};

export default function ThreatMoon({ level, label }: ThreatMoonProps) {
  const safeLevel = Math.max(0, Math.min(3, level));

  return (
    <div className="threat-moon-display">
      <div
        className={`threat-moon-scene moon-threat-${safeLevel}`}
        role="img"
        aria-label={`Threat Moon at ${label} level`}
      >
        <span className="threat-moon-orbit moon-orbit-outer"><i>✦</i></span>
        <span className="threat-moon-orbit moon-orbit-inner"><i>✧</i></span>
        <span className="threat-moon-body">
          <i className="threat-moon-shadow" />
          <i className="threat-moon-crater crater-one" />
          <i className="threat-moon-crater crater-two" />
          <i className="threat-moon-crater crater-three" />
        </span>
        <span className="threat-moon-glow" />
      </div>
      <span className="threat-moon-caption">THREAT MOON</span>
    </div>
  );
}
