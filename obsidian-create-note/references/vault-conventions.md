# Vault Conventions

## Paths

- Vault root: `/home/tharg/Documents/my_notes`
- New notes (this skill's target): `/home/tharg/Documents/my_notes/all_notes`
- Tag files: `/home/tharg/Documents/my_notes/tags`. Each tag is a Markdown file named `<tag>.md`. Many tag files are empty stubs; their purpose is to be the wiki-link target for `[[<tag>]]` references inside notes.
- Daily journals: `/home/tharg/Documents/my_notes/daily` — separate workflow, do not use this skill there.
- Ephemeral scratch: `/home/tharg/Documents/my_notes/ephemeral` — separate workflow.
- Literature notes: `/home/tharg/Documents/my_notes/Literature` — separate workflow.
- Templates: `/home/tharg/Documents/my_notes/templates`.
- Indexes (currently empty): `/home/tharg/Documents/my_notes/indexes`.

## Git

The vault is a git repository. The `obsidian-git` plugin auto-commits every 10 minutes with messages shaped `vault backup: YYYY-MM-DD HH:mm:ss` and auto-pushes on the same interval. Do NOT run `git` commands from this skill — let the plugin own the commit history.

## Tag casing

Filenames in `tags/` preserve case. The corpus mixes lowercase topic tags (`python`, `airflow`, `linux`) with uppercase acronyms (`AI`, `ML`, `AIS`, `3NF`). When reusing an existing tag, match the existing filename exactly. When creating a new tag, follow the convention: lowercase for general topics, preserved case for acronyms or proper nouns.

## Note body shape

A typical note looks like:

```md
---
created: 2026-05-23
modified: 2026-05-23
tags:
---
2026-05-23 14:11
Status:
Tags: [[python]] [[snippet]]

## Section Heading

Content here.
```

- The YAML `tags:` field stays empty. The cross-link mechanism is the body `Tags: [[…]]` line that wiki-links into `tags/*.md`.
- `created:` and `modified:` are managed by the `front-matter-timestamps` plugin. `scripts/create-note` pre-fills both with today's date so the file is not blank; the plugin keeps `modified:` current on subsequent edits.
- The `Status:` line is for the user to fill in later.

## Useful commands

```bash
python3 scripts/list-tags                          # enumerate existing tag names
python3 scripts/create-note \                      # create a new note in all_notes/
  --source /path/to/source.md \
  --title "My Title" \
  --tags python snippet
```
