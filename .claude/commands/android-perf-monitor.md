---
name: android-perf-monitor
description: Monitor React Native Android app performance via ADB during development — JS thread, bridge, memory, renders — then run React Compiler ESLint hook, fix violations, and auto-optimize
---

# React Native Android Performance Monitor

You are a performance engineering assistant for React Native development. Use ADB, Metro logs, and RN-specific tooling to collect real-time performance data, identify bottlenecks in the JS thread, bridge calls, and renders, then suggest concrete optimizations for time and space complexity.

If `$ARGUMENTS` is provided, use it as the package name. Otherwise ask:
> "What is your app's package name? (e.g. com.myapp)"

**Rule:** Collect data first. Never guess at the root cause. Always show evidence before recommending a fix.

---

## Phase 1: Device Setup

```bash
# Verify device connected
adb devices

# Get device info
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release

# Confirm app is running
adb shell pidof $PACKAGE
```

Enable React Native performance overlay on device:
```bash
# Open RN dev menu (shake or via ADB)
adb shell input keyevent 82
```
Then enable: **Show Perf Monitor** — this shows JS FPS, UI FPS, RAM live on screen.

Take a baseline screenshot:
```bash
adb shell screencap -p /sdcard/rn_baseline.png && adb pull /sdcard/rn_baseline.png ./rn_baseline.png
```

---

## Phase 2: Collect Metrics

### 2.1 JS Thread & UI Thread FPS (via Perf Monitor)

Enable via dev menu → "Show Perf Monitor" then take screenshot:
```bash
adb shell screencap -p /sdcard/rn_perf.png && adb pull /sdcard/rn_perf.png ./rn_perf.png
```

Read the screenshot — report:
- **JS FPS** (target: 60) — drops indicate heavy JS work
- **UI FPS** (target: 60) — drops indicate native render issues
- **RAM** — current MB usage

### 2.2 Frame Rendering (Native Layer Jank)

```bash
adb shell dumpsys gfxinfo $PACKAGE reset
# Interact with app for 10-15 seconds
adb shell dumpsys gfxinfo $PACKAGE
```

Key values:
- **Janky frames %** — target < 5%
- **Slow UI thread** — native thread blocked
- **50/90/95/99th percentile frame time** — target all < 16ms

### 2.3 Memory

```bash
adb shell dumpsys meminfo $PACKAGE
```

RN-specific areas to watch:
- **Java Heap** — Android/React Native runtime
- **Native Heap** — Hermes JS engine heap, C++ bridge
- **TOTAL Pss** — total real device footprint

### 2.4 JS Heap (Hermes Engine)

If using Hermes (default in RN 0.70+):
```bash
# Check Hermes is enabled
adb shell dumpsys package $PACKAGE | grep hermes
```

For JS heap profiling, use Chrome DevTools:
```bash
# Forward Hermes debugger port
adb forward tcp:8081 tcp:8081
```
Then open `chrome://inspect` → inspect app → Memory tab → take heap snapshot.

### 2.5 Bridge / JSI Calls (Log-based)

```bash
adb logcat -c
# Reproduce the slow interaction, then:
adb logcat -d | grep -E "ReactNative|JS_THREAD|BRIDGE|RCTBridge|hermes" | tail -50
```

### 2.6 Metro Bundler / JS Logs

```bash
# Watch Metro output for warnings/errors
adb logcat | grep -E "console\.|ReactNativeJS|RCTLog"
```

### 2.7 Startup Time

```bash
adb shell am force-stop $PACKAGE
adb shell am start -W $PACKAGE/.MainActivity
```

RN startup breakdown:
- Native app init → JS bundle load → JS execution → first render
- Target: < 2000ms TotalTime

### 2.8 Re-render Detection

Add this temporarily to your components during dev (instruct user if not already present):
```js
// In dev builds only
if (__DEV__) {
  const { unstable_enableWhyDidYouRenderUpdates } = require('@welldone-software/why-did-you-render');
  unstable_enableWhyDidYouRenderUpdates(React);
}
```

Then check Metro/logcat output for unnecessary re-render warnings.

### 2.9 Crash / ANR Check

```bash
adb logcat -d | grep -E "FATAL|AndroidRuntime|ANR|ReactNativeFatalException|RedBox" | tail -20
```

---

## Phase 3: Analyze Metrics

### JS FPS Targets

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| JS FPS | 60 | 45–59 | < 45 |
| UI FPS | 60 | 45–59 | < 45 |

**JS FPS low, UI FPS fine** → problem is in JavaScript (logic, state updates, re-renders)
**Both FPS low** → native layer issue or bridge overflow
**UI FPS low, JS fine** → overdraw, expensive native views, layout thrashing

### Memory Targets (React Native)

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| TOTAL Pss | < 200MB | 200–400MB | > 400MB |
| Native Heap | < 100MB | 100–200MB | > 200MB |

### Startup Targets

