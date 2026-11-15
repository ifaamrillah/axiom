---
name: project-documentation
description: >
  Create or update concise engineering documentation from verified project
  evidence. Use when onboarding knowledge, implementation behavior, or
  operational guidance needs to be recorded.
---

# Project Documentation

## Purpose

Turn verified engineering knowledge into maintainable, discoverable Markdown.

## When to use / avoid

Use when a change alters setup, behavior, architecture, APIs, operations, or durable project knowledge. Avoid duplicating code comments, temporary task notes, or existing documentation that remains accurate.

## Inputs and preconditions

Target audience, relevant source/docs, project conventions, and status of existing documentation.

## Procedure

1. Identify the source of truth and audience.
2. Check for existing content and decide whether to update, link, or add a focused section.
3. Draft concise content with prerequisites, steps, expected result, and caveats as relevant.
4. Cite paths or commands for technical details; label assumptions and version-sensitive guidance.
5. Check links and consistency with the implementation.

## Tools

Use Markdown and repository conventions; no documentation service is required.

## Outputs and gates

A focused document or update. Gate: no unsupported claims, links resolve, and the content can be followed by its intended reader.

## Failure handling

If behavior is unclear, record the unknown or verify with an appropriate safe check; do not fill gaps with guesses.

## References

See [document contract](../../../core/contracts/DOCUMENT-CONTRACT.md) and [documentation standard](../../../core/standards/documentation.md).
