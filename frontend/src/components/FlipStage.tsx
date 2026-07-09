import { useEffect, useMemo, useState, type ReactNode } from "react";
import { motion, AnimatePresence, useMotionValue, animate } from "framer-motion";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import TiltPanel from "./TiltPanel";
import type { RefactorResult, ScoreResult } from "../api";

function PointsCounter({ to }: { to: number }) {
  const mv = useMotionValue(0);
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    const controls = animate(mv, to, {
      duration: 1.2,
      ease: "easeOut",
      onUpdate: (v) => setDisplay(Math.round(v)),
    });
    return () => controls.stop();
  }, [to]);
  return <>{display}</>;
}

/** Radial DOM particle explosion fired on every flip. */
function BurstParticles({ nonce }: { nonce: number }) {
  const particles = useMemo(
    () =>
      Array.from({ length: 26 }).map((_, i) => {
        const angle = (i / 26) * Math.PI * 2 + Math.random() * 0.4;
        const dist = 180 + Math.random() * 240;
        return {
          id: `${nonce}-${i}`,
          dx: Math.cos(angle) * dist,
          dy: Math.sin(angle) * dist * 0.7,
          size: 3 + Math.random() * 6,
          color: i % 3 === 0 ? "var(--ember)" : "var(--amber)",
          delay: Math.random() * 0.12,
        };
      }),
    [nonce]
  );

  if (nonce === 0) return null;

  return (
    <div className="burst-field" aria-hidden>
      {particles.map((p) => (
        <motion.span
          key={p.id}
          className="burst-particle"
          style={{ width: p.size, height: p.size, background: p.color, boxShadow: `0 0 10px ${p.color}` }}
          initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
          animate={{ x: p.dx, y: p.dy, opacity: 0, scale: 0.2 }}
          transition={{ duration: 1.1, delay: p.delay, ease: [0.16, 1, 0.3, 1] }}
        />
      ))}
    </div>
  );
}

interface FlipStageProps {
  /** front face content: the live editor */
  front: ReactNode;
  flipped: boolean;
  refactorResult: RefactorResult | null;
  initialScore: ScoreResult | null;
  flipNonce: number;
}

/**
 * The glass editor is a physical object: on refactor it rotates a full
 * 180° on the Y axis, exploding particles outward, revealing the cleaned
 * code engraved on its back face.
 */
export default function FlipStage({
  front,
  flipped,
  refactorResult,
  initialScore,
  flipNonce,
}: FlipStageProps) {
  const noValidCandidate = refactorResult?.final_score == null;
  const startScore = initialScore?.risk_score ?? 0;
  const pointsSaved =
    !refactorResult || noValidCandidate
      ? 0
      : Math.max(0, startScore - (refactorResult.final_score as number));

  return (
    <div className="flip-stage">
      <BurstParticles nonce={flipNonce} />
      <TiltPanel className="flip-tilt" maxTilt={6}>
        <motion.div
          className="flip-object"
          animate={{ rotateY: flipped ? 180 : 0 }}
          transition={{ duration: 1.1, ease: [0.68, -0.2, 0.27, 1.15] }}
        >
          <div className="flip-face flip-front glass-panel">{front}</div>

          <div className="flip-face flip-back glass-panel">
            <div className="editor-header">
              <span className="glow-text-amber editor-title aberrate">// CLEANED.py</span>
              <span className="editor-subtitle">
                {refactorResult
                  ? `${refactorResult.iterations_run} iteration(s) · RISK ${
                      noValidCandidate ? "N/A" : refactorResult.final_score
                    }`
                  : "awaiting refactor"}
              </span>
            </div>
            <div className="editor-body back-body">
              {refactorResult && (
                <pre
                  className="code-block"
                  dangerouslySetInnerHTML={{
                    __html: Prism.highlight(
                      refactorResult.final_code,
                      Prism.languages.python,
                      "python"
                    ),
                  }}
                />
              )}
            </div>
            <AnimatePresence>
              {flipped && refactorResult && (
                <motion.div
                  className="back-footer"
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  transition={{ delay: 0.7 }}
                >
                  <div className="points-saved">
                    <span className="points-saved-number glow-text-amber">
                      <PointsCounter to={pointsSaved} />
                    </span>
                    <span className="points-saved-label">points saved</span>
                  </div>
                  {noValidCandidate && (
                    <div className="back-note">
                      no candidate beat the original this round — unchanged code shown
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </TiltPanel>
    </div>
  );
}
