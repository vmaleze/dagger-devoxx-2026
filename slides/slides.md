---
theme: default
colorSchema: light
highlighter: shiki
shikiConfig:
  theme: github-light
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
hideInToc: true
---

# Dagger @Betclic

<div class="stats-row">
  <div class="stat-card">
    <div class="stat-value">~60</div>
    <div class="stat-label">pipelines / min</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">~400</div>
    <div class="stat-label">développeurs</div>
  </div>
  <div class="stat-card">
    <div class="stat-value">5</div>
    <div class="stat-label">langages</div>
  </div>
</div>

<div v-click class="highlight-box" style="margin-top: 1.5rem; text-align: center;">
  Comment on y est arrivé chez Betclic ? C'est ce qu'on va vous expliquer. 👉
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
  <li>🏢 Staff Engineer — DevX chez Betclic depuis 2 ans
    <ul style="margin-top:4px;padding-left:1.2em;">
      <li><logos-github-actions /> Mise en place de la plateforme CI/CD GitHub Actions + Dagger</li>
      <li>📊 Déploiement des métriques DORA</li>
    </ul>
  </li>
  <li><img src="/images/dagger.png" style="display:inline;height:1.2em;vertical-align:middle;margin-right:0.3em;" /> Adopteur de Dagger de la première heure</li>
  <li><logos-linkedin-icon /> garcia-de-oliveira-rodrigo</li>
</template>

---

# Pourquoi Dagger ?

<div class="two-col">
<div>

### Le problème 😤

- Scripts shell partout 🍝
- YAML copié-collé entre équipes
- Local ≠ CI → *"works on my machine"*
- Onboarding long, docs obsolètes

</div>
<div>

### Notre réponse ✅

- **Un seul endroit** pour les pipelines
- **Reproductible** : local = CI = partout
- **Modulaire** : partagé comme un package
- **Testable** comme du vrai code

</div>
</div>

<div class="highlight-box" style="margin-top: 1.5rem;">
  <strong>Dagger</strong> — pipelines as code, portables, conteneurisés. Créé par le fondateur de Docker.
</div>

---
layout: default
---

# Architecture Dagger chez Betclic

<div class="two-col arch-slide">
<div>

<div class="arch-v2">
  <div class="arch-v2-group">
    <div class="arch-v2-group-label">🏃 GitHub Actions Runners</div>
    <div class="arch-v2-runners">
      <div class="arch-v2-runner">
        <div class="arch-v2-rname">Runner A</div>
        <div class="arch-v2-rtag">Dagger CLI</div>
      </div>
      <div class="arch-v2-runner">
        <div class="arch-v2-rname">Runner B</div>
        <div class="arch-v2-rtag">Dagger CLI</div>
      </div>
      <div class="arch-v2-runner">
        <div class="arch-v2-rname">Runner C</div>
        <div class="arch-v2-rtag">Dagger CLI</div>
      </div>
    </div>
  </div>
  <svg class="arch-v2-svg" viewBox="0 0 300 52" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
    <line x1="50"  y1="0" x2="50"  y2="22" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="150" y1="0" x2="150" y2="22" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="250" y1="0" x2="250" y2="22" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="50"  y1="22" x2="250" y2="22" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="150" y1="22" x2="150" y2="34" stroke="#CBD5E1" stroke-width="2"/>
    <polygon points="143,31 157,31 150,42" fill="#CBD5E1"/>
  </svg>
  <div class="arch-v2-engine">
    <div class="arch-v2-ename">⚙️ Dagger Engine</div>
    <div class="arch-v2-esub">- Partagé entre tous les runners -</div>
    <div class="arch-v2-cache">💾 Cache partagé</div>
  </div>
</div>

</div>
<div class="arch-key-points">
  <div>🔌 Un seul moteur pour tous les runners</div>
  <div>💾 Cache mutualisé entre pipelines</div>
  <div>⚡ Réduction drastique du temps de CI</div>
</div>
</div>

---

# Nos problèmes — Passer à l'échelle

