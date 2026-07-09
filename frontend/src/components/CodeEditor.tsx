import Editor from "react-simple-code-editor";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import { motion, AnimatePresence } from "framer-motion";

interface CodeEditorProps {
  code: string;
  onChange: (code: string) => void;
  scanning: boolean;
}

export default function CodeEditor({ code, onChange, scanning }: CodeEditorProps) {
  return (
    <div className="editor-inner">
      <div className="editor-header">
        <span className="glow-text-copper editor-title aberrate">// SOURCE.py</span>
        <span className="editor-subtitle">
          {scanning ? "SCANNING STRUCTURE…" : "paste python to analyze"}
        </span>
      </div>
      <div className="editor-body">
        <Editor
          value={code}
          onValueChange={onChange}
          highlight={(src) => Prism.highlight(src, Prism.languages.python, "python")}
          padding={16}
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 14,
            minHeight: 260,
            color: "var(--text-primary)",
          }}
        />
        <AnimatePresence>
          {scanning && (
            <motion.div
              key="laser"
              className="scan-laser"
              initial={{ top: "0%", opacity: 0 }}
              animate={{ top: ["0%", "100%"], opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{
                top: { duration: 1.1, repeat: Infinity, ease: "linear" },
                opacity: { duration: 0.2 },
              }}
            />
          )}
        </AnimatePresence>
        {scanning && <div className="scan-tint" />}
      </div>
    </div>
  );
}
