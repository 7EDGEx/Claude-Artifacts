
<!-- Created by Pooja Shetty -->
Generate detailed documentation for the feature: $ARGUMENTS

Follow these steps:

1. **Locate the feature** — Search the codebase for files, functions, classes, and modules related to "$ARGUMENTS". Use Glob and Grep to find all relevant code.

2. **Understand the implementation** — Read the relevant source files to understand:
   - What the feature does and its purpose
   - How it works internally (key functions, data flow, algorithms)
   - Entry points and public API surface
   - Dependencies and integrations with other parts of the system

3. **Generate documentation** with these sections:

   ## Overview
   A concise description of the feature and its purpose.

   ## Usage
   How to use the feature — code examples, API calls, or UI interactions.

   ## How It Works
   Internal mechanics: key components, data flow, and important implementation details.

   ## API Reference
   Public functions, classes, methods, or endpoints — with parameters, return types, and descriptions.

   ## Configuration
   Any configuration options, environment variables, or settings that affect the feature.

   ## Dependencies
   External libraries or internal modules this feature relies on.

   ## Edge Cases & Limitations
   Known constraints, gotchas, or behaviors to be aware of.

Do not invent details. Base all documentation solely on what you find in the code. If the feature cannot be found, say so clearly.
