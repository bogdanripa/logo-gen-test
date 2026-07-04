# Rebuilding a flower logo as a scalable, transparent SVG — process notes

Starting point: a single JPEG of a flower-in-circle logo on a solid cream
background (`00-reference-image.jpeg`). Goal: an equivalent vector logo with
a transparent background that scales cleanly. What follows is the actual
sequence of attempts, in order, including the ones that didn't work.

## 00 — Reference

`00-reference-image.jpeg` — the only input. Colors and geometry (circle
radii, petal angles, leaf placement) were reverse-engineered from this file
by sampling pixel colors and scanning radial cross-sections in Python.

## 01 — First attempt: pointy petals

`01-first-attempt/` — petals built as symmetric pointed-bezier shapes
("marquise" outlines) rotated around the center. Looked like a sharp
6-pointed star, not the soft rounded flower in the reference. Also shipped
with a real bug: `<use href="#...">` without an `xlink:href` fallback,
which silently drops in a number of SVG viewers and would have dropped
every petal for anyone whose tooling didn't support the bare attribute.

## 02 — Rounded petals

`02-rounded-petals/` — reshaped the petal path so it tapers like a teardrop
instead of a symmetric point. Much closer, but still not a match — the
proportions (how wide each petal gets, and where along its length) were
eyeballed rather than measured.

## 03 — Measuring the source image, and a failed spline attempt

`03-measurement-and-failed-spline/` — went back to the reference JPEG and
measured actual petal half-width at a dense set of radii (`fit_petal.py`),
then tried to build the petal outline as a smoothing spline straight
through the measured points (`gen_svg3.py`). Result: `failed_spline_result.png`
— a lumpy, faceted shape. Accurate measurements at sparse sample points
don't imply a smooth curve; interpolating through noisy real-world
measurements amplifies the noise into visible creases. Lesson: more data
isn't automatically better if the fitting method doesn't match the shape.

`aligned_measurement_comparison.png` and `overlay_diff.png` are from the
analysis pass used to figure out *why* things looked off (cropping both
images to the same circle radius/scale and diffing them directly, rather
than eyeballing).

## 04 — Vectorization / tracing exploration (abandoned)

`04-vectorization-exploration/` — tried classifying every pixel of the
source image to its nearest palette color and tracing each color region
with `potrace` for an exact outline instead of an approximated one. The
per-color masks came out clean (`mask_*.png`), but this path was dropped
in favor of the interactive-editor approach below, which gave more
direct control for hand-tuning.

## 05 — Pivot: an interactive HTML editor

`05-interactive-editor/` — rather than continuing to guess bezier curve
parameters, built a self-contained HTML tool (`editor.html`, in the repo
root) that overlays a live SVG (petals as plain ellipses, fully
parameterized) on top of the reference image, with sliders for every
shape parameter and an opacity/difference-blend toggle for precise visual
alignment. This shifted the fitting problem from "guess curve math" to
"a human drags sliders until it lines up," which is a much better fit for
matching a piece of hand-drawn art.

## 06 — Final logo from hand-tuned parameters

`06-final-from-tuned-params/` — the parameters dialed in with the editor,
baked into the final `logo.svg`/`logo.png` at the repo root
(`build_final.py` does the JSON-params-to-SVG conversion).

## 07 — Leaf/petal stacking-order fix

`07-leaf-zorder-fix/` — after the shapes matched, the leaves were still
rendering underneath the petals wherever they overlapped, clipping off the
leaf tips (`before_bug.png`) instead of staying intact like the reference
(`reference.png`). Fixed by moving the leaf elements later in the SVG
document order so they paint last (`after_fix.png`).

## Artifacts referenced above but living elsewhere in the repo

- `editor.html` — the interactive tuning tool (step 05)
- `logo.svg` / `logo.png` — the final result (step 06/07)
- `docs/comparison.png` — an earlier side-by-side comparison saved on request