| Metric | Target | Poor |
|--------|--------|------|
| Cold TotalTime | < 2000ms | > 3000ms |
| JS bundle load | < 500ms | > 1500ms |

### Jank Targets

| Metric | Healthy | Problem |
|--------|---------|---------|
| Janky frames | < 5% | > 5% |
| 99th percentile | < 32ms | > 32ms |

---

## Phase 4: Diagnose Root Cause

### A. Too Many Re-renders (Most Common RN Issue)
Symptoms: JS FPS drops on state changes, Metro shows re-render warnings.

Diagnose — ask user to share the component code where slowness is felt, then check:
- Is `useState` / `useReducer` updating too broadly?
- Are objects/arrays being recreated on every render as props?
- Is `useEffect` missing deps or has too many deps causing cascades?

### B. Expensive JS on Main Thread
Symptoms: JS FPS drops during specific operations (list scroll, search, filter).

Diagnose:
```bash
adb logcat | grep -i "JS_THREAD\|slow"
```
- Heavy computations running synchronously in event handlers or render functions
- Sorting/filtering large arrays on every keystroke

### C. Bridge Saturation (Old Architecture)
Symptoms: UI feels delayed after JS updates, both FPS drop together.

Diagnose — look for:
- Sending large objects over the bridge (images as base64, huge JSON)
- Calling native modules in tight loops
- Serialization overhead in `ScrollView` / `FlatList` with complex items

### D. FlatList / ScrollView Performance
Symptoms: Scroll jank, memory growth while scrolling.

Diagnose:
```bash
adb shell dumpsys meminfo $PACKAGE | grep -E "Java Heap|TOTAL"
# Take memory before and after scrolling long list
```

### E. Memory Leak
Symptoms: RAM grows session-over-session, app slows down after extended use.

Diagnose — look for:
- `useEffect` with subscriptions/timers not cleaned up in return function
- Event listeners added but never removed
- Large objects cached in module scope

### F. Slow Bundle / Startup
Symptoms: High `TotalTime` on cold start.

Diagnose:
```bash
adb logcat | grep -E "ReactNative|loadJSBundleFromFile|runJSBundle"
```

---

## Phase 5: Optimization Recommendations

Based on diagnosis, provide specific, prioritized fixes. Reference the actual code if user shares files.

### Re-render Optimizations (Space/Time Complexity)

```js
// ❌ New object on every render → child always re-renders
<Child style={{ flex: 1 }} onPress={() => doSomething()} />

// ✅ Stable references
const style = useMemo(() => ({ flex: 1 }), []);
const handlePress = useCallback(() => doSomething(), []);
<Child style={style} onPress={handlePress} />
```

```js
// ❌ Filtering/sorting in render — O(n) on every render
const filtered = data.filter(x => x.active);

// ✅ Memoize — only recalculate when data changes
const filtered = useMemo(() => data.filter(x => x.active), [data]);
```

Wrap expensive components:
```js
export default React.memo(MyComponent); // Skip re-render if props unchanged
```

### FlatList Optimizations

```js
// ✅ Always provide these
<FlatList
  data={items}
  keyExtractor={(item) => item.id.toString()} // stable, not index
  getItemLayout={(_, index) => ({            // skip dynamic measurement
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index
  })}
  removeClippedSubviews={true}               // unmount off-screen items
  maxToRenderPerBatch={10}                   // reduce initial render batch
  windowSize={5}                             // render 5 screens worth
  initialNumToRender={10}
/>
```

### Moving Heavy Work Off JS Thread

```js
// ❌ Heavy computation blocking JS thread
const result = heavySort(largeArray); // freezes UI

// ✅ Use InteractionManager to defer until after animations
InteractionManager.runAfterInteractions(() => {
  const result = heavySort(largeArray);
  setResult(result);
});

// ✅ Or use a worker (react-native-workers / worklets via Reanimated)
```

### Reducing Bridge Calls (Old Architecture)

```js
// ❌ Calling native module in a loop
items.forEach(item => NativeModule.process(item));

// ✅ Batch into single call
NativeModule.processBatch(items);
```

### Startup Optimization

- Use `react-native-bundle-splitter` or Hermes bytecode (`*.hbc`) for faster bundle load
- Defer non-critical screens with `React.lazy()` + `Suspense`
- Move `App.tsx` initializers behind `InteractionManager.runAfterInteractions`
- Reduce top-level module imports — each `import` at module root runs at startup

### Memory Leak Prevention

```js
// ❌ Timer never cleared
useEffect(() => {
  const id = setInterval(tick, 1000);
}, []); // leak

// ✅ Clean up
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id); // cleaned up on unmount
}, []);
```

---

## Phase 5b: React Compiler Check (Run After Every Feature)

After finishing a feature or before committing, always run the React Compiler ESLint hook to catch violations and verify the compiler can auto-optimize the code.

### Step 1: Verify React Compiler ESLint Plugin is Set Up

Check if already installed:
```bash
cat package.json | grep -E "eslint-plugin-react-compiler|babel-plugin-react-compiler"
```

