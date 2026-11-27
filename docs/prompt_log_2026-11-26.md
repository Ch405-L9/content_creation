# Prompt log — CapCut (Nano Banana 2 / Seedance 2.0) — sessions 2026-11-25/26

Every generation prompt typed into CapCut in these sessions, verbatim and in order, tagged by outcome for pattern analysis.
Tags: GOOD (used / approved), MIXED (partly usable), BAD (rejected or failed). Timestamps are UTC from the transcript.
See docs/capcut_pipeline_learnings.md for the distilled rules.

Totals: BAD 15, GOOD 25, MIXED 7, UNKNOWN 1, BAD->GOOD 1

## 00 · BAD · 2026-11-26 01:34
**Outcome:** Design Studio: 5 stills in one request -> failed both times. One image per request.

```text
Create 5 separate photoreal cinematic stills, each its own vertical 9:16 image (1080x1920), NOT a grid or collage, no text or watermarks. They are keyframes for a slow-motion "Met Gala" style music-video intro, shot at night inside a dark Atlanta garage club: red laser beams, haze/smoke, crowd holding up phones with flash, red and white strobe light, shallow depth of field, gritty handheld phone/cinema-camera look with grain.

Characters (keep faces identical to the references in every image):
- GORDON = the young man in image 1. Wear exactly his outfit from image 1: black polo with grey shoulder panels, black fitted cap with the white "M" logo, iced-out "M" pendant on a Cuban chain, iced watch, sleeve tattoos.
- TRIXIE = the young woman in image 2 (black bob with bangs, tattoos). NEW outfit: black satin corset top, cropped red leather moto jacket, black high-waist pants, iced Cuban choker. No pink.
- THE CAR = exactly the car in image 3: matte Shadow Black Ford Mustang Dark Horse with thin red pinstripes, black wheels and calipers. ADD one thing only: a large bold red stylized "M" chevron painted on the center of the hood (like a racing hood emblem). Nothing else changed.

Shots:
1. Extreme macro of Gordon's iced "M" pendant swinging mid-air on his chest, red strobe glints on the diamonds, black polo behind.
2. Gordon walking straight toward camera through the parting crowd, low angle, slight motion blur on the crowd, red lasers behind him, confident stare into lens.
3. Trixie turning her head over her shoulder toward camera mid hair-flip, phone flashes popping around her, red jacket catching the light.
4. The Mustang parked in the middle of the club, low front three-quarter view, headlights and amber DRLs on, red "M" on the hood lit by a red laser, crowd silhouettes and phones around it.
5. Gordon leaning on the Mustang's front fender, Trixie sitting on the hood beside the red "M", both looking into the lens, crowd flashes.
```

## 01 · BAD · 2026-11-26 01:35
**Outcome:** Same multi-image request retried -> failed.

```text
Create 5 separate photoreal cinematic stills, each its own vertical 9:16 image (1080x1920), NOT a grid or collage, no text or watermarks. They are keyframes for a slow-motion "Met Gala" style music-video intro, at night inside a dark Atlanta garage club: red laser beams, haze, crowd holding up phones with flash, red and white strobe light, shallow depth of field, gritty handheld look with film grain. CHARACTERS (faces identical to the references in every image): GORDON = the young man in image 1, wearing exactly his outfit from image 1 (black polo with grey shoulder panels, black fitted cap with white "M" logo, iced "M" pendant on a Cuban chain, iced watch, sleeve tattoos). TRIXIE = the young woman in image 2 (black bob with bangs, tattoos) in a NEW outfit: black satin corset top, cropped red leather moto jacket, black high-waist pants, iced Cuban choker, no pink. THE CAR = exactly the car in image 3 (matte Shadow Black Ford Mustang Dark Horse, thin red pinstripes, black wheels and calipers) with ONE addition: a large bold red stylized "M" chevron painted in the center of the hood like a racing hood emblem; nothing else changed. SHOT 1: extreme macro of Gordon's iced "M" pendant swinging mid-air on his chest, red strobe glints on the diamonds. SHOT 2: Gordon walking straight toward camera through the parting crowd, low angle, motion blur on the crowd, red lasers behind him, confident stare into the lens. SHOT 3: Trixie turning her head over her shoulder toward camera mid hair-flip, phone flashes popping around her, red jacket catching the light. SHOT 4: the Mustang parked in the middle of the club, low front three-quarter view, headlights and amber DRLs on, the red "M" on the hood lit by a red laser, crowd silhouettes with phones around it. SHOT 5: Gordon leaning on the Mustang's front fender and Trixie sitting on the hood beside the red "M", both looking into the lens, crowd flashes.
```

## 02 · GOOD · 2026-11-26 01:38
**Outcome:** One image only, explicit model -> worked. Template for all later stills.

```text
Both attempts failed. Try a test with just ONE image first, using whichever image model is available on my current free plan at standard resolution (not 2K, not Pro models): SHOT 4 only - the car from image 3 (matte black Ford Mustang Dark Horse, red pinstripes) with a large bold red stylized M chevron painted on the center of the hood, parked in a dark garage club with red laser beams, haze and crowd phone flashes, low front three-quarter view, headlights on, vertical 9:16, photoreal, no text.
```

## 03 · GOOD · 2026-11-26 01:39
**Outcome:** Remaining shots one at a time, same model/settings -> worked.

```text
Perfect, that works. Now generate the other 4 shots the same way (same Nano Banana 2 model, standard resolution, vertical 9:16, photoreal, no text, same club lighting as this image), one separate image per shot, using my reference images: image 1 = Gordon (exact face and exact outfit from image 1: black polo with grey shoulder panels, black cap with white M, iced M pendant, iced watch, tattoos), image 2 = Trixie (exact face, black bob with bangs, tattoos; NEW outfit: black satin corset top, cropped red leather moto jacket, black high-waist pants, iced choker, no pink). SHOT 1: extreme macro of Gordon's iced M pendant swinging on his chest, red strobe glints on diamonds. SHOT 2: Gordon walking toward camera through the parting crowd, low angle, crowd motion blur, red lasers behind him, staring into the lens. SHOT 3: Trixie turning her head over her shoulder toward camera mid hair-flip, phone flashes around her, red jacket catching light. SHOT 5: Gordon leaning on the front fender of the black Mustang with the red M hood from the image you just made, Trixie sitting on the hood next to the M, both looking into the lens, crowd flashes.
```

