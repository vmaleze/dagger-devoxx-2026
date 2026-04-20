import dagger
from typing import Annotated
from dagger import dag, function, object_type, field, Doc, Ignore, CacheSharingMode

JDK_IMAGE = "eclipse-temurin:25-jdk"
JRE_IMAGE = "eclipse-temurin:25-jre"

# Volatile/generated paths excluded from the source snapshot to avoid
# busting the Dagger layer cache on every run.
SOURCE_IGNORE = [
    "**/build",
    ".gradle",
    ".github",
    ".idea",
    ".vscode",
]


async def _extract_test_report(container: dagger.Container) -> dagger.Directory:
    """Collect JUnit XML files from the build output into a flat directory."""
    report = dag.directory()
    xml_files = await container.directory("/app").glob(
        "**/build/test-results/test/*.xml"
    )
    for xml in xml_files:
        report = report.with_file(
            xml.split("/")[-1],
            container.directory("/app").file(xml),
        )
    return report


@object_type
class TestResult:
    """Holds test results without failing the pipeline on test errors."""

    _container: dagger.Container = field()
    _exit_code: int = field()

    @function
    def exit_code(self) -> int:
        """0 = all tests passed, non-zero = failures."""
        return self._exit_code

    @function
    async def result(self) -> dagger.Directory:
        """JUnit XML reports, extracted from the build output."""
        return await _extract_test_report(self._container)


@object_type
class DaggerKotlin:
    def _gradle(self, source: dagger.Directory) -> dagger.Container:
        return (
            dag.container()
            .from_(JDK_IMAGE)
            # .with_mounted_cache(
            #     "/root/.gradle",
            #     dag.cache_volume("gradle-cache"),
            #     sharing=CacheSharingMode.PRIVATE,  # isolated per pipeline
            # )
            .with_workdir("/app")
            .with_directory("/app", source)
        )

    @function
    async def test(
        self,
        source: Annotated[dagger.Directory, Ignore(SOURCE_IGNORE), Doc("Source directory of the kotlin app")],
    ) -> dagger.Directory:
        """Run the test suite and return JUnit XML reports."""
        container = self._gradle(source).with_exec(["./gradlew", "test"])
        return await _extract_test_report(container)

    # @function
    # async def test(
    #     self,
    #     source: Annotated[dagger.Directory, Ignore(SOURCE_IGNORE), Doc("Source directory of the kotlin app")],
    # ) -> TestResult:
    #     """Run the test suite — never raises, always returns results."""
    #     container = self._gradle(source).with_exec(
    #         ["./gradlew", "test", "--build-cache", "--project-cache-dir", "/app/build-cache"],
    #         expect=dagger.ReturnType.ANY,
    #     )
    #     exit_code = await container.exit_code()
    #     return TestResult(_container=container, _exit_code=exit_code)

    @function
    def build(
        self,
        source: Annotated[dagger.Directory, Ignore(SOURCE_IGNORE), Doc("Source directory of the kotlin app")],
    ) -> dagger.Directory:
        """Build the application and return the install directory"""
        return (
            self._gradle(source)
            .with_exec(["./gradlew", "installDist", "--build-cache", "--project-cache-dir", "/app/build-cache"])
            .directory("/app/build/install/kotlin-app")
        )

    @function
    def build_docker(
        self,
        source: Annotated[dagger.Directory, Ignore(SOURCE_IGNORE), Doc("Source directory of the kotlin app")],
    ) -> dagger.Container:
        """Build a Docker image ready to run the application"""
        dist = self.build(source)

        return (
            dag.container()
            .from_(JRE_IMAGE)
            .with_directory("/app", dist)
            .with_entrypoint(["/app/bin/kotlin-app"])
        )
