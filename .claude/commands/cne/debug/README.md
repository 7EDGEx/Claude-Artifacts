# Debug System: Build Mental Models Through Structured Debugging

## Purpose

The Debug System helps you:
1. **Debug effectively** — find root causes systematically, not guessing
2. **Build mental models** — learn the project structure deeply as you debug
3. **Prompt AI efficiently** — with rich context about your codebase, you can ask Claude better questions

By combining debugging with learning, you gain both **immediate fixes** and **long-term codebase understanding**.

---

## The Complete Flow

```
Step 1: Add debug-init.md to Your Global Claude Root File
        Add content to: ~/.claude/CLAUDE.md (or equivalent global config)
        (One-time setup across all projects)
            ↓
Step 2: Run /debug-init in Your Project Repo
        Reads: package.json, folder structure, entry points, patterns
        Learns: How THIS project is organized
        Creates: .claude/commands/debug.md (project-specific context)
            ↓
Step 3: Run /debug <issue context> When You Hit a Bug
        Uses the project context created in Step 2
        Guides you through 7-phase debugging
        You learn: folder structure, data flow, why things work
            ↓
Step 4: Future Prompts to Claude Are Better
        You understand the mental model
        You can ask: "In src/services, how does X connect to Y?"
        You prompt with context, not guessing
```

---

## Why This Works

**Goal:** Build a **mental model** of your project's structure and flow.

### Without Debug System
```
"The API is broken"
→ Ask AI: "Why is my API broken?"
→ AI needs to ask questions (missing context)
→ Back and forth: "What file?" "What error?" "What's your folder structure?"
→ Slow, inefficient
```

### With Debug System
```
Step 1: Run /debug-init
        You learn: "src/domain/, src/application/, src/infrastructure/"
        You learn: "Middleware → Controller → UseCase → Repository → Database"
        
Step 2: Run /debug <issue>
        You trace the flow
        You see logs at each layer
        You understand WHERE it breaks and WHY
        
Step 3: Next time you need help
        Ask AI: "In src/application/useCase, the CreateUser method gets past validation
                 but fails at repository.save(). The error is 'unique constraint violation'.
                 How should I handle this?"
        AI understands your structure, gives precise answer
        No back-and-forth needed
```

---

## Three Steps to Get Started

### Step 1: Add `debug-init.md` Content to Global Claude Config (One-Time Setup)

Save the `debug-init.md` file to your global Claude configuration directory:

**Option A: Copy the file**
```bash
# Copy from this repo to your global Claude config
cp /path/to/Claude-Artifacts/.claude/commands/cne/debug/debug-init.md \
   ~/.claude/commands/debug-init.md
```

**Option B: Add to global CLAUDE.md**
Add the content from `debug-init.md` to your global `~/.claude/CLAUDE.md` as a section or custom command definition.

This makes `/debug-init` available to ANY project repo on your machine.

---

### Step 2: Run `/debug-init` in Your Project (Once Per Project)

When you start working on a new project repo:

```bash
cd your-project-repo
/debug-init
```

What this does:
- **Reads** your project: `package.json`, folder structure, entry points, services
- **Understands** your architecture: layers, file organization, patterns
- **Learns** common issues in YOUR specific codebase
- **Creates** `.claude/commands/debug.md` — a project-specific debugging guide
- **Outputs** folder structure and mental model reference

This creates a **project context file** that becomes your reference for all future debugging.

---

### Step 3: Run `/debug <issue context>` When You Hit a Bug

When something breaks:

```bash
/debug The POST /users endpoint returns 500 instead of creating a user
```

or

```bash
/debug The integration test for payment service is timing out
```

What this does:
1. **Phase 1 — Define:** Clarifies exactly what should happen vs what actually happens
2. **Phase 2 — Trace:** Maps the code flow through YOUR project structure (using context from Step 2)
3. **Phase 3 — Log:** Tells you where to add logs based on YOUR file paths
4. **Phase 4 — Execute:** Guides you to run and watch the logs
5. **Phase 5 — Analyze:** Helps you find where expected ≠ actual
6. **Phase 6 — Design:** Guides you to design ONE targeted fix
7. **Phase 7 — Verify:** Confirms the fix works

**As you go through these phases:**
- You learn the folder structure
- You understand data flow
- You see how different layers communicate
- You build a mental model of the codebase

---

