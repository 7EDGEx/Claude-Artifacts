---
name: debug-init
description: Initialize debugging for a project — generates a repo-specific debug.md that teaches you your codebase structure through systematic debugging
allowed-tools: [Read, Glob, Bash, Grep]
---

# Debug System Initialization

## Purpose

Generate a **project-specific debugging guide** (`.claude/commands/debug.md`) that helps you:
1. Debug systematically using the 7-phase framework
2. Learn your project's structure, file organization, and data flow
3. Build a mental model of the codebase for better future prompts to AI

This command analyzes YOUR project and creates a guide tailored to it.

---

## What This Command Does

1. **Identifies your project stack**
   - Reads `package.json`, `tsconfig.json`, `Dockerfile`, config files
   - Determines: frontend/backend, frameworks, database, testing setup

2. **Maps your architecture**
   - Scans folder structure: `src/`, `tests/`, `api/`, etc.
   - Identifies entry points: main files, API routes, event handlers
   - Finds patterns: middleware, services, repositories, components

3. **Learns your patterns**
   - Finds common file paths and naming conventions
   - Identifies typical error patterns in YOUR codebase
   - Locates test setup and mock patterns

4. **Generates `.claude/commands/debug.md`**
   - A project-specific debugging guide
   - Contains YOUR file paths, entry points, and patterns
   - Will be used by `/debug` command for all future debugging
   - Becomes your **mental model reference** for the project

---

## When to Run This

**First time** setting up debugging in a project:
```bash
cd your-project-repo
/debug-init
```

**Run again** if:
- Major refactoring changes the folder structure
- Significant architecture changes (new layers, services, patterns)
- You're starting fresh in an established project

---

## How to Run

### Option 1: As a Slash Command (Recommended)
```bash
/debug-init
```
The command will guide you through the initialization interactively.

### Option 2: Manual (Advanced)
If slash command integration isn't available, you can manually run the initialization steps:

1. **Analyze your project structure:**
   ```bash
   # Read project config
   cat package.json tsconfig.json
   
   # List main folders
   find . -maxdepth 2 -type d | grep -E "^\./(src|api|services|tests)" | sort
   
   # Find entry points
   find . -name "index.ts" -o -name "main.ts" -o -name "server.ts" | head -10
   ```

2. **Understand your architecture:**
   ```bash
   # List main files
   ls -la src/ src/*/
   
   # Find typical patterns
   grep -r "export class\|export function" src/ | head -20
   grep -r "async.*function\|Promise" src/ | wc -l
   ```

3. **Review common paths:**
   ```bash
   # Database files
   find . -name "*repository*" -o -name "*model*" -o -name "*schema*" | grep -v node_modules
   
   # Test patterns
   find . -name "*.test.ts" -o -name "*.spec.ts" | head -5
   ```

4. **Create `.claude/commands/debug.md`:**
   - Use the information gathered above
   - Follow the template in the next section
   - Replace `[YOUR_...]` placeholders with actual paths from your project

---

## Output: Project-Specific `debug.md`

After running `/debug-init`, you'll have a new file: `.claude/commands/debug.md`

This file will contain:

### Section 1: Project Overview
```
Project Type: [Backend API / Frontend / Full-stack / Library]
Framework: [Node.js + Express / Django / React / etc.]
Language: [TypeScript / JavaScript / Python]
Database: [PostgreSQL / MongoDB / etc.]
Testing: [Jest / Mocha / Pytest / etc.]
```

### Section 2: Folder Structure Map
```
src/
├── controllers/      ← API request handlers
├── services/        ← Business logic
├── repositories/    ← Database queries
├── models/          ← Data structures
├── middleware/      ← Request processing
└── utils/           ← Helper functions
```

### Section 3: Common File Paths
```
Main entry: src/index.ts
API routes: src/api/routes.ts
Database: src/models/, src/repositories/
Tests: tests/, __tests__/
Config: .env.example, config.ts
```

### Section 4: Data Flow
```
API Request
  ↓ (middleware)
Controller (validate input)
  ↓
Service (business logic)
  ↓
Repository (database query)
  ↓
Database
  ↓
Response
```

