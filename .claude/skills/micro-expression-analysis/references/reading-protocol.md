# Reading Protocol — from pixels to careful claims

The pipeline gives you evidence; this protocol governs what you may say about
it. The point is not caution for its own sake: expression analysis of real
people fails in predictable ways, and each rule below blocks one failure mode.

## 1. Assign roles by continuity, not coordinates

Group face chips into anonymous roles (A, B, C…) using clothing, hairstyle,
build, and scene position *as seen across time*. Never cluster by pixel
x-coordinate — any camera pan silently reshuffles who is where. State the
visual cues that anchor each role so the user can audit your grouping.

## 2. What FER labels are worth

The FER+ classifier sees a 64×64 grayscale crop. On small, motion-blurred,
recompressed faces it collapses toward "neutral"; a scattered "happiness" hit
is corroboration, not proof, and "contempt/disgust" on a tiny face is almost
always noise. Rules of thumb:

- Face width ≥ 60px, sharp: label is usable as weak evidence.
- Face width < 40px or blurred: ignore the label; read posture instead.
- Never build a claim on a single chip. Look for runs (several consecutive
  chips agreeing) and cross-check against what the body is doing.

## 3. The observables that actually carry information

Ranked by reliability at typical phone-video quality:

1. **Where attention goes** — head/gaze orientation over time; who tracks
   whom; who never looks at whom. Phones in hands: who films, aimed at what,
   for how long (sustained filming is an allocation of attention).
2. **Posture and spatial deference** — who stands in front, who stays half a
   step behind, who repositions to watch, who leaves/returns and how they
   move (ducking past a camera signals awareness of the recording).
3. **Timing correlations** — expression/gesture changes synchronized with
   events (a laugh burst in audio, a peak in motion.csv, someone entering).
4. **Facial expression** — last, and only per rule 2.

## 4. Confidence vocabulary (mandatory)

Attach one of these to every interpretive claim, and say what it rests on:

- **高置信 / high** — multiple independent observables agree across time.
- **中等 / medium** — one strong observable, or several weak ones.
- **推测 / speculative** — a plausible reading; alternatives exist. Name the
  main alternative.

Absence of evidence is a reportable finding: "no visible antagonism" is a
conclusion, state it plainly rather than inventing tension to seem insightful.

## 5. Privacy & dignity lines (non-negotiable)

- All processing local. No frame, chip, or audio leaves the machine.
- No identification of real persons; roles stay anonymous (A/B/C…). If the
  user names people, you may use their labels but add nothing to them.
- Psychological attributions (intent, scheming, deceit) are always labeled as
  interpretation, never asserted as fact about a real person.
- Close every relational/psychological report with a short disclaimer block
  stating the above and the video-quality limits of the analysis.
