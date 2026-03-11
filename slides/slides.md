---
theme: default
colorSchema: light
title: "Dagger à l'échelle"
titleTemplate: "%s - DevoxxFR 2026"
favicon: /images/betclic-logo.svg
drawings:
  persist: false
transition: slide-left
mdc: true
lineNumbers: false
layout: cover
class: cover-slide
---

<div class="cover-wrapper">
  <div class="cover-tag">Tools in Action · DevoxxFR 2026</div>
  <h1 class="cover-title">Dagger à l'échelle</h1>
  <p class="cover-subtitle">Comment éviter de se poignarder avec ses pipelines</p>
  <div class="cover-speakers">
    <span>Vivien Maleze</span>
    <span class="separator">·</span>
    <span>Rodrigo</span>
  </div>
  <img src="/images/betclic-logo.svg" class="cover-logo" />
</div>

---
title: About Vivien
layout: about-me
hideInToc: true
speakerName: Vivien MALEZE
speakerTitle: Platform Engineer
speakerImage: /images/vivien-speaker.jpeg
speakerCompanyLogo: /images/ippon.png
---

::details::

* Background java <logos-java />
* +12 ans d'xp
* +7 ans chez Ippon
* Bordeaux, France 🇫🇷
* Sujets du moment
  * Developer Experience <logos-kubernetes />
  * Platform Engineering 🛠️
* <logos-twitter /> <logos-github-octocat /> @vmaleze

---
layout: about-me
speakerName: "Rodrigo"
speakerTitle: "Engineer @ Betclic"
speakerImage: /images/rodrigo.jpg
speakerCompanyLogo: /images/betclic-logo.svg
---

<template #details>
  <li>🏢 Engineer chez Betclic</li>
  <li>⚙️ CI/CD & Infrastructure</li>
  <li>🧪 Passionné de testing</li>
  <li>🚀 Dagger adopter de la première heure</li>
</template>

---
layout: section
---

# Contexte

## Ce qu'on a fait chez Betclic

---

# Le Golden Path chez Betclic

<div class="two-col">
<div>

### Avant Dagger

- Scripts shell partout 🍝
- Pipelines YAML copiés-collés entre les équipes
- Environnements locaux différents de la CI
- Onboarding long et douloureux

</div>
<div>

### La vision Golden Path

- Un seul endroit pour définir les pipelines
- **Reproductible** en local et en CI
- **Partageable** entre équipes via des modules
- **Testable** comme du vrai code

</div>
</div>

---

# Pourquoi Dagger ?

<div class="highlight-box">
  <strong>Dagger</strong> — un moteur de CI/CD programmable basé sur des conteneurs, créé par le fondateur de Docker.
</div>

<br/>

- **Pipeline as Code** : Go, Python, TypeScript... votre langage, vos règles
- **Portable** : tourne en local, sur GitHub Actions, GitLab CI, etc.
- **Modulaire** : partagez des modules comme des packages
- **Caching** natif : plus de "works on my machine"

---

# Nos problèmes — Passer à l'échelle

<div class="problems-grid">
  <div class="problem-card">
    <div class="problem-icon">💣</div>
    <div class="problem-title">Explosion des modules</div>
    <p>Des dizaines de modules sans convention ni gouvernance</p>
  </div>
  <div class="problem-card">
    <div class="problem-icon">🐢</div>
    <div class="problem-title">Performances</div>
    <p>Montage de volumes, caches mal gérés, pipelines lents</p>
  </div>
  <div class="problem-card">
    <div class="problem-icon">😵</div>
    <div class="problem-title">DX dégradée</div>
    <p>Commandes à rallonge, rapports inexploitables</p>
  </div>
  <div class="problem-card">
    <div class="problem-icon">🔒</div>
    <div class="problem-title">Streamlining</div>
    <p>Difficile de forcer les bonnes pratiques à l'échelle</p>
  </div>
</div>

---
layout: section
---

# Montage des volumes

## Le piège des performances

<div class="speaker-tag">Vivien</div>

---

# Montage des volumes

> Placez votre contenu ici

---
layout: section
---

# TestContainers

## Tester comme en production

<div class="speaker-tag">Rodrigo</div>

---

# TestContainers avec Dagger

> Placez votre contenu ici

---
layout: section
---

# Organisation des modules

## Gouvernance & conventions

<div class="speaker-tag">Rodrigo</div>

---

# Organisation des modules

> Placez votre contenu ici

---
layout: section
---

# Rapport de tests

## Rendre les résultats exploitables

<div class="speaker-tag">Rodrigo</div>

---

# Rapport de tests

> Placez votre contenu ici

---
layout: section
---

# Gestion du streamlining

## Forcer les bonnes pratiques

<div class="speaker-tag">Vivien</div>

---

# Gestion du streamlining

> Placez votre contenu ici

---
layout: section
---

# Simplifier les commandes Dagger

## Arrêtez de taper des romans dans votre terminal

<div class="speaker-tag">Vivien</div>

---

# Simplifier les commandes Dagger

> Placez votre contenu ici

---
layout: center
class: text-center
---

# Merci ! 🗡️

<div class="end-cta">
  <p>Des questions ?</p>
  <div class="social-links">
    <span>🐦 @vmaleze</span>
  </div>
</div>

<img src="/images/betclic-logo.svg" class="end-logo" />
