# Dain Kil

### AI Engineer · NLP 

**Language is my edge; ML and cloud are my tools.**  
I build AI end to end, from training models to serving them in production.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dainkil/dainkil/output/pacman-contribution-graph-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dainkil/dainkil/output/pacman-contribution-graph.svg">
    <img alt="pacman contribution graph" src="https://raw.githubusercontent.com/dainkil/dainkil/output/pacman-contribution-graph.svg">
  </picture>
</p>

---

## 📌 Pinned

| | Project | What | Highlight |
|:-:|---|---|---|
| 📜 | [**SJW Translator**](https://github.com/dainkil/sjw-translator) | Translation system for the *Seungjeongwon Ilgi* that curbs LLM name hallucination with a person KB | Name accuracy **86.9% → 92.3%** · KB-listed names **99.0%** |
| ⚾ | [**KBO Pitch Command**](https://github.com/dainkil/kbo-pitch-command-prediction) | LG Aimers 9th hackathon · pitch command grade prediction | Final score **70.314 · team best** |
| 🗣 | [**Tashkeel Check**](https://github.com/dainkil/tashkeel-check) | Front-end layer that makes Arabic voice agents read names correctly | Readings fixed by **evidence**, not guessed |

---

### 📜 [SJW Translator](https://github.com/dainkil/sjw-translator) | Name-grounded translation of the *Seungjeongwon Ilgi*
> Resolves person names in Classical Chinese source text with NER and a person knowledge base (KB),  
> injects them into the LLM prompt, and checks every response for whether the names came through correctly

`Mar – Sep 2026` · team of 4 · **My role: KB, modeling, backend, model serving** · `Oct 2026` evaluation redesign · KB expansion

The *Seungjeongwon Ilgi* (242.5M characters) is only 37.4% translated; at the current pace it won't be finished until 2062.
An LLM alone reads rare Chinese-character names as plausible but wrong Korean names (崔葕 Choe **Heon** → Choe **Yeon**), and because the output reads naturally, reviewers rarely catch it. So the LLM handles the language and a verifiable KB decides the names.

```
Source → NER (name spans) → KB linking (resolve person) → inject names into prompt → LLM translation → quality gate (name check)
```

- **Name accuracy:** KB-listed names 91.9% → **99.0%**, all names 86.9% → **92.3%** (+5.4%p, 95% CI [+1.2, +9.2]) against an independent answer key built from the expert translation (preliminary, 47 sentences · 130 names)
- **Evaluation redesign:** found that the old answer key used KB spellings as ground truth, so it was measuring whether the LLM copied the KB. Re-scoring on the new key showed 9 of the 10 remaining errors were names missing from the KB: **the bottleneck was KB coverage, not the LLM**
- **Offline KB expansion (no LLM calls):** ran NER over all 52,764 corpus sentences and promoted out-of-KB names by voting on the translation's spellings → KB **2,690 → 6,718 people** (auto-promoted precision 97.4%)
- **Serving:** NER quantized to ONNX INT8 (709MB → **178MB**, p50 17.9ms → **8.3ms**) for CPU-only serving; Spring Boot API/Worker on Redis Streams with checkpointed bulk-translation resume (**0 duplicate LLM calls**); deployed on EKS with TLS and API-key + BYOK access control

**Tech**  
`Python` `PyTorch` `ONNX Runtime` `FastAPI` `Gemini API` `Java 21` `Spring Boot` `Spring AI` `Redis Streams` `PostgreSQL` `Docker` `Kubernetes`

---

### ⚾ [KBO Pitch Command Prediction](https://github.com/dainkil/kbo-pitch-command-prediction) | LG Aimers 9th hackathon
> Predicted the command grade (Shadow / Heart / Failure) probabilities of KBO pitches and a pitcher ranking  
> from just 29 pre-pitch columns, in a 24-hour offline hackathon (DACON)

`Sep 2026` · team of 4 (miniL) · **Final score 70.314, team best** · **+1.79** over the host baseline

- Broke the metric down and found the Pitch term (Brier) was saturated; the score gap came from the **pitcher ranking (Kendall τ)**, so I reframed the problem around it
- Proposed **separating probability q from the pitcher target score t by projection** → Player **+4.9**, adopted as the team's base structure
- Designed a **ball-count row term** by ridge-regressing pitcher residuals on row state → Player **+1.08**, adopted as a standard team component
- Assembled and submitted the final model 18 minutes before the deadline with no downside risk

**Tech**  
`Python` `LightGBM` `pandas` `NumPy` `scikit-learn` `SciPy` `Empirical Bayes` `Kendall τ`

---

### 🗣 [Tashkeel Check](https://github.com/dainkil/tashkeel-check) | Name pronunciation layer for Arabic TTS
> Sits in front of the TTS engine of an Arabic voice agent, decides the correct reading of every proper name with evidence,  
> and flags low-confidence names for human confirmation

`Oct 2026 –` · **In design** (pivoted on 2026-10-23 from a shipped document-review service)

Arabic omits short vowels, so the same spelling can be read several ways (مسلم: Muslim or Musallam?). TTS engines guess silently, and diacritizers and LLMs fail most often on exactly these proper names.
Tashkeel Check uses a reading only when there is evidence for it (customer pronunciation dictionary, the person's own recording, Latin spelling on registration documents, human confirmation); otherwise it sends a default reading marked low-confidence and queues it for review.

- **Previous product:** a review tool showing English reading candidates with evidence for every name in Arabic documents (two agents + company-records MCP + document archive)
- **Key finding (EXP-003):** an instruction-only LLM already reached 99.9% strict accuracy on synthetic documents, so the product's value moved to **evidence, verification, records, and reuse**
- **Next:** engine baseline experiment (EXP-006) across 4–5 TTS engines × 3 input formats; pre-registration drafted

**Tech**  
`Python` `FastAPI` `LangGraph` `LangChain` `MCP` `CAMeL Tools` `Qdrant` `PostgreSQL` `Docker`

---

## 🛠 Tech Stack

### AI · ML

<a href="https://skillicons.dev">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=py%2Cpytorch&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=py%2Cpytorch&theme=light">
    <img alt="Python · PyTorch · ONNX Runtime" src="https://skillicons.dev/icons?i=py%2Cpytorch&theme=dark">
  </picture>
</a>
<br/>
<sub>Python · PyTorch · ONNX Runtime</sub>

### Backend

<a href="https://skillicons.dev">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=java%2Cspring%2Cfastapi&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=java%2Cspring%2Cfastapi&theme=light">
    <img alt="Java · Spring Boot · Spring AI · FastAPI" src="https://skillicons.dev/icons?i=java%2Cspring%2Cfastapi&theme=dark">
  </picture>
</a>
<br/>
<sub>Java · Spring Boot · Spring AI · FastAPI</sub>

### Data & Messaging

<a href="https://skillicons.dev">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=postgres%2Credis%2Ckafka&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=postgres%2Credis%2Ckafka&theme=light">
    <img alt="PostgreSQL · Redis · MariaDB · Kafka" src="https://skillicons.dev/icons?i=postgres%2Credis%2Ckafka&theme=dark">
  </picture>
</a>
<br/>
<sub>PostgreSQL · Redis · MariaDB · Kafka</sub>

### Cloud & Infra

<a href="https://skillicons.dev">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=docker%2Ckubernetes%2Caws&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=docker%2Ckubernetes%2Caws&theme=light">
    <img alt="Docker · Kubernetes · AWS EKS" src="https://skillicons.dev/icons?i=docker%2Ckubernetes%2Caws&theme=dark">
  </picture>
</a>
<br/>
<sub>Docker · Kubernetes · AWS EKS</sub>

### Frontend & Tools

<a href="https://skillicons.dev">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=vue%2Cgit%2Cgithub&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=vue%2Cgit%2Cgithub&theme=light">
    <img alt="Vue.js · Git · GitHub" src="https://skillicons.dev/icons?i=vue%2Cgit%2Cgithub&theme=dark">
  </picture>
</a>
<br/>
<sub>Vue.js · Git · GitHub</sub>

### Languages

<!-- LANGUAGES:START -->
```text
Python            █████████████████░░░░░░░░   69.7%
Java              ███░░░░░░░░░░░░░░░░░░░░░░   11.1%
HTML              █░░░░░░░░░░░░░░░░░░░░░░░░    5.5%
Vue               █░░░░░░░░░░░░░░░░░░░░░░░░    3.9%
Jupyter Notebook  █░░░░░░░░░░░░░░░░░░░░░░░░    2.7%
Shell             █░░░░░░░░░░░░░░░░░░░░░░░░    2.6%
JavaScript        █░░░░░░░░░░░░░░░░░░░░░░░░    2.5%
Go                ░░░░░░░░░░░░░░░░░░░░░░░░░    0.9%
Other             ░░░░░░░░░░░░░░░░░░░░░░░░░    0.9%
```
<sub>By code size (bytes) across 9 repos · updated hourly</sub>
<!-- LANGUAGES:END -->

---

## 🌐 Spoken Languages

- **🇬🇧 English** — OPIc IH · TOEIC Speaking AL 
- **🇸🇦 Arabic**

---

## 🎓 Education & Activities

### Hankuk University of Foreign Studies (HUFS) | Ingenium College of Convergence Studies
**Mar 2022 – Aug 2027**

### SKALA | SK AX
**Jul 2026 – Dec 2026**

- AI/SW industry training program run by SK AX

### LG Aimers 9th, Phase 1 & 2 & 3 | LG AI Research
**Jun 2026 – Sep 2026**

- AI/ML coursework and online hackathon

### DAT, Data Analysis Society | President
**Sep 2025 – Jun 2026**

- Led the HUFS data analysis society
- Planned and ran study groups and capstone projects

### ITDA, Inter-university Data Analysis Club (Seoul Metropolitan Area) | Organizing Committee
**Jan 2026 – Jul 2026**

- Planned and ran activities for an inter-university data analysis club in the Seoul area

### Sports

- STROKER, inter-university swimming club · Training team · Mar 2025 – present
- HUFS Swimming Team · Vice-captain · Jan 2024 – Aug 2024
