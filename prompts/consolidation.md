# Consolidation

Consolidate the implemented and validated story N in [project directory]
into its project-level documentation.

Read, relative to that directory:
- AgileSpec/stories/storyN/
- AgileSpec/project/
- The relevant implemented source code

Use the following correspondence, skipping absent optional files:
- acceptance.md to backlog.md: adjust the story summary if needed
- design.md to architecture.md: incorporate architectural decisions
- views.md to ui.md: incorporate global UI decisions and conventions
  to preserve across future stories, even when already reflected in
  existing screens or components; avoid screen-specific descriptions
  and duplicated implementation details
- tables.md to database.md: incorporate global persistence decisions
  and conventions to preserve across future stories, even when already
  reflected in models, schemas, or migrations; avoid reproducing table
  definitions and implementation details

Consolidation is required even when no project specs need updating.
Preserve only decisions useful for future stories, summarizing and
combining them with existing guidance. Keep story-specific details
in their original specifications.

Do not modify the source code or story-level specifications.
If the specifications and code disagree, report the discrepancy before
consolidating.

Summarize the changes and any pending completion criteria for review.
Leave the story unchecked in backlog.md until the developer approves
consolidation and all completion criteria are met.
