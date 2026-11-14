<p align="center">
  <img src="logo.png" alt="AgileSpec logo" width="640">
</p>

# An Agile Workflow for AI-Native Development

## Table of Contents

- [Motivation](#motivation)
- [Specifications](#specifications)
- [Project Specs](#project-specs)
- [User Story Specs](#user-story-specs)
- [Folder Structure](#folder-structure)
- [Workflow](#workflow)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Example: PodLite](#example-podlite)

## Motivation

Agile methods emerged when developers performed most software
development tasks themselves, from requirements and design to coding and
testing. Today, AI agents can take on much of this work, significantly
accelerating implementation.

This shift calls for new workflows that help developers define
lightweight specifications, guide AI coding agents during
implementation, and verify that the resulting software meets its
requirements while remaining consistent with project-wide decisions.

To address this need, we propose **AgileSpec**, a workflow for
developing software with AI coding agents that emphasizes lightweight,
living specifications.

## Specifications

AgileSpec organizes specifications into two main levels:

- **Project Specs** describe the system as a whole. They guide
  developers and AI agents in maintaining the system's conceptual
  integrity, ensuring that development remains aligned with its
  requirements and architectural decisions.

- **User Story Specs** capture requirements and decisions specific to
  individual stories. They guide AI agents in implementing each story
  while ensuring consistency with the project's global specifications.

```mermaid
flowchart LR
    A["AgileSpec"]
    A --> P["Project Specs"]
    A --> S["User Story Specs"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef level fill:#f1f5f9,stroke:#94a3b8,color:#0f172a

    class A root
    class P,S level
```

AI agents can help maintain, and synchronize these documents with the
codebase. However, developers remain responsible for reviewing and
approving their content, ensuring that the documentation accurately
reflects the system and its intended evolution.

```mermaid
flowchart LR
    A["AI Agents"]
    H["Developers"]

    subgraph S["AgileSpecs"]
        direction TB
        C(["Create"])
        U(["Update"])
        R(["Review"])
        P(["Approve"])
        RR(["Read"])
    end

    H --- C
    H --- R
    H --- P
    A --- RR
    A --- U
    
```

## Project Specs

AgileSpec starts with a set of documents that provide a shared
understanding of the project. These documents serve as global project
documentation, guiding development decisions and providing context for
AI coding agents. They should remain accessible and up to date
throughout development.

At this level, we recommend three Markdown files:

- **`architecture.md`**: A high-level description of the system's
  architecture, including its main modules, their responsibilities, and
  architectural constraints. For example, UI components must access the
  database through a service layer rather than directly. This document
  should also describe the project's main technology choices, including
  programming languages, frameworks, and databases, preferably in a
  dedicated section.

- **`database.md`**: Describes the database schema, including tables,
  their columns and data types, primary and foreign keys, relationships
  between tables, and integrity constraints.

- **`ui.md`**: Describes the overall user interface structure,
  navigation, and shared design conventions. For example, it may specify
  that the application uses a sidebar for navigation, consistent button
  labels, and a common layout for displaying items.

```mermaid
flowchart LR
    P["Project Specs"]

    P --> A["architecture.md"]
    P --> D["database.md"]
    P --> U["ui.md"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef doc fill:#f1f5f9,stroke:#94a3b8,color:#0f172a

    class P root
    class B,A,D,U doc
```

Although these documents provide project-wide guidance, **they do not
need to be complete before implementation begins**. Requiring detailed
specifications upfront would contradict agile principles and risk
introducing Big Design Up Front (BDUF), an approach in which detailed
design decisions are made before development starts.

Instead, AgileSpec treats project documentation as a set of **living
documents** that evolve alongside the software. They are progressively
refined and extended as user stories are implemented.

## User Story Specs

As in traditional agile methods, AgileSpec organizes development around
individual user stories. A Product Owner or Product Manager selects a
story from the backlog and assigns it to a developer for implementation.

```mermaid
flowchart LR
    A["Backlog"] --> B["Selected Story"] --> C["Agile Specs"]
````

Next, the developer prepares four Markdown files to guide the
story's implementation:

- **`acceptance.md`**: Defines the story's acceptance criteria,
  organized into **Normal Case** and **Edge Cases**. The former
  describes expected behavior under typical conditions, while the latter
  covers exceptional situations, invalid inputs, and boundary
  conditions.

- **`design.md`**: Describes story-specific implementation decisions,
  including classes, functions, modules, API endpoints, algorithms,
  and data structures.

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
    S --> C["views.md"]
    S --> D["tables.md"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef doc fill:#f1f5f9,stroke:#94a3b8,color:#0f172a

    class S root
    class A,B,C,D doc
```

As with project-level documentation, these files can be drafted with the
assistance of AI agents. However, they must be reviewed and approved by
the developer responsible for implementing the story.

Even after a user story has been implemented, its directory and associated
files should remain in the project repository. They serve as documentation
for the story and can be particularly useful when future maintenance is
required, such as fixing a bug or adapting to changes in business rules.

## Folder Structure

We recommend storing the proposed specifications in a directory named
`AgileSpec/` at the root of the project.

```text
AgileSpec/
  project/
    architecture.md
    ui.md
    database.md
  stories/
    storyN/
      acceptance.md
      design.md
      views.md
      tables.md
```

## Workflow

AgileSpec follows an iterative workflow consisting of five main
activities:

- Inception
- Story-Level Activities
  - Specification
  - Implementation 
  - Review and Verification
- Consolidation

The first activity establishes the project's initial context. The
next three activities are repeated for each user story, allowing
the system and its specifications to evolve incrementally. The last
activity consolidates the decisions made during story implementation
into the project's global specifications, keeping them consistent
with the evolving implementation.

```mermaid
flowchart TD
    A["Inception"]
    B["Specification"]
    C["Implementation"]
    D["Review and Verification"]
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
create the project specs, defining key architectural, database, and
UI decisions.

### Specification

For each selected user story, the developer prepares its specifications
in four files: `acceptance.md`, `design.md`, `views.md`, and `tables.md`.

The goal is to provide enough detail for an AI coding agent to implement
the story without introducing unnecessary documentation.

### Implementation

Once the specs are approved, an AI coding agent implements the story using
both the story-specific documents and the global project context.

The developer can initiate implementation with a prompt such as:

```text
Implement story N using the approved specifications in
AgileSpec/stories/storyN/:
- acceptance.md
- design.md
- views.md (if present)
- tables.md (if present)

Read AgileSpec/project/ for project-wide context and constraints.

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

Do not update project-level documentation.
```

For convenience, this prompt is saved in the repository's
[`prompts/implementation.md`](prompts/implementation.md) file.
You can use it as follows:

```text
Follow prompts/implementation.md to implement story [n] in
[project name].
```

### Review and Verification

After implementation, the developer reviews the changes and verifies
that the story satisfies its acceptance criteria.

Verification may involve inspecting the generated code, running
automated tests, and manually interacting with the application.
Particular attention should be given to the Normal Case and Edge Cases
documented in `acceptance.md`, as well as compliance with the approved
design and, where present, `views.md` and `tables.md`.

If problems are found, the developer provides feedback to the AI agent,
which revises the implementation. This cycle continues until the story
is approved. If implementation reveals missing or incorrect
specifications, the corresponding story specs should also be
updated.

```mermaid
flowchart TD
    A["Review and Verification"] --> B{"Approved?"}
    B -->|Yes| C["Consolidation"]
    B -->|No| D["Revise Specs / Reimplement"]
    D --> A
```

### Consolidation

Once the story has been implemented and approved, its relevant design
decisions and changes must be incorporated into the project specs.

This activity, called **Consolidation**, ensures that the global
specifications remain consistent with the implemented system, using the
correspondence between the two levels:

- **`design.md` to `architecture.md`**: Incorporate relevant
  architectural decisions.
- **`views.md` to `ui.md`**: Incorporate relevant global UI structure
  and conventions.
- **`tables.md` to `database.md`**: Incorporate database schema changes.

```mermaid
flowchart LR
    subgraph S["User Story Specs"]
        direction TB
        S1["design.md"]
        S2["views.md"]
        S3["tables.md"]
    end

    subgraph P["Project Specs"]
        direction TB
        P1["architecture.md"]
        P2["ui.md"]
        P3["database.md"]
    end

    S1 --> P1
    S2 --> P2
    S3 --> P3

    classDef story fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef project fill:#dcfce7,stroke:#16a34a,color:#166534

    class S1,S2,S3 story
    class P1,P2,P3 project
```

Consolidation can be performed with the assistance of an AI agent using
a prompt such as:

```text
Consolidate the completed implementation of story N into the
project-level documentation.

Read:
- AgileSpec/stories/storyN/
- AgileSpec/project/
- The relevant implemented source code

Use the following correspondence, skipping absent optional files:
- design.md to architecture.md: incorporate architectural decisions
- views.md to ui.md: incorporate global UI structure and conventions
- tables.md to database.md: incorporate schema changes

Incorporate relevant decisions and changes, keeping the documentation
concise, accurate, and consistent with the implemented code.

Preserve the distinction between project-wide documentation and
story-specific implementation details. Do not copy entire story
specifications into project-level documents.

Do not modify the source code or story-level specifications.

Summarize the documentation changes for developer review.
```

The developer reviews and approves the resulting documentation changes.

Consolidation completes the development cycle for a story. The next
story can then be selected from the backlog, using the updated
project-level documentation as context.


## Frequently Asked Questions

**1. Does AgileSpec define events such as sprints, reviews, and
retrospectives?**

AgileSpec focuses on lightweight specifications and a workflow for agile
development with AI coding agents. Events such as sprints, reviews, and
retrospectives remain relevant but fall outside its scope. Teams are
free to continue using these practices alongside AgileSpec.

**2. What about roles (e.g., Product Owner and Scrum Master) and
artifacts (e.g., product backlog)?**

Similarly, AgileSpec does not prescribe specific roles or a complete set
of agile artifacts. Teams can retain their existing roles and practices.
Some artifacts, such as the product backlog, are already used by
AgileSpec.

**3. Can I add specifications beyond those proposed by AgileSpec?**

Absolutely. In keeping with agile principles, AgileSpec is flexible by
design. Teams can extend, adapt, or simplify its specifications and
workflow to suit their project's needs.

## Example: PodLite

See [PodLite](examples/podlite/README.md) for the podcast-player example
and its setup instructions.