## 04 · MIXED · 2026-11-26 01:43
**Outcome:** Identity fix by description: tattoos/hair improved, face still drifted.

```text
Redo SHOT 3 (mustang_club_shot3.png) and fix Trixie's identity: her face, skin tone, eyes, black bob with bangs, and tattoos (neck, arms and the large back tattoo) must match the attached Trixie character sheet exactly. KEEP the outfit exactly as in shot 3: black satin corset top, cropped red leather moto jacket, black high-waist pants, iced choker (red and black only, ignore the pink top and denim in the sheet). Same composition as shot 3: turning her head over her shoulder toward camera mid hair-flip, phone flashes around her, red lasers and haze, same club lighting, vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text. Also redo SHOT 5 (mustang_club_shot5.png) with the same Trixie face fix, keeping everything else.
```

## 05 · MIXED · 2026-11-26 01:46
**Outcome:** Second identity fix: face drifted again, wrong car generation.

```text
Shot 5 needs one more fix. Trixie's face drifted again and the car is the wrong generation. Regenerate SHOT 5 using: TRIXIE face, skin tone and tattoos EXACTLY as in the new shot 3 you just made (the over-the-shoulder red jacket image, mustang_club_shot3 in Section 4), same red leather jacket and black corset outfit. THE CAR exactly as in mustang_club_shot4_test.png: the 2026 Mustang Dark Horse front end (slim LED headlights with amber DRLs, large black grille, carbon hood vent), matte black, with the same clean bold red M chevron graphic centered on the hood (crisp painted graphic, not a brush stroke). GORDON exactly as now. Pose: Gordon leaning on the front fender, Trixie sitting on the hood beside the M, both looking into the lens, crowd phone flashes, red lasers, haze. Vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text.
```

## 06 · BAD · 2026-11-26 01:49
**Outcome:** Batch animate 5 clips: only 1 rendered (Seedance Mini free trial), rest hit the Upgrade paywall.

```text
Animate each of these 5 images as its own separate video clip (image-to-video, first frame = the image), with Seedance 2.0 Mini, vertical 9:16, about 5 seconds each, no text, no music. Style: Met Gala music-video intro, dreamy SLOW MOTION, subtle handheld drift, red laser beams sweeping, haze drifting, phone flashes popping in the crowd. Keep faces, outfits and the car exactly as in the images. Clip 1 (pendant): the iced M pendant swings slowly toward camera, diamonds sparkle under a red strobe, slow rack focus. Clip 2 (Gordon): Gordon walks toward camera in slow motion, crowd parts around him, flashes pop, he holds eye contact with the lens. Clip 3 (Trixie): Trixie finishes her slow-motion hair flip and settles her gaze into the lens, jacket catching red light. Clip 4 (car): slow push-in on the black Mustang, headlights flare brighter, a red laser sweeps across the red M on the hood, haze rolls over the car. Clip 5 (both): slow push-in, Gordon lifts his chin, Trixie leans back on the hood, flashes pop around them. Start with clip 4 first so I can check quality, then do the rest.
```

## 07 · BAD · 2026-11-26 01:53
**Outcome:** Paywall again -> FFmpeg push-in fallback used.

```text
Clip 4 looks great. Now generate clips 1, 2, 3 and 5 the same way (Seedance 2.0 Mini, image-to-video from each attached image, vertical 9:16, about 5 seconds, slow motion, same style and the exact motion described in my previous message), one separate video per image.
```

## 08 · UNKNOWN · 2026-11-26 01:54
**Outcome:** Slow-mo walk-in, part of the paywalled batch.

```text
Slow-motion music-video shot: the young man in the black polo and black M cap walks slowly toward the camera through the club crowd, the crowd parts around him, phone flashes pop, red laser beams sweep behind him through the haze, he holds steady eye contact with the lens, subtle handheld drift. Keep his face, outfit and chain exactly as in the image. No text.
```

## 09 · MIXED · 2026-11-26 01:59
**Outcome:** 'EXACTLY the woman in the sheet' -> closer, still not exact.

```text
Redo the Trixie shot (trixie_shot3_v2.png) so she is EXACTLY the woman in trixie_sheet_official.png: same face (soft oval face, almond-shaped eyes, full glossy lips, small nose), same light tan skin tone, same straight blunt black bob with full straight-cut bangs, same tattoos (large koi fish and yin-yang back piece with pink cherry blossoms, sleeve tattoos on both arms), and NO neck tattoo. Keep everything else from trixie_shot3_v2.png exactly: the red leather moto jacket worn off the shoulders showing the koi back tattoo, black satin corset top, black pants, iced choker, the over-the-shoulder pose looking into the lens, the club with red lasers, haze and phone flashes. Vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text.
```

## 10 · MIXED · 2026-11-26 02:01
**Outcome:** Face/skin/tattoo swap edit: tattoos+hair fixed, face still off.

```text
Edit trixie_shot3_v2.png: replace the woman's face, skin and tattoos with the exact woman from trixie_sheet_official.png. Same face as the sheet (soft oval face, almond-shaped eyes, full glossy lips, small nose, light tan skin tone), same straight blunt black bob with full bangs, her large koi fish and yin-yang back tattoo with pink cherry blossoms visible on her back, sleeve tattoos on her arms, and NO neck tattoo at all. Keep the outfit (red leather moto jacket off the shoulders, black satin corset, black pants, iced choker), the over-the-shoulder pose, framing, club, red lasers and flashes exactly as they are. Vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text.
```

## 11 · GOOD · 2026-11-26 02:07
**Outcome:** 'Edit X with two changes only' -> clean targeted edit.

