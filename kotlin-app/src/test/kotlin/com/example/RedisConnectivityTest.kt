package com.example

// Uncomment to enable TestContainers test in step 3 of the demo
//
// import org.junit.jupiter.api.Assertions.assertTrue
// import org.junit.jupiter.api.Test
// import org.testcontainers.containers.GenericContainer
// import org.testcontainers.junit.jupiter.Container
// import org.testcontainers.junit.jupiter.Testcontainers
// import org.testcontainers.utility.DockerImageName
//
// @Testcontainers(disabledWithoutDocker = true)
// class RedisConnectivityTest {
//
//     companion object {
//         @Container
//         @JvmField
//         val redis: GenericContainer<*> = GenericContainer(DockerImageName.parse("redis:7-alpine"))
//             .withExposedPorts(6379)
//     }
//
//     @Test
//     fun `redis container starts and exposes port`() {
//         assertTrue(redis.isRunning, "Redis container should be running")
//         assertTrue(redis.getMappedPort(6379) > 0, "Redis port should be mapped")
//     }
// }
