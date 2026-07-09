import { useEffect, useRef, useState } from "react";
import { animate } from "framer-motion";

const R = 78;
const CIRC = 2 * Math.PI * R;

const GLITCH_GLYPHS = "0123456789ABCDEF#%&$@!?";

function lerpRGB(a: number[], b: number[], t: number): number[] {
  return a.map((v, i) => Math.round(v + (b[i] - v) * t));
}

function mixColor(score: number): string {
  // titanium #8b9099 -> copper #e8823f -> ember #ff6a2b
  const t = Math.min(Math.max(score / 100, 0), 1);
  const titanium = [0x8b, 0x90, 0x99];
  const copper = [0xe8, 0x82, 0x3f];
  const ember = [0xff, 0x6a, 0x2b];
  const c =
    t < 0.5 ? lerpRGB(titanium, copper, t * 2) : lerpRGB(copper, ember, (t - 0.5) * 2);
  return `#${c.map((v) => v.toString(16).padStart(2, "0")).join("")}`;
}

/**
 * Futuristic 270-degree dial. The arc sweeps up with a spring, the needle
 * chases it, and the readout ticks with glitch glyphs until it locks in.
 */
export default function RiskGauge({ score }: { score: number }) {
  const [display, setDisplay] = useState("00");
  const [locked, setLocked] = useState(false);
  const [progress, setProgress] = useState(0);
  const glitchTimer = useRef(0);

  useEffect(() => {
    setLocked(false);
    const controls = animate(0, score, {
      duration: 1.6,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => {
        setProgress(v / 100);
        glitchTimer.current++;
        // every few frames, corrupt a digit while ticking
        if (glitchTimer.current % 4 === 0 && v < score - 2) {
          const glyph = GLITCH_GLYPHS[Math.floor(Math.random() * GLITCH_GLYPHS.length)];
          setDisplay(String(Math.round(v)).padStart(2, "0").slice(0, -1) + glyph);
        } else {
          setDisplay(String(Math.round(v)).padStart(2, "0"));
        }
      },
      onComplete: () => {
        setDisplay(String(score).padStart(2, "0"));
        setLocked(true);
      },
    });
    return () => controls.stop();
  }, [score]);

  const color = mixColor(score);
  const needleAngle = -135 + progress * 270;

  return (
    <div className="risk-gauge">
      <svg viewBox="0 0 200 200" className="gauge-svg">
        {/* track */}
        <circle
          cx="100"
          cy="100"
          r="78"
          fill="none"
          stroke="rgba(232,130,63,0.14)"
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray="367.5 490"
          transform="rotate(135 100 100)"
        />
        {/* tick marks */}
        {Array.from({ length: 28 }).map((_, i) => {
          const angle = ((-135 + (i / 27) * 270) * Math.PI) / 180;
          const inner = 88;
          const outer = i % 9 === 0 ? 96 : 92;
          return (
            <line
              key={i}
              x1={100 + inner * Math.sin(angle)}
              y1={100 - inner * Math.cos(angle)}
              x2={100 + outer * Math.sin(angle)}
              y2={100 - outer * Math.cos(angle)}
              stroke={i / 27 <= progress ? color : "rgba(139,144,153,0.28)"}
              strokeWidth={i % 9 === 0 ? 2.5 : 1.2}
            />
          );
        })}
        {/* value arc */}
        <circle
          cx="100"
          cy="100"
          r={R}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          transform="rotate(135 100 100)"
          strokeDasharray={`${progress * 0.75 * CIRC} ${CIRC}`}
          style={{ filter: `drop-shadow(0 0 8px ${color})` }}
        />
        {/* needle */}
        <g transform={`rotate(${needleAngle} 100 100)`}>
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="34"
            stroke={color}
            strokeWidth="2.5"
            style={{ filter: `drop-shadow(0 0 6px ${color})` }}
          />
          <circle cx="100" cy="100" r="5" fill={color} />
        </g>
      </svg>
      <div
        className={`gauge-readout ${locked ? "gauge-locked" : "gauge-ticking"}`}
        style={{ color, textShadow: `0 0 18px ${color}` }}
      >
        {display}
      </div>
      <div className="gauge-caption">RISK INDEX</div>
    </div>
  );
}