```text
Edit both_mustang_shot5_v3.png with two changes only. 1) Replace the woman sitting on the hood with the exact woman from trixie_shot3_v3.png: same face, same light tan skin tone, same blunt black bob with full bangs, same koi and yin-yang back tattoo and arm sleeve tattoos, NO neck tattoo, same red leather moto jacket and black satin corset, black pants, iced choker. 2) Make the hood plain matte black with NO graphic or logo on it at all (remove the red M completely). Keep everything else exactly the same: Gordon, his pose and outfit, the 2026 Mustang Dark Horse front end with amber DRLs, the framing, crowd phone flashes, red lasers and haze. Vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text.
```

## 12 · GOOD · 2026-11-26 02:09
**Outcome:** 'ONE change only' outfit edit -> clean. Narrow edits beat regenerations.

```text
Edit both_mustang_shot5_v5_plainhood.png with ONE change only: the man standing on the left must wear exactly the outfit from gordon_outfit_sheet.jpg: black short-sleeve polo with grey shoulder panels, black fitted cap with the white M logo, iced-out M pendant on a Cuban chain, iced watch, and his sleeve tattoos visible on his forearms. Keep his face, pose and position. Keep everything else exactly the same: the woman on the hood (face, red jacket, koi back tattoo), the plain matte black hood with no logo, the Mustang, framing, lasers, haze and flashes. Vertical 9:16, standard resolution, Nano Banana 2, photoreal, no text.
```

## 13 · GOOD · 2026-11-26 04:40
**Outcome:** Exit-chase keyframes (2 stills) -> usable.

```text
Create 2 separate photoreal vertical 9:16 images (standard resolution, Nano Banana 2, no text, no watermarks, not a collage). THE CAR in both = exactly the car in ref_mustang_mach5.jpg: matte Shadow Black 2026 Ford Mustang Dark Horse, thin red pinstripes, black wheels, carbon hood vent, slim LED headlights with amber DRL strips, red M racing emblem on the hood. SETTING in both = like ref_bg_rain_highway.jpg: night, steady rain, wet black multi-lane interstate with long mirror reflections, concrete median barrier, overhead steel sign gantry with blank green signs, street lights, Georgia State Patrol cruisers with red and blue light bars FAR BEHIND the Mustang (never in front). SPEED in both = like ref_speed.jpg: well over 100 mph, heavy directional motion blur on road and barrier, long light streaks, rain spray off the tyres. IMAGE A (fly-by first frame): camera very low at bumper height at the right lane edge next to the barrier, 24mm lens, looking back up the highway; the Mustang is approaching in the centre lanes still mid-distance, headlights and amber DRLs blazing through the rain, police lights further back, gantry overhead. IMAGE B (tracking shot first frame): low tracking camera alongside the Mustang at door-handle height, 35mm, rear three-quarter side profile of the car filling the frame, barrier and street lights streaking behind in long blur lines, police light bars smeared far back.
```

## 14 · GOOD · 2026-11-26 04:43
**Outcome:** Keyframes -> usable.

```text
Create 2 separate photoreal cinematic film stills, vertical 9:16, standard resolution, Nano Banana 2, no text, not a collage. The car in both is exactly the car in ref_mustang_mach5.jpg (matte black 2026 Ford Mustang Dark Horse, red pinstripes, amber DRL strips, red M emblem on the hood). The setting in both looks like ref_bg_rain_highway.jpg: night, rain, wet multi-lane highway with long reflections, concrete barrier, overhead sign gantry with blank green signs, street lights, and police cruisers with red and blue lights far in the background behind the car. Strong motion blur and light streaks like ref_speed.jpg to show high speed. IMAGE A: very low camera at the edge of the right lane beside the barrier, wide lens, the Mustang coming toward camera in the centre lanes at mid distance with headlights glowing through the rain. IMAGE B: low camera tracking alongside the Mustang at door height, rear three-quarter side profile filling the frame, background streaking into long blur lines.
```

## 15 · GOOD · 2026-11-26 04:45
**Outcome:** Car-from-ref still -> usable.

```text
One photoreal cinematic still, vertical 9:16, standard resolution, Nano Banana 2, no text: the car from ref_mustang_mach5.jpg (matte black Ford Mustang Dark Horse with red M emblem on the hood) driving on a wet multi-lane highway at night in the rain, overhead sign gantry with blank green signs, street lights, long reflections on the road, motion blur and light streaks, very low camera at the right lane edge, the car approaching in the centre lanes with headlights glowing.
```

## 16 · GOOD · 2026-11-26 04:49
**Outcome:** Interior footwell still -> usable (C1).

```text
Create 1 photoreal cinematic film still, vertical 9:16, Nano Banana 2, no text, no readable numbers. Interior of a matte black 2026 Ford Mustang Dark Horse at night in the rain, like ref_cabin.jpg (black RECARO seats with red accents, flat-bottom steering wheel, digital instrument cluster glowing). The driver is the man from gordon_outfit_sheet.jpg (same face, black polo with grey shoulder panels, black cap with white M, iced M pendant, sleeve tattoos). Tight handheld shot from the passenger side at centre-console height: his left hand on the steering wheel, his right hand gripping the round shift knob of the six-speed manual gear lever on the centre console, and in the lower part of the frame the footwell with three pedals, his left foot pressing the clutch pedal (the left pedal) and his right foot on the accelerator. Rain streaks sideways across the windshield and side glass, street lights and blurred highway lights streaking past outside like ref_speed.jpg, the cabin lit by passing lights.
```

## 17 · BAD · 2026-11-26 04:52
**Outcome:** Shifter close-ups: wrong LHD geometry (arms from passenger side) -> rejected later.

```text
Create 2 separate photoreal cinematic close-up stills, vertical 9:16, Nano Banana 2, no text, no readable numbers, inside a left-hand-drive 2026 Ford Mustang Dark Horse at night in the rain (cabin like ref_cabin.jpg: black interior, RECARO seats with red accents). The driver sits in the LEFT seat behind the steering wheel. IMAGE C1 (footwell close-up): very low camera on the floor of the driver's footwell looking at the three metal pedals (clutch on the left, brake in the middle, accelerator on the right); the driver's left foot in a black sneaker presses the clutch pedal fully down while his right foot hovers just above the accelerator, lifting off it; dark jeans; dim red ambient light and flickers of passing street light. IMAGE C2 (gear shift close-up): camera beside the centre console looking at the driver's RIGHT hand gripping the round shift knob of the six-speed manual gear lever, sleeve tattoos and an iced watch on that forearm (from gordon_outfit_sheet.jpg), his left hand on the steering wheel softly out of focus behind, rain streaking across the windshield and blurred highway lights streaking past outside, motion blur conveying high speed.
```

