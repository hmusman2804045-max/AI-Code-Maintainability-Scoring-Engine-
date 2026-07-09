import { useState } from "react";
import Scene3D from "./components/Scene3D";
import CodeEditor from "./components/CodeEditor";
import AnalyticsHUD from "./components/AnalyticsHUD";
import FlipStage from "./components/FlipStage";
import MagneticButton from "./components/MagneticButton";
import GlitchTitle from "./components/GlitchTitle";
import { scoreCode, refactorCode, type ScoreResult, type RefactorResult } from "./api";

const SAMPLE_CODE = `global_counter = 0

def bloated_pipeline(data):
    global global_counter
    try:
        for x in data:
            if x > 0:
                for i in range(x):
                    try:
                        if i % 2 == 0:
                            global_counter += 1
                    except:
                        pass
    except Exception:
        return -1
    return global_counter
`;

export default function App() {
  const [code, setCode] = useState(SAMPLE_CODE);
  const [scoreResult, setScoreResult] = useState<ScoreResult | null>(null);
  const [refactorResult, setRefactorResult] = useState<RefactorResult | null>(null);
  const [scoring, setScoring] = useState(false);
  const [refactoring, setRefactoring] = useState(false);
  const [burstNonce, setBurstNonce] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [flipNonce, setFlipNonce] = useState(0);
  const [statusMessage, setStatusMessage] = useState("");
  const [statusError, setStatusError] = useState(false);

  async function handleScore() {
    setScoring(true);
    setStatusMessage("");
    setStatusError(false);
    setRefactorResult(null);
    setFlipped(false);
    try {
      const result = await scoreCode(code);
      if (result.error) {
        setStatusMessage(result.message ?? "Scoring failed.");
        setStatusError(true);
        setScoreResult(null);
      } else {
        setScoreResult(result);
        setBurstNonce((n) => n + 1);
      }
    } catch (err) {
      setStatusMessage(err instanceof Error ? err.message : "Scoring failed.");
      setStatusError(true);
    } finally {
      setScoring(false);
    }
  }

  async function handleRefactor() {
    setRefactoring(true);
    setStatusMessage("");
    setStatusError(false);
    try {
      const result = await refactorCode(code);
      if (result.error) {
        setStatusMessage(result.message ?? "Refactor failed.");
        setStatusError(true);
      } else {
        setRefactorResult(result);
        setFlipped(true);
        setFlipNonce((n) => n + 1);
        setBurstNonce((n) => n + 1);
      }
    } catch (err) {
      setStatusMessage(err instanceof Error ? err.message : "Refactor failed.");
      setStatusError(true);
    } finally {
      setRefactoring(false);
    }
  }

  function handleFlipBack() {
    setFlipped(false);
    setFlipNonce((n) => n + 1);
  }

  const intensity = scoring || refactoring ? 1 : 0;

  const stagePanel = (
    <div className="stage-3d">
      <FlipStage
        front={<CodeEditor code={code} onChange={setCode} scanning={scoring} />}
        flipped={flipped}
        refactorResult={refactorResult}
        initialScore={scoreResult}
        flipNonce={flipNonce}
      />
      <div className="editor-actions">
        <MagneticButton
          onClick={handleScore}
          disabled={scoring || refactoring || !code.trim()}
          variant="copper"
        >
          {scoring ? "ANALYZING…" : "ANALYZE RISK"}
        </MagneticButton>
        <MagneticButton
          onClick={handleRefactor}
          disabled={!scoreResult || !!scoreResult.error || refactoring || scoring}
          variant="ember"
        >
          {refactoring ? "REFACTORING…" : "AUTO-REFACTOR"}
        </MagneticButton>
        {flipped && (
          <MagneticButton onClick={handleFlipBack} variant="titanium">
            RETURN TO SOURCE
          </MagneticButton>
        )}
      </div>
      <div className={`status-line ${statusError ? "error" : ""}`}>{statusMessage}</div>
    </div>
  );

  const hudPanel = <AnalyticsHUD result={scoreResult} />;

  return (
    <div className="app-shell">
      <Scene3D
        riskScore={scoreResult?.risk_score ?? 0}
        intensity={intensity}
        burstNonce={burstNonce}
        stagePanel={stagePanel}
        hudPanel={hudPanel}
      />
      <div className="crt-layer" aria-hidden />
      <header className="app-header-overlay">
        <GlitchTitle text="MAINTAINABILITY ENGINE" />
        <p className="app-subtitle">
          AST-driven risk scoring + autonomous AI refactoring, forged in 3D
        </p>
      </header>
    </div>
  );
}
