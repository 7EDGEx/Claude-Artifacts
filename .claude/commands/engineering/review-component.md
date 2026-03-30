Review the frontend component: $ARGUMENTS

1. **Locate the component** from $ARGUMENTS.
   It could be a file path or a component name. If a path, read it directly. If a name, search for it in the codebase.
   If the component cannot be found, ask the user to provide the full file path.

2. **Analyse the component** and produce a structured review covering:

   **Accessibility (a11y)**
   - Missing ARIA attributes, labels, or roles
   - Keyboard navigation gaps
   - Focus management issues
   - Screen reader compatibility

   **Performance**
   - Unnecessary re-renders (missing memoization, unstable references in deps)
   - Heavy imports that could be lazy-loaded
   - Missing loading / error / empty states
   - Unoptimized list rendering (missing keys, no virtualization for large lists)

   **Code Quality**
   - Props that should be typed more strictly
   - State that could be derived instead of stored
   - Effects with missing or incorrect dependency arrays
   - Logic that should be extracted into a custom hook
   - Hardcoded strings that should be constants or i18n keys

3. **Output the review** in this format:

   ```
   COMPONENT REVIEW: <component name>
   ===================================
   Critical (blocks merge):   [list — must fix before merge]
   Warning (should fix):      [list — fix before or soon after merge]
   Suggestion (nice-to-have): [list — non-blocking improvements]
   Verdict: PASS / NEEDS WORK
   ```

4. **Provide corrected code** for any Critical or Warning items.
   Show only the changed sections as diffs, not the entire file.

5. **Flag anything unclear**:
   ```
   QUESTIONS FOR THE DEVELOPER:
   ============================
   - [ ] <question 1>
   - [ ] <question 2>
   ```