## 18 · GOOD · 2026-11-26 04:57
**Outcome:** Fly-by: 'races toward the low camera ... growing' -> Video A, used.

```text
Fast fly-by shot. The black Mustang races toward the low camera at very high speed through the rain, growing huge in frame within a second, rain spray kicking off its tyres, and blasts past just a few feet from the lens; the camera whip-pans to follow it and we glimpse its glowing tail lights and rear wing speeding away up the wet highway while the police lights trail far behind. Violent motion blur, long light streaks, camera shake on the pass. Keep the car exactly as in the image. No text.
```

## 19 · BAD · 2026-11-26 05:05
**Outcome:** 'over 100 mph' + police chase wording -> CapCut 'security error'.

```text
High-speed tracking shot at over 100 mph in heavy rain at night: the camera races alongside the black Mustang at door height, slowly sliding from the front three-quarter view back along its side past the wheels while the concrete barrier, street lights and the overhead sign gantry streak past in long motion-blur lines and rain spray flies off the tyres; then the camera eases off and the Mustang surges ahead and pulls away down the wet interstate, ending on a rear three-quarter view with glowing tail lights and the rear wing, red and blue police lights far behind. Handheld shake, heavy directional motion blur. Keep the car exactly as in the image. No text.
```

## 20 · BAD · 2026-11-26 05:06
**Outcome:** Fragment resend of #19 (typing glitch).

```text
tracking shot at over 100 mph in heavy rain at night: the camera races alongside the black Mustang at door height, slowly sliding from the front three-quarter view back along its side past the wheels while the concrete barrier, street lights and the overhead sign gantry streak past in long motion-blur lines and rain spray flies off the tyres; then the camera eases off and the Mustang surges ahead and pulls away down the wet interstate, ending on a rear three-quarter view with glowing tail lights and the rear wing, red and blue police lights far behind. Handheld shake, heavy directional motion blur. Keep the car exactly as in the image. No text.
```

## 21 · GOOD · 2026-11-26 05:07
**Outcome:** Reworded ('emergency lights', 'cinematic') -> Video B tracking, used.

```text
Cinematic high-speed tracking shot in heavy rain at night: the camera travels alongside the black Mustang at door height, slowly sliding from the front three-quarter view back along its side past the wheels while the concrete barrier, street lights and overhead sign gantry streak past in long motion-blur lines and rain spray flies off the tyres; then the Mustang accelerates ahead and pulls away down the wet highway, ending on a rear three-quarter view with glowing tail lights and the rear wing, distant red and blue emergency lights far behind. Handheld feel, strong motion blur. Keep the car exactly as in the image. No text.
```

## 22 · GOOD · 2026-11-26 05:15
**Outcome:** Footwell pedals handheld -> used (cut before glitch frame at 0.67 s).

```text
Tight handheld close-up in the dark driver's footwell of a manual sports car at night, three pedals: clutch on the left, brake in the middle, accelerator on the right. In one quick fluid motion the driver's left foot stamps the clutch pedal all the way to the floor while his right foot lifts off the accelerator at the same moment; a beat later the left foot releases the clutch smoothly back up and the right foot presses the accelerator back down hard. Streaks of passing street light sweep across the pedals, the cabin vibrates with speed, slight camera shake. Realistic foot and pedal movement, keep everything as in the image. No text.
```

## 23 · BAD · 2026-11-26 05:22
**Outcome:** Shifter v1 -> wrong geometry, 'driving sideways' per user.

```text
Tight handheld close-up on the six-speed manual gear lever of the sports car at night while driving at very high speed. The driver's hand grips the shift knob and in one fast, clean, decisive motion snaps the lever straight back from fifth gear into sixth gear, then rests on the knob; the cabin shakes slightly with speed, streaks of passing street light and rain shadows sweep across the hand and console, slight camera push-in as the gear goes in. Realistic hand and lever motion, keep everything as in the image. No text.
```

## 24 · BAD · 2026-11-26 06:06
**Outcome:** New tracking take: car read as reversing -> rejected (Video 7).

```text
Cinematic high-speed tracking shot in heavy rain at night: the black Mustang drives forward the whole time and never reverses. The camera travels alongside at door height and gradually falls behind the car as it pulls ahead, so we see the front three-quarter, then the side and wheels, then the rear; finally the Mustang surges away down the wet highway, ending on a rear view with glowing tail lights and the rear wing, distant red and blue emergency lights far behind. The concrete barrier, street lights and overhead sign gantry streak past backwards in long motion-blur lines, rain spray flies off the tyres. Handheld feel, strong motion blur. Keep the car exactly as in the image. No text.
```

## 25 · GOOD · 2026-11-26 06:11
**Outcome:** 'Regenerate with correct left-hand-drive geometry ... driver left seat, right hand on console shifter' -> fixed (C2 v2).

```text
Regenerate this interior shot with correct left-hand-drive geometry for a US 2026 Ford Mustang Dark Horse six-speed manual. Camera in the front passenger seat looking left toward the driver. The driver sits in the LEFT seat facing forward, steering wheel directly in front of him on the left side of the frame, his LEFT hand on the steering wheel. The gear lever is on the center console in the middle of the frame, to the driver's right; his RIGHT arm reaches across from the driver's side (from the left of the frame) and his right hand grips the shift knob. No arm comes from the right edge of the frame. Same man: tattooed forearm sleeve, iced-out watch, black polo. Same night rain look through the windshield, red ambient cabin light, red-accent seats, highway lights streaking past. Photoreal, 9:16 vertical, no text.
```

## 26 · MIXED · 2026-11-26 06:15
**Outcome:** Passenger handheld interior -> RHD-looking framing.