If not installed:
```bash
# Install ESLint plugin
npm install --save-dev eslint-plugin-react-compiler

# Install Babel plugin (for compile-time optimization)
npm install --save-dev babel-plugin-react-compiler
```

Add to `eslint.config.js` (or `.eslintrc`):
```js
// eslint.config.js
import reactCompiler from 'eslint-plugin-react-compiler';

export default [
  {
    plugins: { 'react-compiler': reactCompiler },
    rules: {
      'react-compiler/react-compiler': 'error',
    },
  },
];
```

### Step 2: Run ESLint on Changed Files

```bash
# Run on entire project
npx eslint . --ext .js,.jsx,.ts,.tsx

# Or just on recently changed files
git diff --name-only | grep -E '\.(js|jsx|ts|tsx)$' | xargs npx eslint
```

### Step 3: Interpret Compiler Violations

The `react-compiler/react-compiler` rule fires when the compiler **cannot safely auto-memoize** a component or hook. Each violation means:
- The compiler will skip optimizing that component
- You must fix the violation OR manually add `useMemo`/`useCallback`/`React.memo`

**Common violations and fixes:**

| Violation | Meaning | Fix |
|-----------|---------|-----|
| Mutating props or state directly | Breaks React's immutability contract | Use spread / `setState` properly |
| Reading ref during render | Refs are mutable, unsafe to memoize | Move ref reads to effects/handlers |
| Calling hooks conditionally | Violates Rules of Hooks | Move hook to top level |
| Side effects in render | Render must be pure | Move to `useEffect` |
| Accessing `arguments` object | Not safe to analyze statically | Use named params |
| Using non-stable external values | Compiler can't track mutations | Wrap in `useMemo` with explicit deps |

### Step 4: Enable React Compiler in Babel (Auto-Optimize)

Add to `babel.config.js`:
```js
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'annotation', // Start with annotation mode — only compiles components you opt in
      // compilationMode: 'infer',   // When ready — compiles all components automatically
    }],
  ],
};
```

**Annotation mode** — opt specific components in with a directive:
```js
function MyComponent({ items }) {
  'use memo'; // tells compiler: optimize this component
  const filtered = items.filter(x => x.active); // compiler auto-memoizes this
  return <List data={filtered} />;
}
```

**Infer mode** — compiler auto-optimizes everything it can safely analyze. Switch to this once ESLint shows zero violations.

### Step 5: Verify Compiler Is Working

After enabling, check Metro output on app start — you should NOT see manual `useMemo`/`useCallback` warnings if compiler is handling it.

Confirm compiled output in Metro:
```bash
adb logcat | grep -i "react-compiler\|compiled"
```

Check that the compiler removed redundant manual memoization you wrote — it will optimize those away automatically.

### Step 6: Optimize Code Based on ESLint Output

For every violation the ESLint plugin reports, fix it so the compiler can take over. The goal is:

```
❌ Manual useMemo/useCallback everywhere (you maintain deps arrays)
✅ Zero ESLint violations → compiler auto-memoizes → no manual deps to maintain
```

If a component **cannot** be made compiler-compatible (e.g., uses a third-party lib that mutates), add:
```js
'use no memo'; // explicitly opts out — compiler skips this component
```

---

## Phase 6: Screenshot & Interaction During Dev

### Capture current screen state
```bash
adb shell screencap -p /sdcard/s.png && adb pull /sdcard/s.png ./s.png
```

### Tap a UI element (get coords from ui dump)
```bash
adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml ./ui.xml
# Find element in ui.xml → get bounds → tap center
adb shell input tap $X $Y
```

### Reload JS bundle (without restart)
```bash
adb shell input keyevent 82  # Dev menu → Reload
# Or:
adb shell input text "rr"    # If fast refresh keyboard shortcut works
```

### Check what screen is currently shown
```bash
adb shell dumpsys activity | grep "mCurrentFocus"
```

---

## Phase 7: Output Report

```
## React Native Performance Report
**Device:** {model} Android {version}
**Package:** {package}

### Live Metrics
| Metric         | Value    | Target   | Status      |
|----------------|----------|----------|-------------|
| JS FPS         | {val}    | 60       | ✅ / ⚠️ / ❌ |
| UI FPS         | {val}    | 60       | ✅ / ⚠️ / ❌ |
| RAM (Pss)      | {val}MB  | < 200MB  | ✅ / ⚠️ / ❌ |
| Janky frames   | {val}%   | < 5%     | ✅ / ⚠️ / ❌ |
| Cold start     | {val}ms  | < 2000ms | ✅ / ⚠️ / ❌ |

### Root Cause
{Evidence-based diagnosis — which thread, which component, which operation}

### Optimizations (Priority Order)
1. **[HIGH]** {Fix} — reduces {metric} by ~{X}
   - Complexity before: O(n) per render
   - Complexity after: O(1) with memoization
2. ...

### Next Steps
{Specific files / components to look at}
```
