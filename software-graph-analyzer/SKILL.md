---
name: software-graph-analyzer
description: >
  Use Ontoly to build and query a deterministic Software Graph for architecture, route, service, dependency, configuration, and impact-analysis questions before falling back to source search.
---

# Software Graph Analyzer

Use this skill when a repository question should be answered from graph evidence rather than repeated grep, broad file reads, or speculative architecture summaries.

## Trigger

Invoke for requests such as:

- "explain this repository"
- "trace this route"
- "what depends on this service?"
- "what breaks if this module changes?"
- "where is this environment variable used?"
- "show the package/module/service graph"
- "build or inspect an Ontoly Software Graph"

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Repository root | Yes | Current workspace or explicit path |
| User question | Yes | Architecture, route, dependency, configuration, or impact question |
| Existing Ontoly graph | No | Usually `.ontoly/SoftwareGraph.json` |
| Scope hint | No | Node name, package, route, file path, framework, or relationship type |

## Process

1. Find the repository root and check whether an Ontoly graph already exists.
2. If the graph is missing or stale, run `npx ontoly build .` from the repository root.
3. Inspect graph metadata, diagnostics, statistics, graph hash, framework detection, trust, and coverage before relying on results.
4. Use Ontoly CLI or MCP capabilities before reading source files directly.
5. Narrow the query to graph concepts: packages, modules, routes, controllers, services, functions, configuration, environment variables, dependencies, callers, callees, and related nodes.
6. For impact questions, traverse dependency, consumer, caller, callee, import, export, and containment relationships in the graph.
7. For request-flow questions, trace from route to handler/controller/service/repository/database or downstream dependency when those nodes exist.
8. Cite the graph evidence that supports the answer.
9. Use source inspection only when graph coverage is missing, ambiguous, or contradicted by diagnostics; label it as fallback evidence.

## Outputs

Return this structure:

```markdown
## Answer
{Direct answer.}

## Graph Evidence
| Kind | Evidence |
|------|----------|
| Node | `{node id}` ({node kind}) |
| Edge | `{source} --RELATIONSHIP--> {target}` |
| Location | `{file}:{line}` |
| Diagnostic | `{code}: {message}` |

## Confidence
{High, Medium, or Low} because {specific graph coverage and diagnostics}.

## Gaps
{Missing graph concepts, unresolved imports, ambiguity, or source fallback used.}
```

## Constraints

- Do not answer architecture, dependency, route, or impact questions from source search until Ontoly graph evidence has been checked.
- Do not guess confidence; derive it from graph evidence, diagnostics, coverage, and ambiguity.
- Do not hide graph gaps. Report missing nodes, relationships, framework coverage, or diagnostics as findings.
- Do not modify the target repository unless the user explicitly asks for implementation work.
- Keep the answer scoped to the question; avoid dumping the full graph.

## Useful Commands

```bash
npx ontoly build .
npx ontoly mcp
npx ontoly --help
```
