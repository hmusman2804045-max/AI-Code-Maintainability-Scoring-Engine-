import { useMemo, useRef, type ReactNode } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import { EffectComposer, Bloom, ChromaticAberration, Vignette } from "@react-three/postprocessing";
import * as THREE from "three";

const TITANIUM = new THREE.Color("#8b9099");
const COPPER = new THREE.Color("#e8823f");
const EMBER = new THREE.Color("#ff6a2b");

function riskColor(score: number): THREE.Color {
  const t = Math.min(Math.max(score / 100, 0), 1);
  if (t < 0.5) {
    return TITANIUM.clone().lerp(COPPER, t * 2);
  }
  return COPPER.clone().lerp(EMBER, (t - 0.5) * 2);
}

interface Scene3DProps {
  riskScore: number;
  /** 0 = idle drift, 1 = analyzing/refactoring frenzy */
  intensity: number;
  burstNonce: number;
  /** DOM panels physically embedded in the 3D scene */
  stagePanel: ReactNode;
  hudPanel: ReactNode;
}

function WarpGrid({ riskScore, intensity }: { riskScore: number; intensity: number }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const geomRef = useRef<THREE.PlaneGeometry>(null);
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const original = useRef<Float32Array | null>(null);
  const t = useRef(0);
  const boost = useRef(0);

  useFrame((_, delta) => {
    boost.current += (intensity - boost.current) * Math.min(1, delta * 3);
    const frenzy = boost.current;

    t.current += delta * (1 + frenzy * 3.5);
    const geo = geomRef.current;
    if (!geo) return;
    if (!original.current) {
      original.current = Float32Array.from(geo.attributes.position.array);
    }
    const pos = geo.attributes.position as THREE.BufferAttribute;
    const src = original.current;
    const amplitude = 0.25 + (riskScore / 100) * 2.2 + frenzy * 2.4;
    const speed = 0.5 + (riskScore / 100) * 1.4 + frenzy * 2.0;
    for (let i = 0; i < pos.count; i++) {
      const x = src[i * 3];
      const y = src[i * 3 + 1];
      const wave =
        Math.sin(x * 0.18 + t.current * speed) *
          Math.cos(y * 0.18 + t.current * speed * 0.8) +
        frenzy * 0.35 * Math.sin(x * 0.9 + t.current * 6.0) * Math.sin(y * 0.7);
      pos.setZ(i, wave * amplitude);
    }
    pos.needsUpdate = true;

    if (meshRef.current) {
      meshRef.current.rotation.z += delta * (0.02 + frenzy * 0.12);
    }
    if (matRef.current) {
      matRef.current.color.copy(riskColor(riskScore));
      matRef.current.opacity = 0.45 + frenzy * 0.35;
    }
  });

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 2.3, 0, 0]} position={[0, -3.2, -4]}>
      <planeGeometry ref={geomRef} args={[44, 44, 70, 70]} />
      <meshBasicMaterial ref={matRef} wireframe transparent opacity={0.45} toneMapped={false} />
    </mesh>
  );
}

function ParticleField({
  color,
  count,
  radius,
  burstNonce,
  baseSize,
}: {
  color: string;
  count: number;
  radius: number;
  burstNonce: number;
  baseSize: number;
}) {
  const pointsRef = useRef<THREE.Points>(null);
  const burstEnergy = useRef(0);
  const lastNonce = useRef(burstNonce);

  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = radius * (0.4 + Math.random() * 0.9);
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      arr[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.5;
      arr[i * 3 + 2] = r * Math.cos(phi) - 6;
    }
    return arr;
  }, [count, radius]);

  useFrame((_, delta) => {
    if (burstNonce !== lastNonce.current) {
      lastNonce.current = burstNonce;
      burstEnergy.current = 1;
    }
    burstEnergy.current = Math.max(0, burstEnergy.current - delta * 0.55);

    if (pointsRef.current) {
      pointsRef.current.rotation.y += delta * (0.03 + burstEnergy.current * 0.5);
      pointsRef.current.rotation.x += delta * burstEnergy.current * 0.1;
      pointsRef.current.scale.setScalar(1 + burstEnergy.current * 0.35);
      const material = pointsRef.current.material as THREE.PointsMaterial;
      material.size = baseSize + burstEnergy.current * 0.14;
      material.opacity = 0.55 + burstEnergy.current * 0.45;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={baseSize}
        sizeAttenuation
        transparent
        opacity={0.6}
        depthWrite={false}
        toneMapped={false}
      />
    </points>
  );
}

function CameraDrift({ intensity }: { intensity: number }) {
  const t = useRef(0);
  useFrame(({ camera }, delta) => {
    t.current += delta;
    const shake = intensity * 0.035;
    // gentle orbital drift: the embedded DOM panels inherit this perspective
    camera.position.x = Math.sin(t.current * 0.16) * 0.55 + (Math.random() - 0.5) * shake;
    camera.position.y = 2.0 + Math.sin(t.current * 0.11) * 0.28 + (Math.random() - 0.5) * shake;
    camera.position.z = 10 + Math.sin(t.current * 0.07) * 0.35;
    camera.lookAt(0, 0, -4);
  });
  return null;
}

/**
 * The whole interface lives INSIDE the canvas: the editor stage and the
 * HUD are CSS3D-transformed by the same camera that renders the grid, so
 * camera drift continuously re-projects their perspective.
 * (WebGL post-processing cannot sample DOM pixels — bloom/aberration on
 * panel text is approximated in CSS by the theme's glow/aberrate classes.)
 */
export default function Scene3D({
  riskScore,
  intensity,
  burstNonce,
  stagePanel,
  hudPanel,
}: Scene3DProps) {
  const aberration = useMemo(
    () => new THREE.Vector2(0.0012 + intensity * 0.0025, 0.0008 + intensity * 0.0018),
    [intensity]
  );

  return (
    <div className="canvas-layer">
      <Canvas camera={{ position: [0, 2.0, 10], fov: 55 }} dpr={[1, 1.75]}>
        <color attach="background" args={["#0b0806"]} />
        <fog attach="fog" args={["#0b0806", 8, 30]} />
        <WarpGrid riskScore={riskScore} intensity={intensity} />
        <ParticleField color="#e8823f" count={700} radius={16} burstNonce={burstNonce} baseSize={0.05} />
        <ParticleField color="#ffc35e" count={350} radius={12} burstNonce={burstNonce} baseSize={0.06} />
        <CameraDrift intensity={intensity} />

        {/* forge-glass editor stage, floating above the grid */}
        <group position={[0, 1.55, 0]} rotation={[-0.05, 0, 0]}>
          <Html transform distanceFactor={4} zIndexRange={[40, 0]} className="panel3d stage-panel3d">
            {stagePanel}
          </Html>
        </group>

        {/* analytics HUD, reclined like a dashboard instrument cluster */}
        <group position={[0, -3.05, -0.4]} rotation={[0.18, 0, 0]}>
          <Html transform distanceFactor={4} zIndexRange={[30, 0]} className="panel3d hud-panel3d">
            {hudPanel}
          </Html>
        </group>

        <EffectComposer>
          <Bloom intensity={1.35} luminanceThreshold={0.18} luminanceSmoothing={0.85} mipmapBlur />
          <ChromaticAberration offset={aberration} radialModulation modulationOffset={0.4} />
          <Vignette eskil={false} offset={0.18} darkness={0.85} />
        </EffectComposer>
      </Canvas>
    </div>
  );
}
