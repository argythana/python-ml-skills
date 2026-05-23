---
name: obsidian-create-note
description: >
  Use when the user wants to import a local Markdown file as a new note
  in the Obsidian vault at `/home/tharg/Documents/my_notes/` — prompts
  like "import this .md into Obsidian", "add this Markdown doc to my
  vault", "create a note from this file", or "save this Markdown to my
  notes". If the source Markdown path is missing, ask for it before
  proceeding — missing input is not a routing failure. Do NOT use for:
  editing, renaming, moving, or deleting existing notes; vault-wide
  search; daily notes (`daily/`); Literature notes (`Literature/`);
  ephemeral scratch (`ephemeral/`); Excalidraw drawings; fetching
  content from a URL (use `url-reader` first); generating note content
  from scratch (this skill imports an existing `.md` file, not authors
  one from a topic prompt). Do NOT run `git` commands — the
  `obsidian-git` plugin owns commits. This skill is hard-wired to one
  user's vault layout; do NOT use against other Obsidian vaults.
---

# Obsidian create note

## Overview

Create a note in the `my_notes` Obsidian vault from a source Markdown file. Keep title and tag judgment calls in the agent loop; use the helper scripts for the deterministic filesystem operations.

## Routing boundary

Use this skill when:

- the user wants to import a local Markdown file into `/home/tharg/Documents/my_notes/all_notes/` as a new note
- the task includes title choice or refinement and tag selection as part of note creation

If the request fits but the source Markdown path is missing, ask for it before proceeding (missing input is not a routing failure).

Do NOT use for: editing, renaming, moving, or deleting existing notes; vault-wide search; daily notes (`daily/` is its own workflow); Literature notes (`Literature/` is its own workflow); ephemeral scratch (`ephemeral/` is its own workflow); Excalidraw drawings; general Obsidian Markdown formatting questions; fetching content from a URL (route to `url-reader` first — this skill only imports an existing local `.md` file, and there is no automatic handoff because `url-reader` returns content in the conversation, not a file on disk); generating note content from scratch from a topic prompt (this skill imports an existing local `.md` file, it does not author one).

Do NOT run `git` commands. The `obsidian-git` plugin auto-commits and pushes the vault on a 10-minute interval; manual commits will conflict with the plugin's backup history.

This skill is hard-wired to one user's vault layout (`/home/tharg/Documents/my_notes/`). Do NOT use against other Obsidian vaults; fork the skill and adapt the paths in `scripts/` and `references/vault-conventions.md` first.

## Workflow

1. Confirm the user provided a Markdown file path. Read the file before making title or tag decisions.
2. Read [references/vault-conventions.md](references/vault-conventions.md) for canonical paths, body shape, and plugin notes.
3. List the current tag inventory with `python3 scripts/list-tags`. Reuse existing tags exactly, including case — the corpus mixes `AI`, `airflow`, `3NF`.
4. Determine the title:
   - Prefer YAML frontmatter `title:` when present in the source.
   - Otherwise use the highest-level heading.
   - If no clear title exists, generate a concise retrieval-friendly title from the content.
   - If the existing title is weak or misleading, keep it by default but tell the user and suggest a better alternative before creating the note.
   - The title becomes the filename verbatim — spaces preserved, only filesystem-illegal characters stripped.
5. Choose tags:
   - Prefer 2-6 strong tags.
   - Reuse the existing tag vocabulary whenever it fits; match the existing filename case exactly.
   - Create a new tag file only when no existing tag fits.
   - Deduplicate tags and stay below 10.
6. If you create a new tag, write `/home/tharg/Documents/my_notes/tags/<tag>.md` as a separate step with the same frontmatter shape as existing tag files (YAML `created:`/`modified:` set to today's date, blank body). `scripts/create-note` does not create tag files for you.
7. Create the note:

   - If the source begins with its own YAML frontmatter (a leading `---` block), strip it before passing to `create-note`. Read the frontmatter for title/tag hints first if useful, then write a sanitized copy to a temp file (e.g. `/tmp/<title>.md`) and pass that as `--source`. Two `---` blocks back to back produce malformed Markdown that breaks Obsidian's frontmatter parser.
   - Run:

     ```bash
     python3 scripts/create-note \
       --source /path/to/source.md \
       --title "My Title" \
       --tags python snippet
     ```

   - Use `--render-title` only when you generated the title yourself (the source had no usable title).
   - The script writes to `all_notes/`. Do not pass `--notes-dir`; the other vault subdirectories (`daily/`, `Literature/`, `ephemeral/`, etc.) have their own workflows and are out of scope for this skill.
8. Report the created note path, the tags you applied, any new tag files you created, and any alternative title you suggested.

## Title judgment

Prefer titles that are specific, searchable, and stable over time. Avoid filler like `notes`, raw export filenames, or dates unless the content genuinely requires them.

Keep the existing title when it is already representative, even if you can imagine a slightly better one. Only raise an alternative when the current title would materially hurt retrieval or mislead a future reader.

## Tag judgment

Prefer concrete topic tags over vague workflow labels — prefer `python`, `linux`, `airflow`, `aisdb`, `security` over generic buckets like `misc` or `notes`.

Treat the local tag list as the default vocabulary. When you must create a new tag, keep it short, noun-like, and consistent with the existing corpus: lowercase for general topics, preserved case for acronyms or proper nouns (`AI`, `ML`, `AIS`, `3NF`).

If the source Markdown contains code snippets, include `snippet` plus a tag for each relevant programming language (e.g. `python`).

## Resources

- `scripts/list-tags`: list current tag names from `/home/tharg/Documents/my_notes/tags`
- `scripts/create-note`: write the note to `all_notes/`, preserve the human-readable title as the filename, deduplicate tags, render the YAML frontmatter (`created`, `modified`, empty `tags`) + body timestamp + `Status:` line + `Tags: [[…]]` wiki-link line, then append the source Markdown
- `references/vault-conventions.md`: canonical vault paths, body shape, plugin behavior, and the tag-creation procedure
