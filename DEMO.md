# Demo Cheat Sheet — Dagger à l'échelle · DevoxxFR 2026

> Live coding cheat sheet. Each step builds on the previous one.
> Run all commands from the **repo root**.

---

## Setup

```bash
mise install       # installs java 25 + dagger 0.20.3
mise tasks         # verify ci:test task is listed
```

---

## Step 1 — Run the basic test

```bash
dagger --progress dots -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

Point out: first run is slow — Gradle downloads everything on every run. No cache.

---

## Step 2 — Add Gradle cache volumes

> **Concept**: Dagger layer cache (automatic, immutable) vs mounted cache volumes (mutable, named, persisted).
> Key trap: cache must be mounted **before** the source directory.

Uncomment the cache section in `_gradle()` in `dagger-kotlin/src/dagger_kotlin/main.py`.

Then pass `--build-cache` and `--project-cache-dir` directly on the `gradlew` commands:

```python
.with_exec(["./gradlew", "test", "--build-cache", "--project-cache-dir", "/app/build-cache"])
```

Re-run to show cache hit on second run:

```bash
dagger --progress dots -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

---

## Step 3 — Survive test failures + Dagger Shell

> **Concept**: Right now a test failure crashes the pipeline — the report is never exported.
> `ReturnType.ANY` lets the pipeline continue even when tests fail
> so we always get the JUnit XML. We return a `TestResult` object that exposes
> both `result()` (the report directory) and `exit_code()` (for the CI gate).
> Then, instead of two separate `dagger call` connections, Dagger Shell does both in one.

**Uncomment the failing test** in `kotlin-app/src/test/kotlin/com/example/FailingTest.kt`
to show what a failure looks like.

Show that the pipeline crashes — no report exported:

```bash
rm -rf ./build/test-results && dagger --progress dots -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

Comment the current test method, and uncomment the other one to switch to `TestResult`

Now we need two things: export the report **and** propagate the exit code.
Doing this with two separate `dagger call` invocations means two engine connections:

```bash
# Connection 1 — export reports
dagger --progress dots -m dagger-kotlin call test --source ./kotlin-app result export --path ./build/test-results

# Connection 2 — get exit code
dagger --progress dots -m dagger-kotlin call test --source ./kotlin-app exit-code
```

Dagger Shell solves this in a single session:

```bash
rm -rf ./build/test-results && dagger --progress dots -m ./dagger-kotlin --command '
  test_results=$( . | test --source=../kotlin-app )
  $test_results | result | export --path=./build/test-results
  .exit $( $test_results | exit-code )
'
```

Key points to explain:
- `$( . | test … )` — runs the test function, stores the lazy `TestResult` handle
- `$test_results | result | export` — pulls the report directory out, even on failure
- `.exit` — Dagger Shell builtin that sets the process exit code **after** the export

---

## Step 4 — Wrap in a mise task

> **Concept**: The Dagger command is powerful but verbose.
> `mise` acts as the developer-facing interface — nobody needs to know Dagger internals.
> The same command works locally and in GitHub Actions unchanged.

Run it:

```bash
mise run kotlin:ci:test

ls build/test-results/
```

---

## Quick reference

| Goal | Command |
|---|---|
| Run tests + export report | `dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results` |
| Run tests + report + exit code (after step 4) | `mise run ci:test` |
| Build install dir | `dagger -m dagger-kotlin call build --source ./kotlin-app export --path ./dist` |
| Build Docker image | `dagger -m dagger-kotlin call build-docker --source ./kotlin-app` |
| Inspect functions | `dagger -m dagger-kotlin functions` |
| List mise tasks | `mise tasks` |
