import { motion, AnimatePresence } from "framer-motion";
import RiskGauge from "./RiskGauge";
import type { ScoreResult } from "../api";

interface AnalyticsHUDProps {
  result: ScoreResult | null;
}

const levelColor: Record<string, string> = {
  Low: "var(--titanium)",
  Medium: "var(--amber)",
  High: "var(--ember)",
};

export default function AnalyticsHUD({ result }: AnalyticsHUDProps) {
  return (
    <AnimatePresence>
      {result && !result.error && (
        <motion.div
          key="hud"
          className={`glass-panel hud-panel ${result.risk_level === "High" ? "hud-pulse" : ""}`}
          initial={{ opacity: 0, clipPath: "inset(0 100% 0 0)", y: -24, skewX: -8 }}
          animate={{ opacity: 1, clipPath: "inset(0 0% 0 0)", y: 0, skewX: 0 }}
          exit={{ opacity: 0, clipPath: "inset(0 0 0 100%)", y: -10 }}
          transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className="hud-header">
            <span className="glow-text-amber hud-label aberrate">// ANALYTICS HUD</span>
            <span className="hud-header-line" />
          </div>

          <div className="hud-grid">
            <RiskGauge score={result.risk_score} />

            <div className="hud-right">
              <motion.div
                className="hud-badge"
                style={{
                  color: levelColor[result.risk_level],
                  borderColor: levelColor[result.risk_level],
                }}
                initial={{ opacity: 0, scale: 0.6 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5, type: "spring", stiffness: 300, damping: 16 }}
              >
                {result.risk_level.toUpperCase()} RISK
              </motion.div>
              <motion.div
                className="hud-confidence"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
              >
                confidence {(result.confidence * 100).toFixed(0)}%
              </motion.div>

              <motion.ul
                className="hud-factors"
                initial="hidden"
                animate="visible"
                variants={{
                  hidden: {},
                  visible: { transition: { staggerChildren: 0.12, delayChildren: 0.8 } },
                }}
              >
                {result.top_risk_factors.map((factor, i) => (
                  <motion.li
                    key={i}
                    variants={{
                      hidden: { opacity: 0, x: -18, filter: "blur(4px)" },
                      visible: { opacity: 1, x: 0, filter: "blur(0px)" },
                    }}
                  >
                    <span className="hud-factor-marker">▸</span> {factor}
                  </motion.li>
                ))}
              </motion.ul>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
