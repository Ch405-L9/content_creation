# Chase camera language → AI video prompts (method v2, 2026-11-27)

Rig → words the model understands (describe what the camera DOES, never the rig name alone):
- Russian Arm camera car: "low tracking shot from a camera car at bumper height, matching the car's speed"
- Hard/crash mount: "camera locked to the front bumper, road rushing underneath"
- FPV drone: "FPV drone chasing one meter above the asphalt, banking with the car"
- Roadside lock-off: "low static camera at the barrier, car blasts past within a few feet of the lens"
- Whip-pan: "fast whip-pan with heavy directional motion blur, then the camera snaps to a stop"

Speed cues (always include 2–3): foreground objects whipping past, lane lines streaking, wide lens close to the car
(strong parallax), background motion blur with the car sharp, micro handheld shake and road vibration, low/mid angle.

Structure:
- Veo/Omni: shot type → subject → action → setting → camera (ONE move) → lens/look → sound.
- Seedance: "Shot 1 (0–1.2 s) … HARD CUT … Shot 2", one move per shot; first frame = car-sheet keyframe.
- Always: direction of travel vs camera; "no text, no captions, no music, engine and tire sound only".
- Edit rhythm (cuts, flash frames, timing) is done locally to the reference frame counts — the model only makes clean shots.

## Next-shot prompts (v2)
1 BUILD-UP (first frame k1): Low static roadside shot, camera at lane level against the left concrete barrier, 24mm wide
  lens. The matte black Mustang with the big matte red M on the hood blasts into frame from the left within a few feet of
  the lens, a smear of motion blur, then rockets straight away down the empty night highway lane toward the vanishing
  point, tail lights shrinking fast. Camera locked, tiny road-vibration shake as it passes. Engine roar and tire hiss only.
2 SPEED (first frame k2b): Road-level camera, 18mm, the Mustang tears out of frame right with its tail lights smearing;
  the camera does one fast whip-pan up and left under the green overhead highway signs with heavy directional motion
  blur, then snaps to a stop on the long lane between the lamp posts, the car tiny and far away. Engine scream fading.
3 SHIFT-DOWN (first frame k3): Low tracking shot from a camera car at bumper height, behind-left, handheld feel. The
  Mustang fills the frame rear three-quarter, tail lights glowing, then downshifts and pulls away, drifting into the
  center lane; lane lines streak under the lens, green signs and the city skyline slide in on the left. Exhaust crackle.
4 VICTORY (first frame k4): Static camera with a small pan follow. The Mustang, rear three-quarter, drives away under the
  concrete overpass into the dark, shrinking, tail lights the brightest thing in frame. Engine fading.
5 CALM (first frame k5): Side-profile tracking shot from a camera car at the Mustang's exact speed, 50mm, near
  silhouette: red tail glow, thin rim light along the roof, road blurred beneath, car sharp and steady. Low engine hum.

## Lessons (2026-11-27)
- NEVER name equipment ("tripod", "camera car", "drone", "rig") — Omni rendered a literal tripod in frame (victory v2, rejected).
  Say "locked-off camera", "the camera glides alongside", "empty foreground, no equipment or people in frame".
- Arena video: 2 generations per 24 h (battle = 2 models each). Model B in the speed battle put a red M on the DOOR (reject);
  model B in the build-up added cuts and ran 10 s. Arena A clips (5 s, 1280x720) were the keepers.
- Omni with a 4 s duration and the new wording: shift-down v2 matched the reference move (signs + skyline slide in left).