<div class="problems-flow">
  <div class="pf-item">
    <div class="pf-num">01</div>
    <div class="pf-icon">💣</div>
    <div class="pf-title">Explosion des modules</div>
    <div class="pf-desc">Dizaines de modules sans convention ni gouvernance</div>
  </div>
  <div v-click="1" class="pf-arrow">→</div>
  <div v-click="1" class="pf-item">
    <div class="pf-num">02</div>
    <div class="pf-icon">🐢</div>
    <div class="pf-title">Performances</div>
    <div class="pf-desc">Caches mal gérés, montages de volumes, pipelines lents</div>
  </div>
  <div v-click="2" class="pf-arrow">→</div>
  <div v-click="2" class="pf-item">
    <div class="pf-num">03</div>
    <div class="pf-icon">😵</div>
    <div class="pf-title">DX dégradée</div>
    <div class="pf-desc">Commandes à rallonge, rapports inexploitables</div>
  </div>
  <div v-click="3" class="pf-arrow">→</div>
  <div v-click="3" class="pf-item">
    <div class="pf-num">04</div>
    <div class="pf-icon">🔒</div>
    <div class="pf-title">Streamlining</div>
    <div class="pf-desc">Impossible de forcer les bonnes pratiques à l'échelle</div>
  </div>
</div>

---
layout: section
---

# Organisation des modules

## Gouvernance & conventions


---

# Organisation des modules — contexte

<div class="context-panels">
  <div class="context-panel problem">
    <div class="context-panel-header">⚠️ Le problème</div>
    <ul>
      <li>Des dizaines d'équipes, des stacks différentes</li>
      <li>Chaque équipe <strong>réécrit sa CI</strong> à sa façon</li>
      <li>Pas de standardisation, pas de gouvernance</li>
      <li>Migration Jenkins → GHA à absorber</li>
    </ul>
  </div>
  <div v-click class="context-panel solution">
    <div class="context-panel-header">✅ La réponse</div>
    <p>Un module <strong>clé en main par stack</strong>, maintenu par l'équipe DevX.</p>
    <p>Les devs <em>pluggent le module</em> — rien à configurer.</p>
  </div>
</div>


---

# Les modules par stack

<div class="module-grid">
  <div class="module-card mc-kotlin">
    <div class="mc-logo"><logos-kotlin /></div>
    <div class="mc-name">JVM / Kotlin</div>
    <div class="mc-caps">
      <span class="mc-cap">build</span><span class="mc-cap">test</span><span class="mc-cap">lint</span>
    </div>
  </div>
  <div class="module-card mc-python">
    <div class="mc-logo"><logos-python /></div>
    <div class="mc-name">Python</div>
    <div class="mc-caps">
      <span class="mc-cap">build</span><span class="mc-cap">test</span><span class="mc-cap">lint</span>
    </div>
  </div>
  <div class="module-card mc-js">
    <div class="mc-logo"><logos-javascript /></div>
    <div class="mc-name">JavaScript</div>
    <div class="mc-caps">
      <span class="mc-cap">build</span><span class="mc-cap">test</span><span class="mc-cap">lint</span>
    </div>
  </div>
  <div class="module-card mc-rust">
    <div class="mc-logo"><logos-rust /></div>
    <div class="mc-name">Rust</div>
    <div class="mc-caps">
      <span class="mc-cap">build</span><span class="mc-cap">test</span><span class="mc-cap">lint</span>
    </div>
  </div>
  <div class="module-card mc-dotnet">
    <div class="mc-logo"><logos-dotnet /></div>
    <div class="mc-name">.NET</div>
    <div class="mc-caps">
      <span class="mc-cap">build</span><span class="mc-cap">test</span><span class="mc-cap">lint</span>
    </div>
  </div>
</div>

<div v-click class="module-transverse">
  <div class="mt-card">🐳 <strong>Docker</strong> — construction & publication d'images</div>
  <div class="mt-card">🏷️ <strong>Versioning</strong> — gestion sémantique des versions</div>
</div>

<div v-click class="module-guarantees">
  <span>✅ Cache optimisé</span>
  <span>✅ Ressources adaptées</span>
  <span>✅ SonarQube intégré</span>
  <span>✅ TestContainers ready</span>
</div>

---
layout: section
---

# Montage des volumes

## Le piège des performances

---
layout: default
---

# Les principaux niveaux de cache Dagger

