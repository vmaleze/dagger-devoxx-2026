<script setup>
const props = defineProps({
  speakerName: { type: String, required: true },
  speakerTitle: { type: String, required: true },
  speakerImage: { type: String, required: true },
  speakerCompanyLogo: { type: String, required: true },
})

// Dynamic :src bindings are not processed by Vite's asset pipeline,
// so we must manually prepend the base URL for GitHub Pages deployments.
const base = import.meta.env.BASE_URL.replace(/\/$/, '')
const resolvedImage = base + props.speakerImage
const resolvedLogo = base + props.speakerCompanyLogo
</script>

<template>
  <div class="slidev-layout about-me">

    <!-- Dragon Ball background -->
    <img src="/images/speaker.jpeg" class="absolute left-7/10 top-0 bottom-0 right-0 w-2/5 object-cover object-center">

    <!-- Profile picture -->
    <img
      :src="resolvedImage"
      class="absolute rounded-full object-cover z-10"
      style="width: 280px; height: 280px; top: 50%; left: 48%; transform: translateY(-50%); border: 5px solid var(--betclic-red); box-shadow: 0 8px 32px rgba(225, 0, 20, 0.2);"
    />

    <!-- Bio -->
    <div class="bio">
      <h1>{{ props.speakerName }}</h1>
      <p class="title">{{ props.speakerTitle }}</p>
      <div class="details">
        <slot name="details" />
      </div>
      <img :src="resolvedLogo" class="logo">
    </div>

  </div>
</template>

<style>
/* ---- Bio container ---- */
.about-me .bio {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 38%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 14px;
  padding: 32px 24px 32px 40px;
}

.about-me .bio h1 {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--betclic-dark);
  line-height: 1.1;
  margin: 0;
  white-space: nowrap;
}

.about-me .bio .title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--betclic-red);
  margin: 0;
}

.about-me .bio .logo {
  width: 110px;
  box-shadow: none !important;
  border-radius: 0 !important;
}

/* ---- Details list ---- */
.about-me .details ul {
  list-style: disc;
  padding-left: 20px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.about-me .details ul li {
  font-size: 1rem;
  color: var(--betclic-dark);
  line-height: 1.4;
  padding: 0;
}

.about-me .details ul li::before {
  content: none;
}

.about-me .details ul li::marker {
  color: var(--betclic-red);
}

/* nested list */
.about-me .details ul ul {
  padding-left: 14px;
  margin-top: 2px;
  list-style: circle;
}

.about-me .details ul ul li::marker {
  color: var(--betclic-gray);
}
</style>
