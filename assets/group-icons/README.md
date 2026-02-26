# Group Icons

Reusable SVG icons for skill groups.

## Files

- `seo.svg`
- `ads.svg`
- `blog.svg`
- `devops.svg`
- `fullstack.svg`
- `database.svg`
- `kotlin.svg`
- `swift.svg`
- `typescript.svg`
- `code.svg`
- `vue.svg`
- `react.svg`
- `prompt.svg`
- `test.svg`
- `feature.svg`
- `axiom.svg`

The icon-name mapping is in `icons.json`.

## Suggested usage in `agents/openai.yaml`

```yaml
interface:
  icon_small: "./assets/group-icons/<group>.svg"
  icon_large: "./assets/group-icons/<group>.svg"
```

For production use, copy the icon into each skill's local `assets/` folder and set relative paths from that skill.

## Source and License

Icons are from OpenMoji (color SVG set):

- Source: https://github.com/hfg-gmuend/openmoji/tree/master/color/svg
- License: CC BY-SA 4.0 (https://github.com/hfg-gmuend/openmoji/blob/master/LICENSE.txt)