<div class="cache-diagram">
  <div class="cache-column layer-col">
    <div class="cache-col-header layer">Layer Cache (BuildKit)</div>
    <div class="cache-col-badge layer">Automatique</div>
    <div class="cache-row">🔑 Hash des opérations</div>
    <div class="cache-row">❄️ Immutable</div>
    <div class="cache-row">📦 Image layers</div>
    <div class="cache-row">⚡ Container ops</div>
    <div class="cache-col-note">Invalidé si <em>n'importe quel input</em> change en amont</div>
  </div>
  <div v-click class="cache-vs-divider">⚡</div>
  <div v-click="1" class="cache-column volume-col">
    <div class="cache-col-header volume">Cache Volumes</div>
    <div class="cache-col-badge volume">with_mounted_cache</div>
    <div class="cache-row volume-row">📦 gradle-cache → /root/.gradle</div>
    <div class="cache-row volume-row">🔨 build-cache-{project} → /app/build-cache</div>
    <div class="cache-row volume-row">🧶 yarn-cache → /root/.yarn</div>
    <div class="cache-row volume-row">📦 npm-cache → /root/.npm</div>
    <div class="cache-col-note">💾 Mutable · Nommé · Persiste entre les runs</div>
  </div>
</div>


---


# `CacheSharingMode` — accès concurrent au cache

<div class="tl-demo">

  <div class="tl-panel bad">
    <div class="tl-panel-title">SHARED <small style="font-weight:400;font-size:0.75em">(défaut)</small></div>
    <div class="tl-panel-desc">Accès concurrent R/W — plusieurs instances écrivent en même temps dans le même volume.</div>
    <div class="tl-traces">
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 1</div>
        <div class="tl-track"><div class="tl-span bad-span" style="left:0%;width:55%"></div></div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 2</div>
        <div class="tl-track"><div class="tl-span bad-span" style="left:20%;width:55%"></div></div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 3</div>
        <div class="tl-track"><div class="tl-span bad-span" style="left:40%;width:55%"></div></div>
      </div>
    </div>
    <div class="tl-axis"><span>0s</span><span>5s</span><span>10s</span></div>
    <div class="tl-panel-verdict">⚠️ Cache corrompu</div>
  </div>

  <div v-click class="tl-panel warn">
    <div class="tl-panel-title">LOCKED</div>
    <div class="tl-panel-desc">Accès exclusif au volume — les pipelines 2 et 3 attendent que le verrou soit libéré. Pas de parallélisation !</div>
    <div class="tl-traces">
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 1</div>
        <div class="tl-track"><div class="tl-span warn-span" style="left:0%;width:33%"></div></div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 2</div>
        <div class="tl-track">
          <div class="tl-span wait-span" style="left:0%;width:33%"></div>
          <div class="tl-span warn-span" style="left:33%;width:33%"></div>
        </div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 3</div>
        <div class="tl-track">
          <div class="tl-span wait-span" style="left:0%;width:66%"></div>
          <div class="tl-span warn-span" style="left:66%;width:34%"></div>
        </div>
      </div>
    </div>
    <div class="tl-axis"><span>0s</span><span>8s</span><span>15s</span></div>
    <div class="tl-panel-verdict">🐢 3× plus lent</div>
  </div>

  <div v-click class="tl-panel good">
    <div class="tl-panel-title">PRIVATE</div>
    <div class="tl-panel-desc">Copie isolée par container — chaque pipeline a son propre volume, pas de contention.</div>
    <div class="tl-traces">
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 1</div>
        <div class="tl-track"><div class="tl-span good-span" style="left:0%;width:55%"></div></div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 2</div>
        <div class="tl-track"><div class="tl-span good-span" style="left:0%;width:55%"></div></div>
      </div>
      <div class="tl-span-row">
        <div class="tl-service">Pipeline 3</div>
        <div class="tl-track"><div class="tl-span good-span" style="left:0%;width:55%"></div></div>
      </div>
    </div>
    <div class="tl-axis"><span>0s</span><span>3s</span><span>5s</span></div>
    <div class="tl-panel-verdict">✅ Rapide & isolé</div>
  </div>

</div>

---
layout: section
---

# TestContainers

## Tester comme en production


---

# TestContainers avec Dagger

