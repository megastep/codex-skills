# Nano Banana Prompting Guide

Use this reference when the task is blocked by weak prompts rather than by code or tooling.

It is a practical guide for this skill, informed by Google's current Gemini image generation and prompt design docs.

## Core pattern

Write prompts in this order when possible:

1. Subject
2. Action or transformation
3. Composition
4. Style
5. Lighting and color
6. Background or environment
7. Constraints

Template:

```text
Create [subject] [doing what / transformed how], framed as [composition], in [style], with [lighting/color], set against [background], while keeping [constraints].
```

Example:

```text
Create a ceramic mug product photo, framed as a centered three-quarter studio shot, in a clean ecommerce style, with soft diffused daylight and warm neutral tones, set against an off-white seamless background, while keeping the handle fully visible and avoiding props.
```

## Generation prompts

For text-to-image, be specific about:

- The main subject
- Camera distance or framing
- Intended use: ad, mockup, icon, poster, hero image
- Style: flat, photoreal, painterly, 3D, editorial, isometric
- Important exclusions

Good:

```text
Create a flat app icon of a yellow rubber duck, centered, with rounded geometry, subtle depth, and a clean white background. Avoid text, borders, and extra objects.
```

Weak:

```text
Make a duck icon
```

## Editing prompts

For image editing, make the instruction explicit about what must change and what must stay fixed.

Use this pattern:

```text
Keep [elements to preserve], but change [target changes]. Maintain [style or composition constraints].
```

Examples:

```text
Keep the existing sneaker shape and angle, but change the background to pale blue and add a soft floor shadow. Maintain a clean studio advertising look.
```

```text
Keep the icon silhouette and rounded corners, but replace the red fill with cobalt blue glass and add a brighter top-left highlight. Maintain the same centered composition.
```

## Multi-turn refinement

For follow-up turns in the same `--state-file` conversation:

- Refer to the prior image directly.
- Ask for one to three changes at a time.
- Re-state critical elements that must not drift.

Good follow-up:

```text
Keep the same icon design and proportions, but make the background darker navy and reduce the shadow softness.
```

Bad follow-up:

```text
Make it better
```

## Prompt dimensions to control

Choose only the dimensions that matter for the task:

- Subject: person, object, scene, product
- Composition: close-up, hero shot, centered icon, isometric, top-down
- Style: photoreal, flat vector, glossy 3D, watercolor, manga
- Material: ceramic, glass, chrome, matte plastic, paper
- Lighting: soft daylight, dramatic rim light, golden hour, studio softbox
- Color: muted neutrals, high-contrast neon, monochrome, brand palette
- Background: seamless white, textured paper, city street, gradient wash
- Output intent: ecommerce, poster, app icon, landing-page hero, infographic

## Anti-patterns

Avoid:

- Open-ended prompts when you need consistency
- Too many independent ideas in one prompt
- Editing prompts that do not state what must stay unchanged
- Follow-up turns that say only "more polished" or "different vibe"
- Relying on the model to infer framing, style, and output purpose

## Reusable prompt skeletons

Product shot:

```text
Create a premium product photo of [object], framed as [shot type], in [style], with [lighting], on [background], while keeping [must-have detail].
```

Icon generation:

```text
Create a [style] app icon of [subject], centered, with [material/look], using [palette], on [background]. Avoid text and extra objects.
```

Image edit:

```text
Keep [preserved elements], but change [specific edit]. Maintain [composition/style constraints].
```

Poster or illustration:

```text
Create a poster-style illustration of [subject/action], with [composition], in [art style], using [palette], with [background detail]. Avoid [unwanted elements].
```

## Sources

- https://ai.google.dev/gemini-api/docs/image-generation
- https://ai.google.dev/gemini-api/docs/prompting-intro/
- https://ai.google.dev/guide/prompt_best_practices
