# Cutscene: Exit Chase (Mustang) — prompt pack v1

Source of choreography (reference only, third-party clip, never used as footage):
`~/Desktop/speed_create_now-00_[cutscene_exiting_chase|driving_3-5_sec.cut].mp4`, 0.3–4.6 s.
Background reference: `assets/graphics/scene_refs/bg_rain_highway_gsp_chase.png` (rain, night, overhead sign gantry, GSP pursuit).
Speed reference: `assets/graphics/scene_refs/speed_reference.png` (long light streaks, road motion blur).
Car reference: `assets/proxies/car_shot4_mach5logo_v5.png` / `assets/mustang-sc-proto/outputs/S01_B_edit1_APPROVED.png`.

## Continuity lock (paste into every prompt)

> Matte Shadow Black 2026 Ford Mustang Dark Horse, thin red pinstripes, black 10-spoke wheels, black calipers, carbon hood vent, slim LED headlights with amber DRL strips, tall rear wing, a large red stylized "M" racing emblem on the hood. Night, steady rain, wet black asphalt with long mirror reflections, multi-lane interstate with concrete median barrier and an overhead steel sign gantry (green signs, no readable text), sodium and LED street lights, Georgia State Patrol cruisers with red-and-blue light bars far behind. The car is doing well over 100 mph: heavy directional motion blur on road, barrier and lights, long light streaks, rain spray off the tyres. Photoreal, cinematic, 9:16 vertical, 24 fps, shallow depth of field, gritty handheld feel. No text, no watermarks, no license plate text.

**Negative (all shots):** text, captions, readable signs or plates, logos other than the hood M and pony badge, white car, Corvette, McLaren, daylight, dry road, underpass ceiling, police car in front of the Mustang, extra doors, warped wheels, morphing car shape, slow or static traffic speed.

## Shot A — Fly-by (target 1.3 s; generate 5 s, use the strongest 1.3 s)

*First frame:* Camera planted low (bumper height) at the right lane edge beside the barrier, lens ~24 mm, looking back up the highway. The Mustang is small and far away in the centre lanes, headlights and amber DRLs blazing through the rain, red-and-blue police lights further behind, gantry overhead.

*Motion prompt:* The black Mustang rockets toward the camera at over 100 mph, growing huge in frame within a second, rain spray kicking off its tyres, and blasts past just a few feet from the lens; the camera whip-pans right to follow it and we glimpse the glowing tail lights and rear wing disappearing up the highway as police lights trail far behind. Violent motion blur, light streaks, camera shake on the pass.

## Shot B — Tracking orbit and pull-away (target 3.0 s; generate 5 s)

*First frame:* Low tracking camera alongside the Mustang at matching speed, rear three-quarter side profile, camera at door-handle height, ~35 mm, the concrete barrier and street lights streaking behind into long motion-blur lines, wet road blurred, police light bars smeared far back.

*Motion prompt:* Smooth but handheld-feeling tracking shot at over 100 mph: the camera slowly orbits forward along the car's side from the rear quarter toward the front, revealing the front wheel, the amber DRL and the red hood emblem, while the background streaks past; then the camera eases off and the Mustang pulls away ahead, ending on a rear three-quarter view of the car charging down the rain-soaked interstate under the sign gantry, tail lights glowing, red-and-blue lights far behind.

## Shot C — Interior gear change cutaway (target 1.5 s; generate 5 s) — separate prompt, do not merge

*First frame:* Tight handheld interior shot from the passenger footwell/centre-console height looking toward the driver's side: Gordon (black polo with grey shoulder panels, iced M pendant, sleeve tattoos, black M cap) in the RECARO seat with red accents; his left hand on the flat-bottom steering wheel, right hand gripping the shift knob of the six-speed manual gear lever on the centre console; footwell visible with the three pedals (clutch left, brake middle, accelerator right). Rain-streaked windshield with blurred highway lights rushing past, digital instrument cluster glowing (no readable text).

*Motion prompt:* Fast, authentic manual shift at over 100 mph: his left foot presses the clutch (left pedal) to the floor while his right foot eases off the accelerator, his right hand snaps the gear lever from 5th into 6th in one clean motion, then the clutch comes back up and his right foot goes back down on the throttle; the cabin shakes slightly with speed, street lights strobe across his face and hands, raindrops streak sideways across the glass. Handheld camera, quick push-in on the shifter as the gear goes in.

*Alt (only if you want the left hand):* replace "right hand" with "left hand" and "left-hand-drive" with "right-hand-drive Mustang"; note this is not authentic for a US car.

## Post notes

- Trim to frame counts in the edit (24 fps): A = 31 frames, B = 72, C = 36.
- The hood "M" from generators is approximate; replace with the true Mach 5 logo in post where it is clearly visible (edit/tools/hood_logo.py on stills; video needs tracking).
- Sound: engine at high load + downshift/upshift from `assets/originals/sfx_zr1x/` (cockpit_110mph_downshift, passing-by), rain bed, siren swell.
