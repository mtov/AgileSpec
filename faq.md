<p align="center">
  <img src="logo.png" alt="AgileSpec logo" width="640">
</p>

# An Agile-Inspired Workflow for AI-Assisted Software Delivery

## Frequently Asked Questions

[Back to README](README.md)

**1. Does AgileSpec define events such as sprints, reviews, and
retrospectives?**

AgileSpec focuses on lightweight specifications and a workflow for agile
development with AI coding agents. Events such as sprints, reviews, and
retrospectives remain relevant but fall outside its scope. Teams are
free to continue using these practices alongside AgileSpec.

**2. What about roles (e.g., Product Owner and Scrum Master) and
artifacts (e.g., product backlog)?**

AgileSpec does not prescribe specific roles or a complete set of agile
artifacts. It recommends `backlog.md` for story summaries, priorities,
and status. Teams can retain their existing roles and practices.

**3. Can I add specifications beyond those proposed by AgileSpec?**

Absolutely. In keeping with agile principles, AgileSpec is flexible by
design. Teams can extend, adapt, or simplify its specifications and
workflow to suit their project's needs.


**4. Why doesn't AgileSpec require a task list or an agent execution
plan?**

AgileSpec assumes that coding agents can organize their own work within
an approved specification. Developers define the expected behavior and
constraints, including architecture, stored data, and interface layout.
Agents choose the steps needed to implement and test each story, while
`definition-of-done.md` sets shared completion criteria, such as passing
tests, human validation, and approved consolidation.

**5. What is the difference between project specs and agent configuration
files, such as `AGENTS.md`?**

Agent configuration files provide instructions that are included in the context
of each prompt sent to an LLM. They should therefore contain information
that the LLM should always be aware of.

In contrast, project specs contain more detailed information about the system
under development and do not need to be included in every prompt.
For example, suppose you are asking an agent to change the position of an
element on a web page. In this case, information about architecture or
database schema is unlikely to be relevant.

Thus, agent configuration files provide general instructions that apply
throughout development, while project specs provide information that
agents can consult as needed.
