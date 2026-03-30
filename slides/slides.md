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
speakerName: "Rodrigo GARCIA DE OLIVEIRA"
speakerTitle: "Staff Engineer @ Betclic"
speakerImage: /images/rodrigo.jpg
speakerCompanyLogo: /images/betclic-logo.svg
---

<template #details>
  <li>🏢 Staff Engineer — DevX chez Betclic depuis 2 ans</li>
  <li><logos-github-actions /> Mise en place de la plateforme CI/CD GitHub Actions + Dagger</li>
  <li>📊 Déploiement des métriques DORA</li>
  <li><img src="/images/dagger.png" style="display:inline;height:1.2em;vertical-align:middle;margin-right:0.3em;" /> Adopteur de Dagger de la première heure</li>
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
layout: default
---

# Architecture Dagger chez Betclic

<div class="architecture-diagram">

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Runners                   │
│                                                             │
│   Runner A          Runner B          Runner C              │
│  ┌────────┐        ┌────────┐        ┌────────┐            │
│  │ dagger │        │ dagger │        │ dagger │            │
│  │  CLI   │        │  CLI   │        │  CLI   │            │
│  └───┬────┘        └───┬────┘        └───┬────┘            │
│      │                 │                 │                  │
│      └─────────────────┼─────────────────┘                 │
│                        │                                    │
│              ┌─────────▼──────────┐                        │
│              │   Dagger Engine    │                        │
│              │    (mutualisé)     │                        │
│              │                   │                         │
│              │  ┌─────────────┐  │                         │
│              │  │   Cache     │  │                         │
│              │  │  partagé    │  │                         │
│              │  └─────────────┘  │                         │
│              └───────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

</div>

- **Un seul moteur Dagger** partagé entre tous les runners
- **Cache mutualisé** : le build d'un runner profite à tous les suivants
- **Réduction drastique** des temps de CI sur les pipelines répétitifs

<div class="speaker-tag">Rodrigo</div>

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

<div class="two-col">
<div>

**V1 — Module daggerverse**

- [`vito/daggerverse/testcontainers`](https://daggerverse.dev/mod/github.com/vito/daggerverse/testcontainers@edb98345c16e14ac7529fd103c4ce3f8dcab54f5) — Docker DinD as a service
- Zéro modification côté dev : local = CI
- ✅ Simple à mettre en place

**Le problème**

- Docker démarré à chaque exécution → **images non cachées**
- Images lourdes (Localstack, Mongo...)
- Tests parallélisés en groupes → **N téléchargements simultanés**
- Résultat : saturation des **IOP disque** du Dagger Engine

</div>
<div>

**V2 — Notre module custom**

- CI → **Docker host externe** au Dagger Engine
- Local → **TCP Docker daemon** local
- Fallback → DinD service (comportement V1)

<br/>

- Images partagées, **téléchargées une seule fois**
- Cache Docker préservé entre les runs
- Toujours transparent pour les devs

</div>
</div>

<div class="speaker-tag">Rodrigo</div>

---
layout: section
---

# Organisation des modules

## Gouvernance & conventions

<div class="speaker-tag">Rodrigo</div>

---

# Organisation des modules

<div class="highlight-box">
  Migration massive <strong>Jenkins → GitHub Actions</strong> — fournir des modules <em>clé en main</em> pour migrer rapidement sans se soucier des détails d'implémentation.
</div>

<br/>

<div class="two-col">
<div>

### Modules par stack technique

<table style="font-size:0.8rem; width:100%">
  <thead>
    <tr><th>Stack</th><th>build</th><th>test</th><th>lint</th><th>sonar</th></tr>
  </thead>
  <tbody>
    <tr><td><logos-kotlin /></td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td><logos-python /> Python</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td><logos-javascript /> JS</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td><logos-rust /> Rust</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
    <tr><td><logos-dotnet /> .NET</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
  </tbody>
</table>

</div>
<div>

### Modules transverses

- 🐳 **Docker Build** — construction & publication d'images
- 🏷️ **Versioning** — gestion sémantique des versions

### Ce que chaque module garantit

- Cache optimisé out-of-the-box
- Ressources adaptées à la charge
- Intégration transparente avec SonarQube et TestContainers

</div>
</div>

<div class="speaker-tag">Rodrigo</div>

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
