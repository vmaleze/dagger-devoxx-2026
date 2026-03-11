<script setup>
const props = defineProps({
  speakerName: {
    type: String,
    required: true,
  },
  speakerTitle: {
    type: String,
    required: true,
  },
  speakerImage: {
    type: String,
    required: true,
  },
  speakerCompanyLogo: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="slidev-layout about-me">
    <div class="about-me-inner">
      <!-- Left: info -->
      <div class="about-me-info">
        <h1 class="about-me-name">{{ props.speakerName }}</h1>
        <p class="about-me-title">{{ props.speakerTitle }}</p>
        <ul class="about-me-details">
          <slot name="details" />
        </ul>
        <img :src="props.speakerCompanyLogo" class="about-me-company-logo" />
      </div>

      <!-- Right: photo -->
      <div class="about-me-photo-wrap">
        <img
          :src="props.speakerImage"
          class="about-me-photo"
          :alt="props.speakerName"
        />
        <!-- decorative red arc behind photo -->
        <div class="about-me-photo-bg" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-me-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 48px 64px;
  gap: 40px;
}

.about-me-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.about-me-name {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--betclic-dark, #1A1A1A);
  line-height: 1.1;
  margin: 0;
  border-bottom: none !important;
  padding-bottom: 0 !important;
}

.about-me-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--betclic-red, #E30613);
  margin: 0;
}

.about-me-details {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.about-me-details :slotted(li) {
  font-size: 0.95rem;
  color: var(--betclic-dark, #1A1A1A);
  padding-left: 0;
}

.about-me-details :slotted(li)::before {
  display: none;
}

.about-me-company-logo {
  width: 130px;
  margin-top: 20px;
  border-radius: 0 !important;
  box-shadow: none !important;
}

/* Photo section */
.about-me-photo-wrap {
  position: relative;
  flex-shrink: 0;
}

.about-me-photo-bg {
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--betclic-red, #E30613) 0%, var(--betclic-yellow, #FFD200) 100%);
  z-index: 0;
  opacity: 0.15;
}

.about-me-photo {
  width: 260px;
  height: 260px;
  border-radius: 50%;
  object-fit: cover;
  border: 5px solid var(--betclic-red, #E30613);
  position: relative;
  z-index: 1;
  box-shadow: 0 8px 32px rgba(227, 6, 19, 0.2);
}
</style>