<div class="tc-arch-grid">

  <div class="tc-arch-col">
    <div class="tc-arch-label v1">V1 — Module daggerverse</div>
    <div class="tc-arch-diagram v1">
      <div class="tc-arch-box tc-arch-cli">🖥️ Dagger CLI</div>
      <div class="tc-arch-connector">↓</div>
      <div class="tc-arch-box tc-arch-engine">
        ⚙️ Dagger Engine
        <div class="tc-arch-engine-inner">
          <div class="tc-arch-dind">
            <div class="tc-arch-dind-title">🐳 Docker DinD (service)</div>
            <div class="tc-arch-containers">
              <span class="tc-arch-container">mongo</span>
              <span class="tc-arch-container">localstack</span>
              <span class="tc-arch-container">postgres</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-click="1" class="tc-arch-problem-note">
      ⚠️ Docker redémarre à chaque run → <strong>images non cachées</strong><br/>
      Tests parallèles → <strong>N pulls simultanés</strong> → saturation IOP
    </div>
  </div>

  <div v-click="2" class="tc-arch-col">
    <div class="tc-arch-label v2">V2 — Notre module custom</div>
    <div class="tc-arch-diagram v2">
      <div class="tc-arch-box tc-arch-cli">🖥️ Dagger CLI</div>
      <div class="tc-arch-connector">↓</div>
      <div class="tc-arch-box tc-arch-engine">⚙️ Dagger Engine</div>
      <div class="tc-arch-connector">↓</div>
      <div class="tc-arch-box tc-arch-external">
        🐳 Docker Host externe
        <div class="tc-arch-containers" style="margin-top:6px;justify-content:center;">
          <span class="tc-arch-container" style="background:rgba(0,0,0,0.08);">mongo</span>
          <span class="tc-arch-container" style="background:rgba(0,0,0,0.08);">localstack</span>
          <span class="tc-arch-container" style="background:rgba(0,0,0,0.08);">postgres</span>
        </div>
      </div>
    </div>
    <div class="tc-arch-benefit-note">
      ✅ Images téléchargées <strong>une seule fois</strong> — cache Docker persistant<br/>
      🔀 En local → TCP daemon · Fallback → DinD service
    </div>
  </div>

</div>

---
layout: section
---

# Rapport de tests

## Rendre les résultats exploitables


---

# Rapport de tests — Le problème

<div class="highlight-box">
  Par défaut, si des tests échouent, Dagger <strong>arrête l'exécution immédiatement</strong>.<br/>
  Les rapports de tests ne peuvent pas être exportés — la CI n'affiche rien.
</div>

<br/>

<div class="code-compare-grid">
<div class="code-compare-block bad-block">
<div class="code-compare-label bad-label">❌ Par défaut — pipeline stoppé, rapport perdu</div>

```python
# Si des tests échouent 
# → exception levée immédiatement
container = container.with_exec(
    ["./gradlew", "test"])
# → export jamais atteint
return container
```

</div>
<div v-click="1" class="code-compare-block good-block">
<div class="code-compare-label good-label">✅ ReturnType.ANY + objet TestResult</div>

```python
# L'exécution continue même si les tests échouent
container = container.with_exec(
    ["./gradlew", "test"],
    expect=ReturnType.ANY
)
exit_code = await container.exit_code()
return TestResult(
    _container=container,
    _exit_code=exit_code
)
```

</div>
</div>

<div v-click="2" class="trap-insight">
  ⚠️ Problème : récupérer les rapports <strong>et</strong> le code de sortie nécessite <strong>deux appels Dagger distincts</strong> — deux connexions au engine.
</div>

---

# Rapport de tests — Dagger Shell

<div class="highlight-box">
  <strong>Dagger Shell</strong> enchaîne plusieurs opérations en <strong>une seule connexion</strong> au engine — export des résultats <em>et</em> propagation du code de sortie.
</div>

<br/>

<div class="code-compare-grid">
<div class="code-compare-block bad-block">
<div class="code-compare-label bad-label">❌ Deux appels = deux connexions</div>

```bash
dagger -m dagger-kotlin call test \
  --source ./kotlin-app \
  result export --path ./build/test-results

dagger -m dagger-kotlin call test \
  --source ./kotlin-app exit-code
```

</div>
<div v-click="1" class="code-compare-block good-block">
<div class="code-compare-label good-label">✅ Dagger Shell — une connexion</div>

```bash
dagger -m ./dagger-kotlin --command '
  test_results=$( test --source=../kotlin-app )
  $test_results | result | export \
    --path=./build/test-results
  .exit $( $test_results | exit-code )
'
```

</div>
</div>