```text
Handheld interior shot from the passenger seat at very high speed at night. The driver keeps looking forward through the windshield with his left hand on the steering wheel. In one fast, clean motion his right hand pulls the six-speed gear lever on the center console straight back from fifth into sixth gear, then rests on the knob. The car keeps driving forward, highway lights and rain streak past the side window from front to back, the cabin vibrates with speed, slight camera push-in toward the shifter as the gear goes in. Keep the driver, the car interior and the camera angle exactly as in the image. No text.
```

## 27 · BAD · 2026-11-26 06:33
**Outcome:** 'much LOWER' variant -> camera facing driver, RHD-like -> rejected.

```text
Same scene, same man, same car interior and same night rain, but the camera is now much LOWER: a phone held low at center-console / seat-cushion height in the passenger seat, angled upward toward the driver's face. Left-hand-drive: driver in the left seat facing forward, left hand on the steering wheel, right hand on the gear lever. His face is lit by red cabin glow and passing street light, intense focused expression looking at the road. Shot on a modern smartphone: slightly wide lens, natural phone HDR look, a little grain. Photoreal, 9:16 vertical, no text.
```

## 28 · GOOD · 2026-11-26 06:35
**Outcome:** 'Keep EXACTLY the same camera direction and layout as this reference' -> correct C3 keyframe.

```text
Keep EXACTLY the same camera direction and layout as this reference image: we see the driver in side profile from the passenger seat, he faces frame-left toward the windshield, steering wheel in front of him on the left, his LEFT hand on the wheel, his RIGHT hand on the gear lever on the center console. Do NOT turn him toward the camera and do NOT mirror anything. Only change: move the phone camera DOWN to cup-holder height and tilt it upward toward his face and jaw, so the console and his arm are big in the foreground and the headliner is visible above him. Same man, outfit, watch, tattoos, red cabin glow, rainy night highway outside. Modern smartphone photo look, slightly wide lens, a little grain. Photoreal, 9:16 vertical, no text.
```

## 29 · GOOD · 2026-11-26 06:39
**Outcome:** Phone footage low at cup-holder height -> base clip; zoom/dutch/AF hunt done locally (phone_cam.py).

```text
Handheld smartphone footage filmed by a passenger, camera held low at cup-holder height the whole time. Starting from this low framing, the operator quickly pushes in and zooms tight onto the driver's face for intensity, ending in an extreme close-up of his eyes and jaw, while the phone tilts from level into a strong dutch angle. The camera is never still: small hand shake and road vibration at very high speed. The driver stays focused on the road, jaw clenched, left hand on the wheel; passing street lights sweep across his face, rain on the windows, highway lights streaking past outside. Keep the driver, car interior and lighting exactly as in the image. No text.
```

## 30 · GOOD · 2026-11-26 09:55
**Outcome:** Club hands keyframe from char refs -> good likeness.

```text
Create a new 9:16 vertical photo in the same club as these images: the young man from the first image (EXACT same face, black polo with grey shoulder panels, black cap with M, iced-out M pendant chain, sleeve tattoos, iced watch) stands in the center facing the camera with an aggressive, confident expression, both fists pressed together in front of his chest. The woman from the second image (EXACT same face, blunt black bob with bangs, same red and black outfit, same tattoos and jewelry) stands close at his right side, leaning into him lovingly with one hand on his upper arm. Party-goers dancing behind them, red laser beams, haze, phone flashes. LOW camera angle looking up at them for a powerful look, handheld smartphone photo, slight wide lens, a little grain. Photoreal, no text, no captions.
```

## 31 · MIXED · 2026-11-26 09:58
**Outcome:** Hand routine v1 -> too stiff/aggressive vs ref ('more relaxed').

```text
Use club_hands_key_v1 as the first frame and keep both people EXACTLY as in it: his face, black cap with M, black polo with grey shoulder panels, iced M pendant chain, sleeve tattoos and iced watch; her face, blunt black bob with bangs, red and black outfit, tattoos and jewelry. Use hands_ref_crop_8s ONLY as the choreography reference: the man performs the exact same hand movements with the same timing as the reference, in a relaxed, laid-back, smooth way, fists together at the chest, a diamond shape with thumbs and index fingers, hands crossing and sweeping, the diamond again, palms rolling across his chest, fists, diamond, sweep, while keeping a hard, confident stare into the lens. Do not copy the reference person's mask, gear or background. The woman stays lovingly at his side, rubbing his arm, then turns to the camera and playfully rolls her eyes with a smirk as if to say wanna-be thug, clearly fond of him. Party-goers dance behind them, red lasers, haze, phone flashes. Camera: handheld phone held LOW looking up for a powerful look, slow pan and push-in to a close shot of both of them from the chest up, not an extreme close-up, natural hand shake. No text, no captions, no subtitles, no music.
```

## 32 · GOOD · 2026-11-26 10:06
**Outcome:** Relaxed redo -> delivered (Trixie side-eye, not a full eye roll).

```text
Use club_hands_key_v1 as the first frame and keep both people EXACTLY as in it: his face, black cap with M, black polo with grey shoulder panels, iced M pendant chain, sleeve tattoos and iced watch; her face, blunt black bob with bangs, red and black outfit, tattoos and jewelry. Use hands_ref_crop_8s_704 ONLY as the choreography reference: the man performs the exact same hand movements with the same timing as the reference, in a relaxed, laid-back, smooth way, fists together at the chest, a diamond shape with thumbs and index fingers, hands crossing and sweeping, the diamond again, palms rolling across his chest, fists, diamond, sweep, while keeping a hard, confident stare into the lens. Do not copy the reference person's mask, gear or background. The woman stays lovingly at his side, rubbing his arm, then turns to the camera and playfully rolls her eyes with a smirk as if to say wanna-be thug, clearly fond of him. Party-goers dance behind them, red lasers, haze, phone flashes. Camera: handheld phone held LOW looking up for a powerful look, slow pan and push-in to a close shot of both of them from the chest up, not an extreme close-up, natural hand shake. No text, no captions, no subtitles, no music.
```

## 33 · GOOD · 2026-11-26 10:19
**Outcome:** 'Put THIS EXACT car from the two reference images into ...' -> exact car; AI M wrong -> composited locally.

