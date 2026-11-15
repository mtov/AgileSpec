---
name: agilespec-consolidation
description: >-
  Consolidate a validated AgileSpec story into project specifications.
  Use when asked to consolidate an implemented and validated story.
---

# AgileSpec Consolidation

Identify the project directory and story number from the request or
conversation. Ask for clarification only if either is unclear.

Read the [original prompt](../../../prompts/consolidation.md).
Resolve this link relative to this skill directory, not the selected
project. Follow the prompt using the selected project as the base for
its `AgileSpec/project/` and `AgileSpec/stories/storyN/` paths.

If the original prompt is missing, report its path and stop. Keep the
workflow instructions in the prompt rather than duplicating them here.
