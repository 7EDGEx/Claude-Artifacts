<!-- Created by Swasthik Suvarna -->
Review the backend service or file: $ARGUMENTS

1. **Locate the target** from $ARGUMENTS.
   It could be a file path, folder, or service name. Read it directly.
   If not found, ask the user for the full path.

2. **Run static checks** (do not execute — analyse statically):

   **ESLint / Prettier / tsconfig**
   - Flag any code that violates common ESLint rules (unused vars, no-explicit-any, etc.)
   - Flag formatting issues that Prettier would catch (indentation, trailing commas, quotes)
   - Flag TypeScript issues: missing types, use of `any`, incorrect tsconfig paths

3. **DDD Pattern Compliance**
   - Verify separation: domain → application → infrastructure → interface
   - Flag any business logic leaking into handlers or infrastructure layer
   - Flag any direct DB calls from use-cases or domain entities
   - Flag missing repository interfaces (direct implementation usage instead of abstraction)
   - Flag circular dependencies between DDD layers

4. **Redundant Code**
   - Identify dead code, unused imports, duplicate logic
   - For each: either suggest removal or highlight with reason

5. **Performance**
   - Flag slow SQL patterns: missing WHERE clauses, SELECT *, N+1 queries, missing indexes
   - Flag unoptimised loops or repeated DB calls that could be batched

6. **Security (OWASP + GDPR)**
   - SQL injection risks (raw queries without parameterisation)
   - XSS risks — flag any user input reflected in responses without sanitisation
   - DDoS exposure — flag missing rate limiting, throttling, or API Gateway usage plans
   - Missing Zod schema validation on all incoming request bodies, params, and query strings
   - Hardcoded secrets or credentials — all config must be pulled from SSM, never from process.env directly
   - Overly permissive CORS or IAM policies in serverless.yml
   - PII exposure in logs, error messages, or API responses (GDPR violation)
   - Sensitive data returned in responses that should be omitted or masked

7. **Error Handling**
   - Flag any use of `console.log`, `console.error`, or raw `throw new Error('string')` — must use structured error classes
   - Verify a reusable typed base error class exists (e.g. `AppError` extending `Error` with `statusCode`, `code`, `message` fields) and is used consistently across all services
   - Flag any service defining its own ad-hoc error shape instead of extending the shared base error class
   - Verify errors are caught and returned as proper HTTP responses (4xx/5xx) with consistent error shape
   - Flag any unhandled promise rejections or missing try/catch blocks
   - Ensure error messages do not leak stack traces or internal details to the client

8. **Logging (Pino)**
   - Flag any `console.log` / `console.error` — must use Pino logger
   - Verify logs use structured JSON format with a correlation/request ID
   - Flag any log statements that include PII (names, emails, phone numbers, IDs that map to individuals) — GDPR violation
   - Verify log levels are appropriate (debug/info/warn/error)

9. **REST API Best Practices**
   - Correct HTTP methods used (GET/POST/PUT/PATCH/DELETE)
   - Correct HTTP status codes returned (201 for create, 204 for delete, 400 for validation, 404 for not found, etc.)
   - Consistent response envelope shape across endpoints
   - Pagination implemented for list endpoints
   - No verbs in endpoint paths (e.g. `/getUser` is wrong, `/users/{id}` is correct)

10. **Cost Optimisation (AWS)**
    - Flag Lambda functions with over-allocated memory or timeouts set higher than needed
    - Flag missing connection pooling — each Lambda must reuse DB connections (e.g. via `pg-pool`) not open a new one per invocation
    - Flag SSM `getParameter` calls inside the handler function — must be cached at Lambda init (outside the handler)
    - Flag missing API Gateway caching on GET endpoints that return stable data
    - Flag verbose Pino log levels (debug/trace) left on in production — increases CloudWatch cost
    - Flag any large payloads being passed between Lambda functions unnecessarily

11. **Mintlify Doc Comments**
    - Flag any exported function, class, or interface missing a JSDoc/Mintlify comment
    - Suggest the comment if missing

11. **OpenAPI / API Documentation**
    - If a new route or endpoint is found, check if `openapi.yaml` has a matching entry
    - If missing, generate the OpenAPI path entry for it

12. **Output the review** in this format:

    ```
    CODE REVIEW: <file or service name>
    =====================================
    Critical (must fix):   [list]
    Warning (should fix):  [list]
    Suggestion (optional): [list]
    Verdict: PASS / NEEDS WORK
    ```

13. **Provide fixes** for all Critical and Warning items.
    Show only the changed sections as diffs, not the entire file.

14. **Flag anything unclear**:
    ```
    QUESTIONS FOR THE DEVELOPER:
    ============================
    - [ ] <question>
    ```
