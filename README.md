# Dain Kil

### AI Engineer · NLP · Model Serving

**Language is my edge; ML and cloud are my tools.**  
I build AI end to end, from training models to serving them in production.

언어를 깊이 이해하는 것이 제 강점이고, 그 강점으로 AI를 만듭니다.  
데이터 구축부터 모델 학습, 클라우드 서빙까지 직접 해왔습니다.

---

## Featured Projects

| | Project | What | Highlight |
|:-:|---|---|---|
| 📜 | [**SJW Translator**](https://github.com/dainkil/sjw_traslator) | 인물 KB로 LLM 환각을 억제한 《승정원일기》 번역 시스템 | 인명 정확도 **90.4% → 97.1%** |
| ⚾ | [**KBO Pitch Command**](https://github.com/dainkil/kbo-pitch-command-prediction) | LG Aimers 9기 해커톤 · 투구 제구등급 예측 | 최종 Score **70.314 · 팀 최고** |
| 🕌 | [**ShariahGuard**](https://github.com/dainkil/sharia-guard) | 샤리아·할랄 컴플라이언스 탐지 Kafka MSA | 구독 모델별 **비동기 판정 + 감사 이력** |

---

### 📜 [SJW Translator](https://github.com/dainkil/sjw_traslator) | 인물 KB로 LLM 환각을 억제한 《승정원일기》 번역 시스템
> 한문 원문의 인명을 NER과 인물 지식베이스(KB)로 확정해 LLM에 주입하고,  
> 번역문에 올바르게 반영됐는지 매 응답 검증하는 번역 서빙 시스템

`2026.03 – 2026.09` · 4인 팀 · **담당: KB 구축 · 모델링 · 백엔드 · 모델 서빙**

```
원문 → NER(인명 위치) → KB 링킹(인물 확정) → 프롬프트에 인명 주입 → LLM 번역 → 품질 게이트(인명 반영 검증)
```

- 인조 연간 인물 2,690명 KB와 표기 변형 역색인(9,403키) 구축, 역색인 → 활동 시기 → 관직 3단계 엔티티 링킹
- NER 도메인 적응·파인튜닝, 인명 정확도 지표(ETS) 설계, 프롬프트 구성 요소별 통제 실험 (조건별 3회 반복 중앙값 판정)
- 추가 LLM 호출 없이 인명 반영을 판정하는 품질 게이트로 모든 응답에 VERIFIED / DEGRADED / REJECTED 등급 부여
- Spring Boot API/Worker + Redis Streams 비동기 큐, 체크포인트 기반 대량 번역 재개, 429 응답의 원인별 실패 분류
- NER을 ONNX INT8로 경량화해 GPU 없이 CPU만으로 서빙, Docker Compose · Kubernetes 배포

| 항목 | 기준 | 결과 |
|---|---|---|
| 인명 정확도 (ETS) | LLM 단독 90.4% | **97.1%** (인명 오류 10 → 3건) |
| 번역 품질 (chrF) | 37.90 | **40.32** (입력 토큰 −11.2%) |
| NER 추론 지연 (p50) | PyTorch 17.9ms | **8.3ms** (인명 재현율 100% 유지) |
| NER 모델 크기 | 709MB | **178MB** |
| 대량 번역 재개 | — | 강제 종료 후 재개 시 **중복 LLM 호출 0건** |

**Tech**  
`Python` `PyTorch` `ONNX Runtime` `Gemini API` `Java 21` `Spring Boot` `Spring AI` `Redis Streams` `PostgreSQL` `Docker` `Kubernetes`

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
**2022.03 ~ 2027.08 (재학)**

### SKALA | SK AX
**2026.07 ~ 2026.12**

- SK AX 주관 AI/SW 실무 인재 양성 과정 참여

### LG Aimers 9기 Phase 1 & 2 & 3 | (주)엘지경영개발원 AI연구원
**2026.06 ~ 2026.09**

- AI/ML 이론 교육 및 온라인 해커톤 참여

### LG Aimers LLM Compression
**2026.01 ~ 2026.02**

- 대규모 언어 모델 경량화(양자화 · 프루닝 · 지식 증류) 주제 심화 과정 이수

### BDA 데이터 분석 입문반 (통계)
**2025.03 ~ 2025.08**

- 통계 기반 데이터 분석 기초 과정 이수

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

## 💼 Experience

### 서울특별시 120다산콜센터재단 | 인턴
**2024.01 ~ 2024.02**

- 행정업무 보조, 아랍어 번역
- DeepL · Google Cloud · Kakao i 번역 API 비교 분석 및 보고서 작성

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

- **English** — OPIc IH (2026.08) · TOEIC Speaking AL (2024.12) · TOEIC 870 (2024.11)
- **Arabic**

---

## 🛠 Tech Stack

### AI · ML

<div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
  <img src="https://img.shields.io/badge/ONNX_Runtime-005CED?style=for-the-badge&logo=onnx&logoColor=white"/>
  <img src="https://img.shields.io/badge/LightGBM-02569B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini_API-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/>
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