```text
Put THIS EXACT car from the two reference images into a dark underground club / parking-garage party at night: identical matte Shadow Black paint, red pinstripes on the hood graphic and twin red stripes over the roof, semi-gloss black carbon hood vent, splitter, side skirts, mirrors and rear wing, semi-gloss black 10-spoke wheels, black calipers, same lights and pony badge, no hood pins, no other changes to the car. Add one large red M emblem in the center of the hood. Same pose as the first reference: front three-quarter, nose to the left, driver side facing the camera. Dramatic LOW camera angle, crowd of party-goers holding up phones with flashes, red laser beams through thick haze, smoke rolling under the car, headlights on. Photoreal, cinematic, 9:16 vertical, no text, no people near the car doors.
```

## 34 · GOOD · 2026-11-26 10:27
**Outcome:** 5 hard cuts ~1 s each, every angle different -> cuts honored (30/46/61/98 f); door only starts to open.

```text
Multi-shot cinematic music-video sequence, 5 hard cuts, each shot about 1 second, every camera angle different. Use club_car_exact_key_v1_mach5 as the first frame; the car must stay EXACTLY as in it and as in car_APPROVED_side_driver in every shot: matte Shadow Black paint, red hood pinstripes and twin red roof stripes, the red M emblem on the front of the hood, black 10-spoke wheels, black calipers, carbon rear wing; same underground club with phone flashes, red lasers and smoke. Shots 1 to 4 are dramatic SLOW MOTION. Shot 1 (0-1s): low front three-quarter, slow push-in, headlights flare, laser sweeps across the hood. Shot 2 (1-2s): ground-level close tracking shot sliding along the driver side past the front wheel and door, smoke swirling. Shot 3 (2-3s): high overhead angle looking down on the hood and the red M as a laser crosses it. Shot 4 (3-4s): low rear three-quarter showing the rear wing and tail lights; the man from gordon_ref (same face, black cap with M, black polo with grey shoulder panels, iced M chain, sleeve tattoos) walks in from behind the camera toward the driver door. Shot 5 (4-5s): real-time, medium shot at the driver side door: he reaches the door handle and pulls the driver door open; the clip ends just as the door swings open. No text, no captions, no music.
```

## 35 · GOOD · 2026-11-26 12:54
**Outcome:** Car-sheet straight front -> good car; AI M loose -> replaced by exact composite. (first send lost to 'network connection lost')

```text
Studio car character sheet image. Show THIS EXACT car from the two reference images (2026 Mustang Dark Horse, matte black) in a straight-on FRONT view, camera at bumper height slightly above, centered, whole car visible, same light grey studio background and soft studio light as reference 1. Keep everything identical to the references: matte black paint, black grille with the pony badge, headlights, carbon hood vent, splitter, black 10-spoke wheels, mirrors. The ONLY graphic on the car is the single gloss red M on the front of the hood exactly as in reference 1, same shape, same size, centered on the hood ahead of the vent. No stripes, no numbers, no other decals or text. Photoreal, 16:9.
```

## 36 · MIXED · 2026-11-26 12:57
**Outcome:** Top-down 3/4 -> good view but hood turned carbon.

```text
New separate image for the same car sheet. Show THIS EXACT car from the two reference images (2026 Mustang Dark Horse, matte black) from directly ABOVE and slightly in front: a high top-down three-quarter view looking down onto the hood, nose toward the bottom of the frame, so the whole hood, the carbon hood vent, windshield and roof are clearly visible. Same light grey studio background and soft studio light. Keep the car identical: matte black paint, carbon vent, black 10-spoke wheels, mirrors, wing. The ONLY graphic on the car is the single gloss red M on the front of the hood exactly as in reference 1, same shape, same size, centered on the hood ahead of the vent, legs pointing to the nose, peaks toward the windshield. No stripes, no numbers, no other decals or text. Photoreal, 16:9.
```

## 37 · GOOD · 2026-11-26 13:15
**Outcome:** 'Edit image 2 only ... size/placement shown in image 1 ... logo shape image 3 ... vent slats cut through' -> the APPROVED big M look (user then asked matte).

```text
Edit image 2 only (the black Mustang front three-quarter view). Keep the car, angle, lighting and background of image 2 exactly the same. Add ONE large deep gloss red M decal on the hood, exactly the shape of the logo in image 3 and exactly the size and placement shown in image 1: the M spans most of the hood width, its two peaks start at the rear corners of the hood near the windshield base, its legs run down to the front edge of the hood, and the M passes over the carbon hood vent where the vent slats and gaps cut through the decal. Correct perspective on the hood surface, glossy clearcoat with subtle reflections. No stripes, no numbers, no other graphics or text. Same resolution and 16:9.
```

## 38 · BAD · 2026-11-26 13:16
**Outcome:** Same edit for top-down -> chat re-did the 3/4 instead.

```text
Same edit for image 2 only (the high top-down view of the same black Mustang). Keep the car, angle, lighting and background of image 2 exactly the same, and keep the hood matte black with only the vent in carbon. Add the same large deep gloss red M decal exactly as on the car in image 1: shape of the logo in image 3, peaks at the rear corners of the hood near the windshield base, legs running to the front edge of the hood, the vent slats cutting through the decal. Correct perspective, glossy clearcoat. No stripes, no numbers, no other graphics or text. Same resolution, 16:9.
```

## 39 · BAD · 2026-11-26 13:27
**Outcome:** Retry -> again re-did the 3/4. Abandoned the top-down view.

```text
Edit image 2 only (high top-down view of the same black Mustang). Keep the car, angle, lighting and background of image 2 exactly the same; keep the hood matte black with only the vent in carbon. Add the same large deep red M decal exactly as on the car in image 1, flat matte finish, same color: shape of the logo in image 3, peaks at the rear corners of the hood near the windshield base, legs running to the front edge of the hood, the vent slats cutting through the decal. Correct perspective. No stripes, no numbers, no other graphics or text. Same resolution, 16:9.
```

## 40 · BAD · 2026-11-26 13:33
**Outcome:** 'Edit image 1 only ... change ONLY the car graphics' on a busy rain frame -> thin outline 'M'. Fixed by local composite (hood_m_still.py).

