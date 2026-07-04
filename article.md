# LLMs, smart as they are, still cannot do basic things like duplicating a graphic image

A friend of mine is redoing his website and asked me for a hand with the logo. He sent it over the only way most people send a logo: a screenshot. A little flower inside a circle, pink petals, a gold ring in the middle, two leaves at the bottom, sitting on a cream background.

That's fine for a website hero image, but it's the wrong format for basically everything else — a favicon, a dark-mode header, a large-format print, a version where the brand wants to swap the pink for their new color palette. What he actually needed was a vector: an SVG, built from shapes and math instead of pixels, so it scales to any size and drops onto any background because it doesn't have one.

So: recreate this JPEG as a clean, transparent, infinitely-scalable SVG. Should be a fifteen-minute job for an AI that can write code and can *see* the image I sent it. That's what I thought, anyway.

## Attempt one: just ask

I handed the screenshot to Claude (Opus 4.8) and asked it to recreate it as an SVG. It came back fast, with a confident little flower — six petals, a ring, two leaves, all in roughly the right colors. Except the petals were sharp and pointy, like a six-pointed star, where the original was soft and round.

![First attempt: pointy, star-like petals instead of soft rounded ones](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/01-first-attempt/render.png)

Not a big deal, I figured — just describe the problem and let it fix its own drawing. So I did. It rounded the petals off. Better! Except now the proportions were wrong — the flower didn't fill the circle the way the original did, the petals bulged in the wrong places.

![Second attempt: rounder, but still visibly off in proportion](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/02-rounded-petals/compare.png)

Every round went the same way: I'd say "closer, but still not it," Claude would nudge some numbers, and the result would drift into a *different* kind of wrong. It never converged. That's when it stopped being a "prompt it better" problem and started being interesting.

## Why this actually happens

Here's the part that surprised me enough to want to write about it. Claude isn't drawing your logo. It's *describing* your logo to itself, in words and numbers, and then writing code from that description.

When you hand a vision-capable LLM an image, it doesn't get pixels the way Photoshop does. The image is run through a vision encoder and turned into the same kind of token representation the model uses for text — a rich, abstract, *semantic* summary. That representation is fantastic for "what is this a picture of" (a flower logo, pink petals, a gold center, two leaves) and useless for "what is the exact radius of the third petal in pixels." The precise geometry — the thing you actually need to redraw something exactly — is exactly what gets thrown away in that translation.

So when it writes the SVG, it's not tracing your image. It's generating plausible-looking shapes from a fuzzy mental picture of it, the way you might sketch a logo from memory an hour after glancing at it. It'll get the gist right and the measurements wrong, every time, because it never had the measurements to begin with.

The other half of the problem is just as important: even when I *did* go measure the source image precisely — I had Claude write Python to sample pixel colors and scan the flower at every angle to get real numbers for petal width and length — turning a table of numbers back into a smooth, natural-looking curve is its own hard problem. One pass at this produced a flower that was technically closer to the measurements and looked *worse*: lumpy, faceted, like a gear instead of a petal.

![The measure-everything approach, rendered: technically closer to the numbers, but lumpy and unnatural](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/03-measurement-and-failed-spline/failed_spline_result.png)

More precision, worse result. What was actually missing wasn't more measurement — it was a *feedback loop*. A designer redrawing a logo doesn't get it right in one shot either; they draw, hold it up next to the original, squint, adjust, hold it up again. Claude had no equivalent of "hold it up next to the original and squint" — no way to overlay its attempt on the source and *see* the diff, only my typed descriptions of the diff, which are a much lossier channel than a pair of eyes on two overlapping images.

## So I had it build the eyes instead

If the bottleneck was "no visual feedback loop," the fix wasn't to keep iterating blind. It was to build the feedback loop and hand it to something that actually has eyes: me.

I asked Claude to build an interactive tool instead of another guess at the final SVG. The result is a self-contained HTML page: the original reference image sits underneath, a live SVG rendering of the logo sits on top (petals as plain, simple ellipses — nothing fancy, six params each), and every shape parameter — every radius, distance, rotation, color — is wired to a slider. An opacity control blends the two layers, and a "difference" mode lights up any pixel where they don't match, so misalignment is impossible to miss.

![The editor: original underneath, generated logo on top, sliders for every parameter](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/05-interactive-editor/editor_opacity50.png)

I dragged sliders until the two flowers sat on top of each other convincingly, then hit "copy parameters" and pasted the resulting JSON back to Claude. It baked those exact numbers into a clean final SVG.

![Final result next to the original, built from the hand-tuned parameters](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/06-final-from-tuned-params/compare.png)

That worked — on the first try, because the "trying" had already happened, visually, in the editor, before any code was written.

One bug even survived into that final version, which felt like a fitting last laugh: the two leaves at the bottom were quietly rendering *underneath* the petals, clipping off their tips wherever they overlapped. Small thing, easy fix once spotted (just a matter of paint order in the SVG) — but it's one more example of the same root issue. It's the kind of thing that's instantly obvious to a human eye and invisible to a model reasoning about shapes symbolically instead of looking at the picture it just produced.

![Leaf tip silently clipped by the petal on top of it, versus the fixed version with the leaf intact](https://raw.githubusercontent.com/bogdanripa/logo-gen-test/main/process/07-leaf-zorder-fix/before_bug.png)

## The takeaway

None of this means Claude is bad at graphics work — it wrote every line of the SVG, the whole editor, the analysis scripts I used to measure the source image, and it did all of that correctly and fast. What it can't do is a task that fundamentally requires *seeing your own output next to a target and measuring the gap*, over and over, until it closes. That's not a knowledge problem or a prompting problem. It's a missing sense.

The fix wasn't a cleverer prompt. It was recognizing which half of the task the model was actually good at (generating working code, structuring a tool, wiring up sliders and live SVG rendering) and which half it wasn't (eyeballing curves against a reference), and building a small piece of software whose entire job was to hand the second half back to a human.

You can try the editor yourself here: **[bogdanripa.github.io/logo-gen-test/editor.html](https://bogdanripa.github.io/logo-gen-test/editor.html)**

The full repo, including every failed attempt above, is at **[github.com/bogdanripa/logo-gen-test](https://github.com/bogdanripa/logo-gen-test)**.
