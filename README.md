**Note:** AgileSpec is currently a preliminary proposal and is subject
to further refinement and evolution.

<p align="center">
  <img src="logo.png" alt="AgileSpec logo" width="640">
</p>

# An Agile Workflow for AI-Assisted Software Delivery

[Frequently Asked Questions](faq.md) |
[PodLite Example](examples/podlite/README.md)

## Table of Contents

- [Motivation](#motivation)
- [Who Is AgileSpec For?](#who-is-agilespec-for)
- [Specifications](#specifications)
- [Project Specs](#project-specs)
- [User Story Specs](#user-story-specs)
- [Folder Structure](#folder-structure)
- [AgileSpec Workflow](#agilespec-workflow)
- [Summary and Key Principles](#summary-and-key-principles)
- [Example: PodLite](#example-podlite)
- [Frequently Asked Questions](#frequently-asked-questions)
- [License](#license)

## Motivation

*Agile specifications over vibe coding.*

Agile methods, such as Scrum and XP, emerged when developers performed
most software development tasks themselves, from requirements and design
to coding and testing. Today, AI agents can take on much of this work,
significantly accelerating implementation. This shift calls for new
workflows that help developers define lightweight specifications, guide
AI coding agents during implementation, and verify that the resulting
software meets its requirements while remaining consistent with
project-wide decisions.

```mermaid
flowchart LR
    A["Agile Methods<br/>(Scrum, XP, etc.)"] --> B["AgileSpec"]
    B --> C["Maintainable<br/>Code"]
    D["AI Agents"] <--> B
```

To address this need, we propose **AgileSpec**, an agile workflow for
developing software with AI coding agents that emphasizes lightweight,
living specifications.

## Who Is AgileSpec For?

Teams and organizations that want to adopt an AI-first approach to
software development while preserving lightweight specifications and
traceability, keeping comprehension debt under control, and ensuring
that the software remains understandable and maintainable.

## Specifications

AgileSpec organizes specifications into two main levels:

- **Project Specs** describe the system as a whole. They guide
  developers and AI agents in maintaining the system's conceptual
  integrity, ensuring that development remains aligned with its
  requirements and architectural decisions.

- **User Story Specs** capture requirements and decisions specific to
  individual stories. They guide AI agents in implementing each story
  while ensuring consistency with the project specs.

The two specification levels are connected through a **Specification
Alignment Loop**: project specs guide the specification and
implementation of individual stories, while relevant story-level
decisions are consolidated back into the project specs. This continuous
feedback loop keeps both levels aligned as the system evolves.

```mermaid
---
title: Specification Alignment Loop
---
flowchart TB
    P["Project Specs"] -->|"Guide"| S["User Story Specs"]
    S -->|"Consolidate"| P
```

AI agents can help maintain and synchronize these documents with the
codebase. However, developers remain responsible for reviewing and
approving their content, ensuring that the documentation accurately
reflects the system and its intended evolution.

```mermaid
flowchart LR
    H["Developers"] --> R["Review & Approve Specs"]
    A["AI Agents"] --> C["Guided by Specs"]
```

## Project Specs

Using AgileSpec begins with creating a set of documents that provide a
shared understanding of the project. These documents serve as global
project documentation, guiding development decisions and providing
context for AI coding agents. They should remain accessible and up to
date throughout development.

At the Project Specs level, there are five main Markdown documents:

- **`backlog.md`**: Lists user stories in priority order, with a brief
  description and status for each.

- **`definition-of-done.md`**: Defines shared completion criteria for
  all stories, such as passing tests, human validation, and consolidated
  project specs.

- **`architecture.md`**: A high-level description of the system's
  architecture, including its main modules, their responsibilities, and
  architectural constraints. For example, a project may require services
  to access the database through repositories. This document
  should also describe the project's main technology choices, including
  programming languages, frameworks, and databases, preferably in a
  dedicated section.

- **`database.md`**: Describes the database schema, including tables,
  their columns and data types, primary and foreign keys, relationships
  between tables, and integrity constraints. This document is optional
  for systems that do not use a database.

- **`ui.md`**: Describes the overall user interface structure,
  navigation, and shared design conventions. For example, it may define
  colors, typography, reusable components, and common layouts.
  This document is optional for systems without user-facing
  interactions, such as internal backend services.

```mermaid
flowchart LR
    P["Project Specs"]
    P --> B["backlog.md"]
    P --> F["definition-of-done.md"]
    P --> A["architecture.md"]
    P --> D["database.md<br/>(optional)"]
    P --> U["ui.md<br/>(optional)"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef doc fill:#f1f5f9,stroke:#94a3b8,color:#0f172a

    class P root
    class B,A,D,U,F doc
```

**Why project specs are important.** These documents provide shared
guidelines for AI agents, helping ensure that new
implementations follow established architectural decisions, preserve the
consistency and quality of the data model, and maintain a standardized
and usable interface. They also establish common completion criteria,
helping ensure that all deliverables meet minimum quality standards.
Together, they help preserve the system's **conceptual integrity** and
prevent its gradual degradation as the software evolves.

**Avoiding Big Design Up Front (BDUF).** Although project specs
provide global guidance, they do not need to be complete
before implementation begins. Requiring detailed specifications
upfront would contradict agile principles and lead to Big Design
Up Front (BDUF), an approach in which detailed design decisions
are made before development starts. Instead, AgileSpec treats project
documentation as a set of **living documents** that evolve alongside
the software. They are progressively refined and consolidated as user
stories are implemented.

## User Story Specs

As in traditional agile methods, AgileSpec organizes development around
individual user stories. The team selects a story from `backlog.md` for
implementation.

The developer prepares `acceptance.md` and `design.md`, adding
`views.md` and `tables.md` when needed. These user story specifications
guide the story's implementation:

- **`acceptance.md`**: Defines the story's acceptance criteria,
  organized into **Normal Case** and **Edge Cases**. The former
  describes expected behavior under typical conditions, while the latter
  covers exceptional situations, invalid inputs, and boundary
  conditions.

- **`design.md`**: Describes story-specific implementation decisions,
  such as classes and functions to be created, API endpoints to be
  implemented, libraries to be used, and interactions with external
  services.

- **`views.md`**: Describes story-specific screens, layouts, UI
  components, navigation, and interactions. This file is optional when
  the story does not involve UI changes.

- **`tables.md`**: Describes story-specific database changes, including
  tables, columns, relationships, and constraints. This file is optional
  when the story does not involve database changes.

```mermaid
flowchart LR
    S["User Story Specs"]
    S --> A["acceptance.md"]
    S --> B["design.md"]
    S --> C["views.md<br/>(optional)"]
    S --> D["tables.md<br/>(optional)"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef doc fill:#f1f5f9,stroke:#94a3b8,color:#0f172a

    class S root
    class A,B,C,D doc
```

As with project specs, these files can be drafted with the assistance of
AI agents. However, they must be reviewed and approved by the developer
responsible for implementing the story.

## Folder Structure

AgileSpec specifications should be stored alongside the source code, in
an `AgileSpec/` directory at the root of the project. This makes them
easier for agents to access and allows them to be versioned together
with the code.

```text
my-project/
  AgileSpec/
    project/
      backlog.md
      definition-of-done.md
      architecture.md
      ui.md (optional)
      database.md (optional)
    stories/
      storyN/
        acceptance.md
        design.md
        views.md (optional)
        tables.md (optional)
  src/
  tests/
  other-folders/
```

Retain user story specifications in the repository while they remain
useful for maintenance and traceability. They document the story and
support **traceability between requirements, design decisions, and the
source code**, helping developers fix bugs or adapt to changes in
business rules. Specifications that no longer provide value can be
archived.

## AgileSpec Workflow

AgileSpec follows an iterative workflow consisting of five main
activities:

- Inception
- Story-Level Activities
  - Specification
  - Implementation
  - Review and Verification
- Consolidation

The first activity establishes the project's initial context. The next
three activities are repeated for each user story, allowing the system
and its specifications to evolve incrementally. The last activity
consolidates the decisions made during story implementation into the
project's global specifications, keeping them consistent with the
evolving implementation.

```mermaid
---
title: AgileSpec Workflow
---
flowchart TD
    A["Inception"]
    B["Specification"]
    C["Implementation"]
    D["Review and<br/>Verification"]
    E["Consolidation"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> B
```

### Inception

AgileSpec begins with an inception phase that establishes the project's
scope and initial technical direction. During this phase, developers
create an initial `backlog.md` with prioritized user stories and define
key architectural, database, and UI decisions in the other project
specs. They also create a `definition-of-done.md` to establish shared
completion criteria.

### Specification

The developer selects a story from `backlog.md` and prepares
`acceptance.md` and `design.md`, adding `views.md` and `tables.md` when
UI or database changes are involved.

The goal is to provide enough detail for an AI coding agent to implement
the story without introducing unnecessary documentation.

The developer can prepare the specifications with a prompt such as:

```text
Create the specifications for story N in [project directory].

Read AgileSpec/project/ and the selected story in backlog.md.

Create AgileSpec/stories/storyN/ with:
- acceptance.md: Normal Case and Edge Cases.
- design.md: implementation decisions.
- views.md: UI changes, if needed.
- tables.md: database changes, if needed.

Keep specifications concise and avoid duplication.
Ask for clarification if requirements or important decisions are unclear.

Do not implement the story. Submit the specifications for my review.
```

The specification prompt is available in
[`prompts/specification.md`](prompts/specification.md). To use it:

```text
Follow prompts/specification.md to specify story [n] in
[project directory].
```

### Implementation

Once the specs are approved, an AI coding agent implements the story
using both the project and story specs.

The developer can initiate implementation with a prompt such as:

```text
Implement story N using the approved specifications in
AgileSpec/stories/storyN/:
- acceptance.md
- design.md
- views.md (if present)
- tables.md (if present)

Read AgileSpec/project/ for project-wide context and constraints,
including the selected story in backlog.md and the shared criteria in
definition-of-done.md.

Follow the approved design, views, and table changes where applicable.
Preserve existing functionality and avoid unrelated changes. If
requirements conflict or important decisions are missing, ask for
clarification before proceeding.

Implement and run automated tests covering the Normal Case and Edge
Cases defined in acceptance.md.

When finished, summarize:
- The changes made
- The tests executed and their results
- Any limitations or unresolved issues
- Instructions for manually validating the story
- Any Definition of Done criteria still pending

Do not update project-level documentation or mark the story complete.
```

The implementation prompt is available in
[`prompts/implementation.md`](prompts/implementation.md). To use it:

```text
Follow prompts/implementation.md to implement story [n] in
[project directory].
```

### Review and Verification

After implementation, the developer reviews the changes against the
acceptance criteria in `acceptance.md` and the applicable Definition of
Done criteria. Consolidation remains pending until the next activity.

Verification may involve inspecting the generated code, running
automated tests, and manually interacting with the application.
Particular attention should be given to the Normal Case and Edge Cases
documented in `acceptance.md`, as well as compliance with the approved
design and, where present, `views.md` and `tables.md`.

If problems are found, the developer provides feedback to the AI agent,
which revises the implementation. This cycle continues until the story
is approved. If implementation reveals missing or incorrect
specifications, the corresponding story specs should also be updated.

```mermaid
---
title: Review and Verification Workflow
---
flowchart TD
    A["Review and<br/>Verification"] --> B{"Approved?"}
    B -->|Yes| C["Consolidation"]
    B -->|No| D["Revise Specs/<br/>Reimplement"]
    D --> A
```

### Consolidation

Project specs evolve incrementally as stories are developed. After each
story, **Consolidation** incorporates relevant decisions into the
project specs, ensuring that subsequent stories build on an up-to-date
description of the system.

During consolidation, the developer reviews the user story specs and
identifies which decisions will be useful when implementing future
stories. These decisions can be simplified, summarized, and combined
to keep the project specs concise and focused on the system as a whole.
Details that matter only to the current story remain in its own
specifications.

```mermaid
---
title: Consolidation Workflow
---
flowchart LR
    A["Project Specs"] --> B["Next Story"]
    B --> C["Consolidation"]
    C --> A
```

Consolidation updates project specs based on their corresponding user
story specs:

- **`acceptance.md` → `backlog.md`**: Update the story summary if
  needed. Mark it complete only after consolidation is approved and the
  Definition of Done is met.
- **`design.md` → `architecture.md`**: Incorporate relevant
  architectural decisions.
- **`views.md` → `ui.md`**: Incorporate relevant UI structure and
  conventions.
- **`tables.md` → `database.md`**: Incorporate database schema changes.

```mermaid
flowchart LR
    subgraph S["User Story Specs"]
        direction TB
        S0["acceptance.md"]
        S1["design.md"]
        S2["views.md<br/>(optional)"]
        S3["tables.md<br/>(optional)"]
    end

    subgraph P["Project Specs"]
        direction TB
        P0["backlog.md"]
        P1["architecture.md"]
        P2["ui.md"]
        P3["database.md"]
    end

    S0 --> P0
    S1 --> P1
    S2 --> P2
    S3 --> P3

    classDef story fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef project fill:#dcfce7,stroke:#16a34a,color:#166534

    class S0,S1,S2,S3 story
    class P0,P1,P2,P3 project
```

Consolidation completes the development cycle for a story. The next
story can then be selected from `backlog.md`, using the updated project
specs as context.

Consolidation can be performed with the assistance of an AI agent using
a prompt such as:

```text
Consolidate the implemented and validated story N in [project directory]
into its project-level documentation.

Read, relative to that directory:
- AgileSpec/stories/storyN/
- AgileSpec/project/
- The relevant implemented source code

Use the following correspondence, skipping absent optional files:
- acceptance.md to backlog.md: adjust the story summary if needed
- design.md to architecture.md: incorporate architectural decisions
- views.md to ui.md: incorporate global UI structure and conventions
- tables.md to database.md: incorporate schema changes

Incorporate relevant decisions and changes, keeping the documentation
concise, accurate, and consistent with the implemented code.

Summarize and combine decisions that will help guide future stories,
keeping story-specific details in their original specifications.
Do not copy entire story specifications into project-level documents.

Do not modify the source code or story-level specifications.
If the specifications and code disagree, report the discrepancy before
consolidating.

Summarize the changes and any pending completion criteria for review.
Leave the story unchecked in backlog.md until the developer approves
consolidation and all completion criteria are met.
```

The consolidation prompt is available in
[`prompts/consolidation.md`](prompts/consolidation.md). To use it:

```text
Follow prompts/consolidation.md to consolidate story [n] in
[project directory].
```

## Summary and Key Principles

AgileSpec follows a
[spec-anchored approach](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html):
specifications are created before implementation, retained alongside the
code, and continuously evolved to support maintenance and evolution.

Its distinguishing feature is the **Specification Alignment Loop**,
which ensures that project specs guide individual stories while
story-level decisions continuously refine and evolve project specs.

AgileSpec is also guided by the following principles and
characteristics:

1. **Focus on Software Delivery**: Assumes that product discovery has
   already produced a backlog of user stories ready for implementation.

2. **Adherence to Agile Principles**: Supports iterative and incremental
   design and implementation, avoiding Big Design Up Front (BDUF).

3. **Compatibility with Agile Events**: Remains compatible with events
   such as sprint planning, daily stand-ups, reviews, and retrospectives.

4. **Compatibility with Agile Roles**: Accommodates roles such as
   Product Owners, Product Managers, and Scrum Masters.

5. **Specification-to-Code Traceability**: Preserves and versions the
   specifications alongside AI-generated code, supporting traceability,
   maintenance, and evolution.

6. **Preservation of Conceptual Integrity**: Uses project-level
   specifications to maintain consistency in architecture, user
   interfaces, and database design.

7. **Autonomy of AI Coding Agents**: Allows agents to plan and implement
   solutions autonomously while adhering to project-level and
   story-level specifications.

8. **Tool Independence**: Does not depend on specific tools, IDEs, or AI
   coding agents, allowing teams to use their preferred development
   environments.


## Example: PodLite

See [PodLite](examples/podlite/README.md) for the podcast-player example
and its setup instructions.

<p align="center">
  <img src="examples/podlite/podlite-v1/screenshot1-v1.png"
       alt="PodLite: successful podcast subscription" width="480">
</p>

- [PodLite v0](examples/podlite/podlite-v0/README.md): inception.
- [PodLite v1](examples/podlite/podlite-v1/README.md): Story 1 (RSS
  subscriptions).
- [PodLite v1 Consolidated](examples/podlite/podlite-v1-consolidated/README.md):
  Story 1 consolidated and approved.
- [PodLite v2](examples/podlite/podlite-v2/README.md): Story 2 (episode
  browsing), consolidated and approved.
- [PodLite v3](examples/podlite/podlite-v3/README.md): Story 3 (audio
  playback), consolidated and approved.

## Frequently Asked Questions

See the [FAQ](faq.md) for answers to common questions about AgileSpec.

## License

This project is licensed under the [MIT License](LICENSE).