```text
Edit image 1 only (vertical 9:16 rainy night highway chase). Keep EVERYTHING in image 1 exactly the same: framing, camera angle, rain, motion blur, police cars, overhead sign gantry, lighting, road, the car's position, pose and size. Change ONLY the car's graphics so it matches image 2 exactly: remove all red pinstripes and red stripes from the hood and roof, then add the ONE large deep red MATTE M decal on the hood exactly like the car in image 2 (shape of the logo in image 3, peaks at the rear corners of the hood near the windshield base, legs running to the front edge of the hood, the carbon vent slats cutting through it), seen in correct perspective, wet with rain. Matte black car, no other graphics, no text. Same 9:16 resolution.
```

## 41 · BAD->GOOD · 2026-11-26 13:37
**Outcome:** First frame + a 2nd reference image -> refused ('first-frame mode: one reference image'). Resent first-frame only -> good (Video 13 redo).

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p. Use video13_key as the exact FIRST FRAME. front34_big is the authoritative car reference: the car is this exact matte black 2026 Mustang Dark Horse with ONLY the large deep red matte M on the hood (vent slats cutting through it) - keep that M exactly as in the first frame for the whole clip, no stripes, no other graphics. Action: heavy rain at night on an Atlanta interstate, the Mustang races straight toward the camera at very high speed with headlights on, police cruisers with flashing red and blue lights chasing close behind, the overhead sign gantry passes above. Camera: low handheld tracking shot moving backward ahead of the car, slight shake, the car closes the distance and slides slightly toward the barrier side. The car always drives FORWARD, never backward. Realistic rain, spray off the tires, wet reflections. No text, no captions, no music.
```

## 42 · BAD · 2026-11-26 14:36
**Outcome:** Video 7 'tracks alongside ... pulls away ahead' from a front-3/4 first frame -> car faces camera while shrinking = reads REVERSING. Rejected.

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p, using video7_key as the exact FIRST FRAME. Keep the car exactly as in the first frame: matte black 2026 Mustang Dark Horse with ONLY the large deep red matte M on the hood (peaks at the windshield-base corners, legs to the front edge of the hood, vent slats cutting through it) - the full M becomes visible as the car moves, same shape and size the whole clip, no stripes, no other graphics. Action: heavy rain at night on an Atlanta interstate, camera tracks alongside the speeding Mustang at its front corner, low and handheld with slight shake, then the Mustang accelerates hard and pulls away ahead down the highway under the overhead sign gantry, police cruisers with flashing red and blue lights behind. The car always drives FORWARD, never backward. Spray from the tires, wet reflections. No text, no captions, no music.
```

## 43 · GOOD · 2026-11-26 14:43
**Outcome:** 4 timed hard-cut shots in 5 s (front charge / wheel / drone / rear) -> excellent speed piece.

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p, using video13_key as the exact FIRST FRAME. A fast-cut action sequence of FOUR different chase tracking shots with hard cuts, each about 1.25 seconds, no shot repeats an angle, all showing the same matte black 2026 Mustang Dark Horse with ONLY the large deep red matte M on the hood exactly as in the first frame, heavy rain at night on an Atlanta interstate, police cruisers with flashing red and blue lights chasing. Shot 1 (0-1.25s): continue the first frame, low camera racing backward just ahead of the bumper as the Mustang charges at the lens, headlights flaring, rain spray. Shot 2 (1.25-2.5s): HARD CUT, ground-level side tracking shot beside the front wheel, wheel spinning, water rooster-tail, highway lights streaking past as long blur lines. Shot 3 (2.5-3.75s): HARD CUT, drone chase from high above and behind, the Mustang weaving between lanes and leaving the police behind, the red M visible on the hood from above. Shot 4 (3.75-5s): HARD CUT, low chase-car camera behind the Mustang, tail lights and exhaust, it rockets away under the overhead sign gantry. The car always drives FORWARD in the direction it faces, never backward. Extreme sense of speed: motion blur, shaking camera, streaking lights. No text, no captions, no music.
```

## 44 · BAD · 2026-11-26 15:05
**Outcome:** Reference-only (no first frame) emblem close-up -> started on grey studio, drifted to wheel. Rejected.

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p. Use front34_big ONLY as the car reference (do not use it as the first frame): this exact matte black 2026 Mustang Dark Horse with the large deep red matte M on the hood. Shot: cinematic SLOW MOTION, LOW camera very close to the front grille, a slow gliding push-in and slight arc around the nose toward the driver-side front fender. Hero subject: the chrome running-horse pony emblem in the black honeycomb grille, polished HIGH GLOSS, perfectly lit by a soft key light and a sharp rim light that rakes across the horse so it gleams and stands out against the dark grille, small specular glints moving across it. As the camera arcs, the factory Dark Horse fender emblem (black horse-head badge with gray accents) on the front fender comes into view in the background, softly lit. Setting: dark underground club garage at night, light haze, faint red laser glow and phone flashes far behind, out of focus. Shallow depth of field, crisp focus on the pony emblem, glossy reflections. No text, no captions, no music, no people near the car.
```

## 45 · GOOD · 2026-11-26 15:13
**Outcome:** Emblem keyframe still (low, high-gloss pony, rim light) -> excellent.

```text
Vertical 9:16 cinematic still of THIS EXACT car from the reference (matte black 2026 Mustang Dark Horse, large deep red matte M on the hood). LOW camera just above the ground, extreme close-up of the front grille from a slight driver-side angle: the running-horse pony emblem fills the center of the frame, polished HIGH GLOSS chrome, perfectly lit by a soft key light plus a sharp rim light raking across the horse so it gleams and stands out against the dark black honeycomb grille, with small specular highlights. Behind it, slightly out of focus, the driver-side front fender with a small black Dark Horse fender badge with gray accents, and the lower edge of the red M on the hood visible at the top of frame. Setting: dark underground club garage at night, light haze, faint red laser glow and phone-flash bokeh far behind. Shallow depth of field, photoreal, no text, no people.
```

