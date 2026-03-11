# Dagger à l'échelle : comment éviter de se poignarder avec ses pipelines

> **DevoxxFR 2026** — Tools in Action

## Abstract

Dagger est un puissant moteur (trop ?) de CI/CD programmable basé sur des conteneurs et créé par le papa de Docker. Il permet de définir des pipelines reproductibles directement en code. Mal utilisé, il peut vite devenir un cauchemar à maintenir quand les pipelines se multiplient et que les équipes s'en emparent.

Dans ce Tools in Action, on part du terrain : démos live, exemples concrets et situations vécues. On vous montrera ce qu'il faut faire (et surtout ce qu'il ne faut pas faire) pour utiliser Dagger à grande échelle : organisation des modules, performances et expérience développeur. Un retour pragmatique et sans filtre pour tirer le meilleur de Dagger… sans se tirer une balle dans le pied.

## Speakers

| Speaker | Role |
|---------|------|
| **Vivien Maleze** | Staff Engineer @ Betclic |
| **Rodrigo** | Engineer @ Betclic |

## Structure

| Section | Speaker | Duration |
|---------|---------|----------|
| Comment on a fait chez Betclic — Golden Path + modules et nos problèmes (passer à l'échelle) | Vivien | ~5 min |
| Montage des volumes | Vivien | ~3 min |
| TestContainers | Rodrigo | ~3 min |
| Organisation des modules | Rodrigo | ~3 min |
| Rapport de tests | Rodrigo | ~3 min |
| Gestion du streamlining | Vivien | ~3 min |
| Comment simplifier les commandes Dagger à rallonge | Vivien | ~3 min |

## Slides

The presentation slides are built with [Slidev](https://sli.dev/) and available on [GitHub Pages](https://vmaleze.github.io/dagger-devoxx-2026/).

### Run locally

```bash
cd slides
npm install
npm run dev
```

### Build

```bash
cd slides
npm run build
```

## Resources

- [Dagger](https://dagger.io/)
- [Slidev](https://sli.dev/)
- [DevoxxFR 2026](https://www.devoxx.fr/)
