# Dain Kil

### AI Engineer · NLP 

**Language is my edge; ML and cloud are my tools.**  
I build AI end to end, from training models to serving them in production.

언어를 깊이 이해하는 것이 제 강점이고, 그 강점으로 AI를 만듭니다.  
데이터 구축부터 모델 학습, 클라우드 서빙까지 직접 해왔습니다.

<p align="center">
  <img src="metrics.terminal.svg" alt="GitHub metrics" />
</p>

---

## Featured Projects

| | Project | What | Highlight |
|:-:|---|---|---|
| 📜 | [**SJW Translator**](https://github.com/dainkil/sjw-translator) | 인물 KB로 LLM 인명 환각을 억제한 《승정원일기》 번역 시스템 | 인명 정확도 **86.9% → 92.3%** · KB 등재 인물 **99.0%** |
| ⚾ | [**KBO Pitch Command**](https://github.com/dainkil/kbo-pitch-command-prediction) | LG Aimers 9기 해커톤 · 투구 제구등급 예측 | 최종 Score **70.314 · 팀 최고** |
| 🕌 | [**ShariahGuard**](https://github.com/dainkil/sharia-guard) | 샤리아·할랄 컴플라이언스 탐지 Kafka MSA | 구독 모델별 **비동기 판정 + 감사 이력** |

<p align="center">
  <img src="metrics.repositories.svg" alt="Featured repositories" />
</p>

---

### 📜 [SJW Translator](https://github.com/dainkil/sjw-translator) | 인물 KB로 LLM 인명 환각을 억제한 《승정원일기》 번역 시스템
> 한문 원문의 인명을 NER과 인물 지식베이스(KB)로 확정해 LLM에 주입하고,  
> 번역문에 올바르게 반영됐는지 매 응답 검증하는 번역 서빙 시스템

`2026.03 – 2026.09` · 4인 팀 · **담당: KB 구축 · 모델링 · 백엔드 · 모델 서빙** · `2026.10` 평가 재설계 · KB 확장

《승정원일기》(2억 4,250만 자)는 국역률 37.4%로, 지금 속도면 완역까지 2062년이 걸립니다.
LLM 단독 번역은 드문 한자 이름을 그럴듯한 다른 음으로 읽고(崔葕 최**헌** → 최**연**, 沈詻 심**악** → 심**액**),
번역문 자체는 자연스러워서 검수에서도 잘 걸러지지 않습니다. 그래서 언어 변환은 LLM에, 인명 확정은 검증 가능한 KB에 맡겼습니다.

```
원문 → NER(인명 위치) → KB 링킹(인물 확정) → 프롬프트에 인명 주입 → LLM 번역 → 품질 게이트(인명 반영 검증)
```

| 항목 | 기준 | 결과 |
|---|---|---|
| 인명 정확도 · KB 등재 인물 | LLM 단독 91.9% | **99.0%** (인명 오류 8 → 1건) |
| 인명 정확도 · 전체 이름 | LLM 단독 86.9% | **92.3%** (+5.4%p, 95% CI [+1.2, +9.2]) |
| 번역 품질 (chrF) | 37.90 | **40.32** (입력 토큰 −11.2%) |
| NER 추론 지연 (p50) | PyTorch 17.9ms | **8.3ms** (인명 재현율 100% 유지) |
| NER 모델 크기 | 709MB | **178MB** |
| 인물 KB (오프라인 확장) | 2,690명 | **6,718명** (자동 승격분 정밀도 97.4%) |
| 대량 번역 재개 | — | 강제 종료 후 재개 시 **중복 LLM 호출 0건** |

<sub>인명 정확도는 전문가 국역 표기로 만든 독립 정답지 기준 예비 결과입니다(47문장 · 130명, 3회 반복). 같은 조건의 300문장 A/B는 판정 규칙을 실행 전에 사전 등록해 두었습니다.</sub>

- **NER · KB 링킹** — NER 도메인 적응 · 파인튜닝, 인조 연간 인물 2,690명 KB와 표기 변형 역색인(9,403키), 역색인 → 활동 시기 → 관직 3단계 링킹. 이름 경계 · 동음이의 모호성을 막으려고 벡터 DB/RAG 대신 결정론적 정확 일치를 택함
- **평가 재설계** — 기존 정답지가 KB 표기를 정답으로 쓰고 KB 밖 이름 151건이 빠져 있어, 종전 97.1%가 사실상 "LLM이 KB를 옮겨 적었는가"를 재고 있었음을 발견. 전문가 국역 표기 기준 독립 정답지(527명)를 다시 만들어 KB 등재 / 미등재 구간으로 재채점 → 남은 오류 10건 중 9건이 KB 밖 이름, **병목이 LLM이 아니라 KB 커버리지**임을 확인
- **오프라인 KB 확장 (CRAG-inspired, LLM 0회)** — 코퍼스 52,764문장 전수 NER로 KB 밖 인명을 찾고, 같은 행 국역의 한글 표기를 투표 · 합의율로 등급화해 High 4,028명만 자동 승격. 시기 분할(재위 1–20년에서 수집 → 21–27년 평가) 커버리지 25–33%를 일반화 크기로 따로 보고
- **프롬프트 · 품질 게이트** — 구성 요소별 통제 실험(판정 기준 사전 고정, 3회 반복 중앙값)으로 v4 채택. 추가 LLM 호출 없이 인명 반영을 판정해 모든 응답에 VERIFIED / DEGRADED / REJECTED 등급 부여 (전문가 번역 대상 오탐률 3.9%)
- **백엔드** — Spring Boot API/Worker + Redis Streams 비동기 큐, 체크포인트 기반 대량 번역 재개, 같은 429 응답을 분당 · 일일 · 월 한도로 나눠 재시도 / 일시정지 / 격리. 워커 1대와 2대의 처리량이 같아(23.4 vs 23.1 jobs/min, 상한은 외부 API 한도) 1대로 고정
- **서빙 · 배포** — NER을 ONNX INT8로 경량화해 GPU 없이 CPU만으로 서빙, 멀티스테이지 빌드로 API · Worker 이미지 약 600MB → 180MB. SKALA EKS에 공개 배포해 TLS · HSTS, API 키 + 사용자 LLM 키(BYOK) 접근 제어, 캐시 히트 1ms(미스 2,018ms)를 검증
- 설계 결정 23건을 [ADR](https://github.com/dainkil/sjw-translator/tree/main/docs/adr)로 기록

**Tech**  
`Python` `PyTorch` `ONNX Runtime` `FastAPI` `Gemini API` `Java 21` `Spring Boot` `Spring AI` `Resilience4j` `Redis Streams` `PostgreSQL` `Flyway` `Docker` `Kubernetes`

---

### ⚾ [KBO Pitch Command Prediction](https://github.com/dainkil/kbo-pitch-command-prediction) | LG Aimers 9기 해커톤
> 투구 직전 정보 29열만으로 KBO 투구의 제구 등급(Shadow / Heart / Failure) 확률과  
> 투수 순위를 예측한 24시간 오프라인 해커톤 (DACON)

`2026.09` · 4인 팀 (miniL) · **최종 Score 70.314 — 팀 최고** · 주최 베이스라인 대비 **+1.79**

- 평가식을 분해해 Pitch(Brier)는 포화, 점수 차는 **투수 순위(Kendall τ)** 에서 난다는 것을 찾아 문제를 재정의
- 확률 q와 투수 목표점수 t를 **사영(projection)으로 분리**하는 구조 제안 → Player **+4.9**, 팀 기본 구조로 채택
- 투수 잔차를 행 상태에 릿지 회귀한 **볼카운트 행 항** 설계 → Player **+1.08**, 팀 표준 부품으로 채택
- Player 불변 q 앙상블 + 온도 보정으로 마감 18분 전 하방 위험 없이 **최종 조립·제출**
- 오프라인 폴드와 LB의 Player 부호 불일치(0/7)를 확인하고, LB 탐침 규칙과 자동 게이트(행 독립 · 확률 합 · 재현 점수) 구축

**Tech**  
`Python` `LightGBM` `pandas` `NumPy` `scikit-learn` `SciPy` `Empirical Bayes` `Kendall τ`

---

### 🕌 [ShariahGuard](https://github.com/dainkil/sharia-guard) | 샤리아·할랄 컴플라이언스 탐지 MSA
> 은행·증권사가 컴플라이언스 탐지 모델을 구독하고, 자체 거래 데이터를 API로 보내면  
> 모델별 적합성 판정과 감사 이력을 받는 Kafka 기반 MSA

- 교육용 MSA 실습 구조를 금융기관 대상 B2B 서비스로 재설계 (공통 파일 68개 변경, AI 판정 서비스 신규 추가)
- API Key(BCrypt 해시) 기반 거래 수신 → 기관의 ACTIVE 구독 모델별 `trade.received` Kafka 이벤트 발행
- Python/FastAPI 판정 워커: AAOIFI 금지 업종 · 할랄 사업활동 · 재무 한도(이자부채 33%, 비허용 수익 5%) 규칙
- 결과 발행 성공 후 offset 커밋으로 메시지 유실 방지, `kafka-init`으로 토픽 파티션 생성 경쟁 상태 방지
- 기존 제한 종목 사전 차단, 최대 3초 대기 후 `CLEAR` / `ALERT` / `REVIEW` / `PENDING` 응답과 기관별 감사 이력 저장

**Tech**  
`Java` `Spring Boot` `Spring Cloud` `Eureka` `OAuth2` `JWT` `Kafka` `FastAPI` `MariaDB` `Vue` `Docker`

---

## 🧩 Other Projects

- 🤟 [**ASL Translator**](https://github.com/dainkil/ASL_translator) — RGB · 랜드마크 Two-Track 기반 End-to-End 수어 번역 (Track B BLEU-4 44.41, 38.7ms/sample)
- 🔍 [**Sharia Screener**](https://github.com/dainkil/sharia-screener) — AAOIFI 정량 심사 + LLM 정성 심사를 결합한 MCP Agent Tool
- 🕸 [**GNN Fraud Detection**](https://github.com/dainkil/GNN_Fraud_Detection) — GNN 기반 조직적 어뷰징 네트워크 탐지 학술제 기획 (YelpZip)

---

## 🎓 Education & Activities

### 한국외국어대학교 | 융합인재학부
**2022.03 ~ 2027.08**

### SKALA | SK AX
**2026.07 ~ 2026.12**

- SK AX 주관 AI/SW 실무 인재 양성 과정 참여

### LG Aimers 9기 Phase 1 & 2 & 3 | (주)엘지경영개발원 AI연구원
**2026.06 ~ 2026.09**

- AI/ML 이론 교육 및 온라인 해커톤 참여


### 데이터 분석 학회 DAT | 학회장
**2025.09 ~ 2026.06**

- 한국외국어대학교 데이터 분석 학회 운영 총괄 
- 스터디 · 캡스톤 프로젝트 기획 및 운영

### 수도권연합데이터분석동아리 ITDA | 운영진
**2026.01 ~ 2026.07**

- 수도권 대학 연합 데이터 분석 동아리 운영진으로 활동 기획 및 운영

### Sports

- 대학연합수영동아리 STROKER · 훈련팀 · 2025.03 ~ 현재
- 한국외국어대학교 수영부 · 부주장 · 2024.01 ~ 2024.08

---

## 🏆 Awards

- 🏅 **LINK 대학생 연합 아이디어톤** 
- 🥇 **DAT 7th Capstone 대상** 
- 🏅 **HUFS LinguaTech Expo 장려상** 

---

## 📜 Certifications

- 수상구조사 2급 
- SQLD 
- 컴퓨터활용능력 2급 
---

## 🌐 Languages

- **🇬🇧English** — OPIc IH · TOEIC Speaking AL 
- **🇸🇦Arabic**

---

## 🛠 Tech Stack

### AI · ML

<div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/ONNX_Runtime-005CED?style=for-the-badge&logo=onnx&logoColor=white"/>
  
</div>

### Backend

<div>
  <img src="https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=openjdk&logoColor=white"/>
  <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white"/>
  <img src="https://img.shields.io/badge/Spring_AI-6DB33F?style=for-the-badge&logo=spring&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
</div>

### Data & Messaging

<div>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>
  <img src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white"/>
  <img src="https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white"/>
</div>

### Cloud & Infra

<div>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS_EKS-FF9900?style=for-the-badge"/>
</div>

### Frontend & Tools

<div>
  <img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white"/>
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</div>
