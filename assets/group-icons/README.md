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
- `typescript.svg`
- `code.svg`
- `vue.svg`
- `react.svg`
- `prompt.svg`
- `test.svg`

The icon-name mapping is in `icons.json`.

## Suggested usage in `agents/openai.yaml`

```yaml
interface:
  icon_small: "./assets/group-icons/<group>.svg"
  icon_large: "./assets/group-icons/<group>.svg"
```

For production use, copy the icon into each skill's local `assets/` folder and set relative paths from that skill.

## Source and License

Icons are from Lucide:

- Source: https://github.com/lucide-icons/lucide/tree/main/icons
- License: ISC (https://github.com/lucide-icons/lucide/blob/main/LICENSE)
