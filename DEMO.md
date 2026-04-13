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
dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

Point out: first run is slow — Gradle downloads everything on every run. No cache.

---

## Step 2 — Add Gradle cache volumes

> **Concept**: Dagger layer cache (automatic, immutable) vs mounted cache volumes (mutable, named, persisted).
> Key trap: cache must be mounted **before** the source directory.

Edit `_gradle()` in `dagger-kotlin/src/dagger_kotlin/main.py`:

```python
from dagger import CacheSharingMode

def _gradle(self, source: dagger.Directory) -> dagger.Container:
    return (
        dag.container()
        .from_(JDK_IMAGE)
        # ✅ Cache BEFORE source — this layer stays stable across commits
        .with_mounted_cache(
            "/root/.gradle",
            dag.cache_volume("gradle-cache"),
            sharing=CacheSharingMode.PRIVATE,  # isolated per pipeline
        )
        .with_mounted_cache(
            "/app/build-cache",
            dag.cache_volume("build-cache-kotlin-app"),
            sharing=CacheSharingMode.PRIVATE,
        )
        .with_workdir("/app")
        .with_directory("/app", source)         # ← source AFTER cache
    )
```

Then pass `--build-cache` and `--project-cache-dir` directly on the `gradlew` commands:

```python
.with_exec(["./gradlew", "test", "--build-cache", "--project-cache-dir", "/app/build-cache"])
```

> **PRIVATE** = each concurrent pipeline gets its own copy of the volume.
> **SHARED** (default) would corrupt Gradle daemon lock files.
> **LOCKED** would serialize all pipelines (3× slower).

Re-run to show cache hit on second run:

```bash
dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

---

## Step 3 — TestContainers

> **Concept**: V1 used Docker-in-Docker — Docker restarts every run, no image caching,
> N parallel tests = N simultaneous pulls. V2 routes TestContainers to a shared external
> Docker host — images survive between runs, transparent to developers.

**Uncomment `RedisConnectivityTest`** in `kotlin-app/src/test/kotlin/com/example/RedisConnectivityTest.kt`
to activate the TestContainers test.

Run it locally first (needs a local Docker daemon):

```bash
cd kotlin-app && ./gradlew test && cd ..
```

Now plug the `betclic-dagger-testcontainers-config` module into the Dagger pipeline.

**1. Add the dependency in `dagger-kotlin/dagger.json`:**

```json
{
  "name": "dagger-kotlin",
  "engineVersion": "v0.20.3",
  "sdk": { "source": "python" },
  "dependencies": [
    {
      "name": "testcontainers_config",
      "source": "github.com/betclicgroup/betclic-dagger-testcontainers-config@v1.0.11"
    }
  ]
}
```

**2. Wire it into `test()` with a single `with_()`:**

```python
container = (
    self._gradle(source)
    .with_(dag.testcontainers_config().setup)   # ← detects CI vs local automatically
    .with_exec(["./gradlew", "test"])
)
```

> `with_()` applies a module function as middleware — one line wires TestContainers.
> On CI it points to the shared Docker host. Locally it falls back to DinD.

```bash
dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
```

---

## Step 4 — Survive test failures

> **Concept**: Right now a test failure crashes the pipeline — the report is never exported.
> `ReturnType.ANY` lets the pipeline continue even when tests fail
> so we always get the JUnit XML. We return a `TestResult` object that exposes
> both `result()` (the report directory) and `exit_code()` (for the CI gate).

**Uncomment the failing test** in `kotlin-app/src/test/kotlin/com/example/FailingTest.kt`
to show what a failure looks like.

Show that the pipeline crashes — no report exported:

```bash
dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results
# ❌ Pipeline fails — report is lost
```

The `TestResult` class is already in the file — now **update `test()` to use it**
in `dagger-kotlin/src/dagger_kotlin/main.py`:

```python
@function
async def test(self, source: ...) -> TestResult:
    """Run the test suite — never raises, always returns results."""
    container = (
        self._gradle(source)
        .with_(dag.testcontainers_config().setup)
    )

    # expect=ReturnType.ANY → execution continues even if tests fail
    container = container.with_exec(["./gradlew", "test"], expect=ReturnType.ANY)
    exit_code = await container.exit_code()

    return TestResult(_container=container, _exit_code=exit_code)
```

Now the report is always exported, even when tests fail:

```bash
dagger -m dagger-kotlin call test --source ./kotlin-app \
  result export --path ./build/test-results

ls build/test-results/    # JUnit XML files — even with failures
```

Check exit code:

```bash
dagger -m dagger-kotlin call test --source ./kotlin-app exit-code
```

---

## Step 5 — Dagger Shell: one connection, two operations

> **Concept**: Calling `dagger call` twice (once for the report, once for the exit code)
> opens two separate connections to the Dagger Engine. Even if both are mostly cached,
> the connection overhead adds up. Dagger Shell lets you do both in a single session.

Show the two-call problem first:

```bash
# Connection 1 — export reports
dagger -m dagger-kotlin call test --source ./kotlin-app \
  result export --path ./build/test-results

# Connection 2 — get exit code
dagger -m dagger-kotlin call test --source ./kotlin-app exit-code
```

Now switch to Dagger Shell directly:

```bash
dagger --progress=dots -m ./dagger-kotlin --command '
  test_results=$( . | test --source=../kotlin-app )
  $test_results | result | export --path=./build/test-results
  .exit $( $test_results | exit-code )
'
```

Key points to explain:
- `$( . | test … )` — runs the test function, stores the lazy `TestResult` handle
- `$test_results | result | export` — pulls the report directory out
- `.exit` — Dagger Shell builtin that sets the process exit code **after** the export

---

## Step 6 — Wrap in a mise task

> **Concept**: The Dagger command is powerful but verbose.
> `mise` acts as the developer-facing interface — nobody needs to know Dagger internals.
> The same command works locally and in GitHub Actions unchanged.

Fill in `.mise/tasks/ci/test` (same Dagger Shell command, now behind a simple `mise run`):

```bash
#!/usr/bin/env bash
#MISE description="Run the kotlin-app test suite via Dagger"
set -euo pipefail

dagger --progress=dots -m ./dagger-kotlin --command '
  test_results=$( . | test --source=../kotlin-app )
  $test_results | result | export --path=./build/test-results
  .exit $( $test_results | exit-code )
'
```

Run it:

```bash
mise run ci:test

ls build/test-results/
```

> `.exit` is a Dagger shell builtin — it sets the process exit code so the CI step
> fails when tests fail, even though the report was already exported.

Example GitHub Actions step (no changes needed):

```yaml
- name: Test
  run: mise run ci:test

- name: Upload test results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results
    path: build/test-results/
```

---

## Quick reference

| Goal | Command |
|---|---|
| Run tests + export report | `dagger -m dagger-kotlin call test --source ./kotlin-app export --path ./build/test-results` |
| Run tests + exit code (after step 4) | `dagger -m dagger-kotlin call test --source ./kotlin-app exit-code` |
| Run tests + report (after step 4) | `dagger -m dagger-kotlin call test --source ./kotlin-app result export --path ./build/test-results` |
| Run tests (mise) | `mise run ci:test` |
| Build install dir | `dagger -m dagger-kotlin call build --source ./kotlin-app export --path ./dist` |
| Build Docker image | `dagger -m dagger-kotlin call build-docker --source ./kotlin-app` |
| Inspect functions | `dagger -m dagger-kotlin functions` |
| List mise tasks | `mise tasks` |