<div v-click="1" class="trap-insight">
  ⚡ <code>.exit</code> est un builtin Dagger Shell — il propage le code de sortie pour faire échouer la CI si les tests échouent, même après l'export des rapports.
</div>

---
layout: section
---

# Simplifier les commandes Dagger

## Arrêtez de taper des romans dans votre terminal


---

# Simplifier les commandes Dagger

<div class="simplify-demo">
  <div class="sl-before-label simplify-label simplify-before-label">Avant — appel Dagger direct</div>
  <div v-click="1" class="sl-after-label simplify-label simplify-after-label">Après — mise comme interface</div>

  <div class="sl-before-code">

```bash
dagger -m ./dagger-kotlin --command '
  test_results=$( . | test --source=../kotlin-app )
  $test_results | result | export --path=./build/test-results
  .exit $( $test_results | exit-code )
'
```

  </div>

  <div v-click="1" class="sl-arrow">→</div>

  <div v-click="1" class="sl-after-code">

```bash
mise run kotlin:ci:test
```

  </div>
</div>

<div v-click="1" class="simplify-win-bar">
  <span>✅ Pas de syntaxe Dagger à connaître</span>
  <span>✅ Pas d'env vars de versions</span>
  <span>✅ Dagger réduit à un détail d'implémentation</span>
</div>

---
layout: section
---

# Gestion du streamlining

## Forcer les bonnes pratiques


---

# Versions sans friction

<div class="streamline-flow">
  <div class="sf-step">
    <div class="sf-icon">👩‍💻</div>
    <div class="sf-label"><code>mise run kotlin:ci:test</code></div>
  </div>
  <div v-click="1" class="sf-arrow">→</div>
  <div v-click="1" class="sf-step sf-highlight">
    <div class="sf-icon">🔍</div>
    <div class="sf-label"><strong>betclic-action-tools-version</strong><br/><small>résout les versions pour le domaine</small></div>
  </div>
  <div v-click="2" class="sf-arrow">→</div>
  <div v-click="2" class="sf-step">
    <div class="sf-icon">⚙️</div>
    <div class="sf-label">Dagger appelé<br/><small>avec la bonne version du module</small></div>
  </div>
  <div v-click="3" class="sf-arrow">→</div>
  <div v-click="3" class="sf-step sf-ok">
    <div class="sf-icon">✅</div>
    <div class="sf-label">Résultat<br/><small>local = CI, toujours</small></div>
  </div>
</div>

<div v-click="4" class="streamline-note">
  Aucune env var à gérer, aucune version à pinner manuellement.<br/>
  <strong>betclic-action-tools-version</strong> est embarqué dans chaque tâche mise — invisible pour le développeur.
</div>

---

# Rollouts progressifs

<div class="two-col" style="gap:24px">
<div>

### Priorité de résolution

<div class="rollout-track">
  <div class="rt-row rt-early">
    <div class="rt-label">✨ <strong>Early adopter</strong></div>
    <div class="rt-desc">Flag opt-in — reçoit la nouvelle version en avance</div>
  </div>
  <div class="rt-row rt-domain">
    <div class="rt-label">🚀 <strong>Rollout par domaine</strong></div>
    <div class="rt-desc">DevX déploie domaine par domaine, progressivement</div>
  </div>
  <div class="rt-row rt-stable">
    <div class="rt-label">📦 <strong>Stable</strong></div>
    <div class="rt-desc">Version courante validée — défaut pour tous</div>
  </div>
</div>

</div>
<div>

### Nouvelle version de Dagger

```
DevX publie Dagger 0.20 + modules compatibles
          ↓
Tests de validation automatiques
          ↓
Rollout domaine par domaine
  → devx      ✅ migré
  → payments  ✅ migré
  → betting   ⏳ en attente
          ↓
Passage en stable — tous les autres migrent
```

<div class="mise-win" style="margin-top:10px">
  <span>✅ Zéro PR de mise à jour</span>
  <span>✅ Rollback immédiat si problème</span>
</div>

</div>
</div>
---
layout: center
class: text-center
---

# Merci ! 🗡️

<div class="end-cta">
  <p>Des questions ?</p>
  <div class="social-links">
    <span>🐦 @vmaleze</span><br/>
    <span><logos-linkedin-icon /> garcia-de-oliveira-rodrigo</span>
  </div>
</div>

<img src="/images/betclic-logo.svg" class="end-logo" />