### Section 5: 7-Phase Debugging Guide
The generated file includes the full 7-phase framework customized for YOUR project:
- **Phase 1:** Define the problem
- **Phase 2:** Trace through YOUR project's layers
- **Phase 3:** Add logs at YOUR specific decision points
- **Phase 4:** Execute and compare
- **Phase 5:** Analyze (with common failure patterns from YOUR codebase)
- **Phase 6:** Design the fix
- **Phase 7:** Verify

### Section 6: Common Patterns & Issues
Based on your project type, includes:
- **Error patterns:** Common errors in YOUR stack
- **Testing patterns:** How to test in YOUR setup
- **Database patterns:** Query patterns, migration issues
- **Performance patterns:** N+1 queries, bottlenecks

---

## Using the Generated File

After `.claude/commands/debug.md` is created, use it with the `/debug` command:

```bash
# When you hit a bug
/debug The POST /users endpoint returns 500 instead of 201
```

The `/debug` command will:
1. Use the project-specific context from `.claude/commands/debug.md`
2. Guide you through the 7 phases with YOUR file paths
3. Help you trace, log, and understand YOUR specific codebase
4. Build your mental model of the project structure

---

## What You Learn by Using Debug Sessions

Each time you run `/debug`, you're learning about your codebase:

```
Debug Session 1: Bug in API endpoint
  Learn: Controller → Service → Repository flow
  Learn: Where validation happens
  Learn: How database queries work
  
Debug Session 2: Test failure
  Learn: Test setup and mocks
  Learn: Async/await patterns
  Learn: Data preparation
  
Debug Session 3: Performance issue
  Learn: Which operations are slow
  Learn: Query patterns
  Learn: Caching opportunities
  
After 5-10 sessions:
  ✓ You know the entire codebase structure
  ✓ You understand data flow end-to-end
  ✓ You know common problem patterns
  ✓ You can ask Claude specific, contextual questions
```

---

## Mental Model Building

The debug process builds your mental model systematically:

### What You Learn
- **Folder structure:** Where each concern lives (controllers, services, db)
- **Data flow:** How a request travels through the codebase
- **Common patterns:** How similar problems are solved in YOUR project
- **Failure points:** Where things usually break (validation, queries, async)
- **Dependencies:** How services, modules, and layers connect

### How It Helps Future Prompts
```
Before mental model:
"How do I add a feature?"
→ Vague, AI needs to ask many clarifying questions

After mental model (from debug sessions):
"I need to add email validation to user creation.
 In src/services/UserService, the create() method handles the API data,
 but I need to validate the email format before it goes to the repository.
 Where should I add this? Domain layer or service layer?"
→ Precise, AI can give direct answer
```

---

## FAQ

**Q: Do I need to add debug-init.md to my global Claude config?**
A: Yes. Copy `debug-init.md` to `~/.claude/commands/` so `/debug-init` works in any project.

**Q: How often should I run `/debug-init`?**
A: Once per project, unless your architecture changes significantly.

**Q: What if I'm joining an existing project that already has `.claude/commands/debug.md`?**
A: Use it directly! Run `/debug` when you hit issues. The existing file is your project's mental model reference.

**Q: How does this help me prompt AI better?**
A: By understanding your codebase structure through debug sessions, you can ask Claude specific questions about YOUR code, not generic questions about the framework.

**Q: Can I edit the generated `debug.md`?**
A: Yes. Feel free to update it as you learn more about the project or if the structure changes.

---

## Next Steps

1. Run `/debug-init` in your project
2. Review the generated `.claude/commands/debug.md`
3. The next time you hit a bug, run `/debug <issue context>`
4. Follow the 7-phase framework and build your mental model
5. Use your learned mental model to ask Claude better questions in the future

---

## Reference

- **Foundation:** Debugging framework from `/home/user/.claude/CLAUDE.md` (Section 11)
- **Purpose:** Build mental models while debugging systematically
- **Outcome:** Better codebase understanding + efficient AI prompting
