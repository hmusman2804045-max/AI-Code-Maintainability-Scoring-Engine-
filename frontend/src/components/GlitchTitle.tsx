interface GlitchTitleProps {
  text: string;
}

/**
 * Kinetic glitch typography: two chromatic ghost copies (ember / titanium)
 * clip-slice and jitter over the base text on a broadcast-interference loop.
 */
export default function GlitchTitle({ text }: GlitchTitleProps) {
  return (
    <h1 className="glitch-title" data-text={text}>
      {text}
    </h1>
  );
}