## The Mental Model Benefit

### Before (Without Mental Model)
```
"I need to add a feature"
→ Search codebase randomly
→ "Where should this validation go? Domain? Application? Controller?"
→ Try one place, doesn't work
→ Try another place, partially works
→ Spend time on architecture questions instead of feature
```

### After (Built Through Debug Sessions)
```
"I need to add a feature"
→ I know: validation → Domain Entity (business rules)
→ I know: use case coordination → Application Layer
→ I know: API contract → Presentation/Controller
→ I know: data persistence → Infrastructure/Repository
→ I know where to put code, why, and how it connects
→ Feature built correctly first time
```

---

## How It Helps You Prompt AI Better

Once you have a mental model (from Steps 1-3), your prompts to Claude become **precise and contextual**:

### Before Mental Model
```
"The database query is slow. How do I fix it?"
→ AI: "What query? What's your schema? How many records? What index?"
→ Back-and-forth, slow
```

### After Mental Model (Built by Debug System)
```
"In src/infrastructure/repositories/OrderRepository.findByUserId(),
 the query returns 1,000 orders instead of just active ones.
 I traced it: the WHERE clause for status='active' is there,
 but logs show it's returning all statuses. The SQL looks right.
 Why isn't the filter working?"
 
→ AI: "The issue is likely [specific problem]. Check this line in your code.
        Try this fix. Here's why it works."
→ Direct, precise answer
```

---

## How Mental Models Improve Over Time

```
Debug Session 1: Fix API endpoint
  Learn: Middleware → Controller → UseCase → Repository structure
  Learn: Where validation happens
  Learn: How database queries execute

Debug Session 2: Fix test failure
  Learn: How mocks are structured
  Learn: Where async operations are
  Learn: Test data setup flow

Debug Session 3: Performance issue
  Learn: N+1 query patterns
  Learn: Which queries hit database
  Learn: Where caching helps

After 5-10 debug sessions:
  ✓ You know the entire codebase structure
  ✓ You know how data flows
  ✓ You know common problem patterns
  ✓ You can ask Claude precise questions
  ✓ Claude's answers are immediately useful
```

---

## File Structure

In this repository (Claude-Artifacts):

```
.claude/commands/cne/debug/
├── README.md              ← Overview & flow (this file)
├── debug-init.md          ← Copy to ~/.claude/commands/ or add to global config
└── debug.md               ← Generated per project (not in git)
```

**In YOUR project repo** (after running `/debug-init`):

```
your-project/
├── .claude/
│   └── commands/
│       └── debug.md       ← Project-specific debugging guide
│                          ← Created by /debug-init
│                          ← Contains YOUR file paths & patterns
└── (rest of your project)
```

---

## Quick Start Checklist

- [ ] **Step 1:** Copy `debug-init.md` to your global Claude configuration
- [ ] **Step 2:** Run `/debug-init` in your project repo
- [ ] **Step 3:** Review the generated `.claude/commands/debug.md` (your project's mental model reference)
- [ ] **Step 4:** Next time you hit a bug, run `/debug <issue context>`
- [ ] **Step 5:** Go through 7 phases, learn structure, build mental model
- [ ] **Step 6:** Next time you need help from Claude, use your new understanding to ask better questions

---

## Core Benefits

| Aspect | Without Debug System | With Debug System |
|--------|----------------------|-------------------|
| **Debugging Speed** | Try random fixes, slow | Systematic phases, 30 min |
| **Fix Quality** | Symptoms only | Root causes |
| **Codebase Understanding** | Partial, scattered | Complete mental model |
| **Future Prompts** | Vague, need back-and-forth | Precise, contextual |
| **Learning** | Minimal | Deep understanding |
| **Confidence** | Low ("Does this work?") | High ("I know why this works") |

---

## Key Principle

```
DEBUGGING = LEARNING
LEARNING = BETTER PROMPTS
BETTER PROMPTS = EFFICIENT AI USE
```

Every debug session you do teaches you more about your codebase.
That knowledge makes you a better collaborator with AI.

---

## Next Steps

1. **Copy/Add debug-init.md** to your global Claude config
2. **Run /debug-init** in your project
3. **Review** the generated debug.md (your project's mental model)
4. **Use /debug** the next time you hit a bug
5. **Build your mental model** through each debug session
6. **Prompt AI better** with your new understanding