## 46 · GOOD · 2026-11-26 15:15
**Outcome:** Slow push-in from that keyframe -> good; requested ARC to the fender badge ignored.

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p, using emblem_key as the exact FIRST FRAME. Cinematic SLOW MOTION. The low camera glides very slowly forward and arcs slightly to the left around the front of the car while a soft beam of light sweeps across the high-gloss chrome pony emblem, making it gleam with moving specular highlights; the emblem stays the hero, sharp and centered. As the camera arcs, the driver-side front fender softly comes into view behind it with a small black Dark Horse fender badge with gray accents, out of focus. Haze drifts slowly, red laser glow and phone-flash bokeh far behind. The car does not move. Keep the car exactly as in the first frame (matte black, black honeycomb grille, the red M on the hood). No text, no captions, no music.
```

## 47 · GOOD · 2026-11-26 15:57
**Outcome:** 'Location: EXACTLY image 1 (board ATL overpass) ... car: images 2+3 ... seen from BEHIND driving AWAY' -> matches board backdrop.

```text
Vertical 9:16 photoreal night film still. Location: EXACTLY the Atlanta downtown interstate under the concrete overpass from image 1 (same road, overpass, lights and city atmosphere), reframed vertically. Car: THIS EXACT matte black 2026 Mustang Dark Horse from images 2 and 3 (black 10-spoke wheels, carbon wing, large deep red matte M on the hood), seen from BEHIND at a rear three-quarter angle, driving AWAY from the camera down the lane under the overpass, its red tri-bar tail lights glowing and reflecting on the wet asphalt. Camera low near the road surface, static, the car in the middle distance, slightly left of center. Moody, dark, cinematic, cool streetlight tones. No text, no people, no other graphics on the car.
```

## 48 · GOOD · 2026-11-26 16:01
**Outcome:** Two timed shots (drive-away / hard cut to approach with skyline) -> cut at 2.29 s, re-timed to reference.

```text
Generate one video with Seedance 2.0, 9:16, 5 seconds, 720p, using escape_p1_key as the exact FIRST FRAME. Two shots with one hard cut, dark moody night film look. Shot 1 (0-1.9s): continue the first frame exactly, static low camera, the matte black Mustang Dark Horse accelerates AWAY from the camera down the Atlanta interstate under the concrete overpass, red tri-bar tail lights streaking on the wet road, it shrinks into the distance. Shot 2 (1.9-5s): HARD CUT to a wide, very low static camera at the edge of a dark empty Atlanta road at night, curved painted lane lines in the foreground, the lit downtown Atlanta skyline (towers like Bank of America Plaza and the Westin) glowing on the horizon, the same Mustang approaching from far away toward the camera with bright bluish-white headlights, growing larger. The car always drives forward in the direction it faces. No police in this clip. No text, no captions, no music.
```

## Later session (escape pieces 3, 4, 6, storyboard-first)
50. GOOD: Design Studio, gas station: "Edit image 1 only: keep EXACTLY the same gas station, camera position… ONE change only:
    replace the white car with THIS EXACT car from image 2 … Hood: plain matte black, NO graphics…" → clean car swap, plain hood
    ready for the local M.
51. BAD (accident): clicked CapCut's suggestion chip "Increase wetness of pavement" while aiming for Download; it started an
    edit, and Stop still charged 14 cr. Use find→ref for Download, never coordinates near the chips.
52. GOOD: Seedance piece 3, first frame only, 3 timed shots (gas station headlights → HARD CUT interstate → low cam blast-past).
    Cuts landed at 2.375 s / 3.85 s (requested 2.0 / 4.0).
53. GOOD: Design Studio piece 4: "Location: EXACTLY image 1 (board BG D) … remove the other cars and all readable text …
    seen from DIRECTLY BEHIND, close rear chase-camera … driving AWAY" → clean rear chase key with the real ATL skyline.
54. GOOD: Seedance piece 4: rear chase → HARD CUT wider follow → HARD CUT side-profile tracking. Cuts ≈1.7 s / 2.875 s.
55. GOOD: Design Studio piece 6: board overpass BG, "REAR THREE-QUARTER view … driving AWAY into the shadow under the overpass".
56. GOOD: Seedance 2.0 MINI (15 cr, 720p 9:16 5 s) piece 6, first frame escape_p6_key: "Shot 1 (0-0.8s) drives AWAY … under the
    overpass … Shot 2 (0.8-2.6s): HARD CUT low static camera at curb level … coming TOWARD the camera, headlights flooding the
    lens … Shot 3 (2.6-5.0s): same low handheld camera, NO cut: rockets past right beside the lens … camera shakes … tail lights
    shrink". All three beats landed (cut at 1.25 s; flyby ≈3.6-4.2 s). Hood M drawn as a small red M band (not sheet size), ~0.4 s.
57. BAD: Google AI Studio, Gemini Omni 1.2 Flash at 1080p, keyframe only, fast piece 4 prompt → only "Thoughts", no video
    (output streams at 720p; set 720p). Use the badgch account (/u/1, PRO plan, "No API key selected").
58. MIXED: Omni 1.2 Flash 720p 9:16 5 s, images: escape_p4_key + car sheet v2 preview + front_bigM_matte_v3 + gordon_outfit_sheet,
    prompt with chase-track/whip-pan/handheld/low-mid camera language → car + M consistent (best yet), but only 2 shots (cut 2.92 s),
    no whip-pan, motion calmer than the Seedance v1 (mean frame diff 5.6 vs 10.4). Original: assets/originals/aistudio_gen/escape_p4_omni_fast_v1.mp4
59. BAD: Omni video edit with uploaded reference video → "Input blocked: uploaded video … not available in your region".
60. GOOD: Nano Banana 2.1 (AI Studio) "Edit <key> only. Keep EXACTLY the same image … ONE change only: replace the black car
    with the exact car from MUSTANG_DH_M_CAR_SHEET … same angle, position, size, blur" → 6/6 clean swaps, backgrounds untouched.
61. GOOD: Omni 1.2 Flash 3 s from swapped key + car sheet, camera move described (locked-off low cam / whip-pan) → usable; daily cap
    hit after ~4 runs. 62. GOOD: Seedance Mini 16:9 from swapped key (shift-down, victory). 63. BAD: Seedance Mini refused
    twice ("temporary security restriction", credits returned) on victory v1 and calm — a plainer prompt worked once.
