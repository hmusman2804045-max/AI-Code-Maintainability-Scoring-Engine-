import { useRef, useState, type ReactNode, type MouseEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface MagneticButtonProps {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "copper" | "ember" | "titanium";
}

const VARIANT_COLORS = {
  copper: { color: "var(--copper)", glow: "var(--copper-glow)" },
  ember: { color: "var(--ember)", glow: "var(--ember-glow)" },
  titanium: { color: "var(--titanium)", glow: "var(--titanium-glow)" },
} as const;

interface Ripple {
  id: number;
  x: number;
  y: number;
}

export default function MagneticButton({
  children,
  onClick,
  disabled,
  variant = "copper",
}: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement>(null);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [hovered, setHovered] = useState(false);
  const [ripples, setRipples] = useState<Ripple[]>([]);
  const rippleId = useRef(0);

  function handleMouseMove(e: MouseEvent<HTMLButtonElement>) {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const relX = e.clientX - rect.left - rect.width / 2;
    const relY = e.clientY - rect.top - rect.height / 2;
    setOffset({ x: relX * 0.3, y: relY * 0.45 });
  }

  function handleMouseLeave() {
    setOffset({ x: 0, y: 0 });
    setHovered(false);
  }

  function handleClick(e: MouseEvent<HTMLButtonElement>) {
    const el = ref.current;
    if (el) {
      const rect = el.getBoundingClientRect();
      const ripple = { id: rippleId.current++, x: e.clientX - rect.left, y: e.clientY - rect.top };
      setRipples((r) => [...r, ripple]);
      setTimeout(() => setRipples((r) => r.filter((rp) => rp.id !== ripple.id)), 700);
    }
    onClick?.();
  }

  const { color, glow } = VARIANT_COLORS[variant];

  return (
    <motion.button
      ref={ref}
      className="magnetic-button"
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      disabled={disabled}
      animate={{ x: offset.x, y: offset.y, scale: hovered && !disabled ? 1.04 : 1 }}
      whileTap={{ scale: 0.96 }}
      transition={{ type: "spring", stiffness: 260, damping: 14, mass: 0.4 }}
      style={{ color, boxShadow: hovered && !disabled ? `0 0 28px ${glow}` : `0 0 12px ${glow}` }}
    >
      {/* animated border trace */}
      <svg className="button-trace" aria-hidden>
        <motion.rect
          x={1.5}
          y={1.5}
          rx="24"
          fill="none"
          className="trace-rect"
          stroke={color}
          strokeWidth="1.5"
          initial={false}
          animate={{ pathLength: hovered && !disabled ? 1 : 0.08, opacity: disabled ? 0.3 : 1 }}
          transition={{ duration: 0.55, ease: "easeInOut" }}
        />
      </svg>

      <AnimatePresence>
        {ripples.map((r) => (
          <motion.span
            key={r.id}
            className="button-ripple"
            style={{ left: r.x, top: r.y, background: glow }}
            initial={{ scale: 0, opacity: 0.7 }}
            animate={{ scale: 5, opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.65, ease: "easeOut" }}
          />
        ))}
      </AnimatePresence>

      <span className="button-label">{children}</span>
    </motion.button>
  );
}
