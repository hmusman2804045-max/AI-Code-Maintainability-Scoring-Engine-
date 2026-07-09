import { useRef, type ReactNode, type MouseEvent } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

interface TiltPanelProps {
  children: ReactNode;
  className?: string;
  /** max tilt in degrees */
  maxTilt?: number;
}

/**
 * Volumetric glass panel: tilts toward the cursor in 3D and carries a
 * light "sheen" reflection that pans across the surface as you move.
 */
export default function TiltPanel({ children, className = "", maxTilt = 7 }: TiltPanelProps) {
  const ref = useRef<HTMLDivElement>(null);

  const mx = useMotionValue(0.5);
  const my = useMotionValue(0.5);

  const springCfg = { stiffness: 120, damping: 16, mass: 0.6 };
  const sx = useSpring(mx, springCfg);
  const sy = useSpring(my, springCfg);

  const rotateY = useTransform(sx, [0, 1], [-maxTilt, maxTilt]);
  const rotateX = useTransform(sy, [0, 1], [maxTilt, -maxTilt]);
  const sheenX = useTransform(sx, [0, 1], ["-30%", "130%"]);
  const sheenY = useTransform(sy, [0, 1], ["-30%", "130%"]);

  function handleMouseMove(e: MouseEvent<HTMLDivElement>) {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    mx.set((e.clientX - rect.left) / rect.width);
    my.set((e.clientY - rect.top) / rect.height);
  }

  function handleMouseLeave() {
    mx.set(0.5);
    my.set(0.5);
  }

  return (
    <motion.div
      ref={ref}
      className={`tilt-panel ${className}`}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
    >
      <motion.div
        className="tilt-sheen"
        style={{ left: sheenX, top: sheenY }}
        aria-hidden
      />
      {children}
    </motion.div>
  );
}
