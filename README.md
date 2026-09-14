# 1축 테스트벤치 기반 쿼드로터 자세 안정화 제어기 개발·검증

> Quadrotor 1-Axis Attitude Control — Test-Bench Design, Embedded PID Implementation & Model-Based Validation

건국대학교 기계항공공학부 4학년 개인 프로젝트 (2026-09 ~ 2026-12)
작성자: 김상민

---

## 1. 프로젝트 개요

F450 쿼드로터의 한 축(roll)만 회전하도록 고정하는 시소형 테스트 지그를 직접 설계·제작하고,
STM32 Nucleo 보드로 IMU 기반 자세 추정과 PID 제어기를 구현하여 수평 유지 성능을
정량적으로 시험·튜닝·검증하는 프로젝트입니다.

실제 비행 없이 벤치 시험만으로 **설계 → 임베디드 제어 → 데이터 기반 검증** 의 한 사이클을
혼자 끝까지 돌려보는 것이 목표입니다.

| 구분 | 내용 |
|---|---|
| 기체 | F450 프레임 (팔 2개 사용), 2212 920KV 모터 ×2, 30A ESC ×2, 8045 프로펠러 |
| 제어기 | STM32 Nucleo-F446RE, PlatformIO (Mbed / STM32 HAL) |
| 센서 | MPU-6050 IMU (I2C) |
| 전원 | 12V DC 파워서플라이 (벤치 시험용) |
| 설계 툴 | CATIA V5 (지그 3D 모델·2D 도면), 온라인 3D프린팅 출력 |
| 분석 툴 | Python (NumPy, Matplotlib) |

## 2. 시스템 구성

```
[MPU-6050 IMU] --I2C--> [Nucleo-F446RE] --PWM--> [ESC ×2] --> [모터 ×2]
                              |
                              +--UART--> [PC: 데이터 로깅 (CSV)] --> [Python 분석]
```

제어 루프: IMU 원시값 → 상보필터(roll 각도 추정) → PID → 좌/우 모터 PWM 차동 출력

## 3. 결과물 구성

| 층 | 산출물 | 위치 |
|---|---|---|
| 설계 | 지그 3D 모델(STEP), 2D 도면(PDF), BOM, 설계 근거서, 강성 손계산 | `cad/` |
| 제어 | 자세 추정 · PID 펌웨어, 배선도 | `firmware/` |
| 검증 | 게인별 스텝응답 데이터·그래프, 1축 모델 시뮬레이션 vs 실측 비교 | `analysis/` |
| 문서 | 계획서, 진행 기록, 사진·영상 | `docs/` |

## 4. 진행 현황

- [ ] 1주차 (9/15~) 요구사항 정의, 부품 발주
- [ ] 2주차 PlatformIO 환경 세팅, 1축 동역학 손계산
- [ ] 3~4주차 CATIA 지그 설계, 도면·BOM, 출력 발주, IMU 읽기
- [ ] 5주차 상보필터 roll 각도 추정
- [ ] 6주차 지그 조립, 모터 개루프 구동
- [ ] 7~8주차 PID 폐루프, 데이터 로깅, 1차 튜닝
- [ ] 9주차 게인별 스텝응답 비교 (최소 완료선)
- [ ] 10~11주차 1축 모델 시뮬레이션 vs 실측 비교
- [ ] 12주차 최종 문서화, 동작 영상

자세한 일정과 부품 목록은 [docs/project_plan.md](docs/project_plan.md) 참고.

## 5. 저장소 구조

```
├── firmware/      PlatformIO 프로젝트 (Nucleo-F446RE)
├── cad/           CATIA 원본, STEP, 도면 PDF, BOM
├── analysis/      Python 분석 스크립트, 대표 실험 데이터(CSV), 그래프
├── docs/
│   ├── project_plan.md   계획서
│   ├── images/           사진·그래프
│   └── data/             실험 로그 (대용량 raw 는 제외)
└── README.md
```

## 6. 빌드 방법

```
cd firmware
pio run                # 빌드
pio run -t upload      # Nucleo 보드에 업로드
pio device monitor -b 115200   # 시리얼 로그 확인
```

## 7. 결과 (진행하면서 채움)

- 스텝응답 비교표: (예정)
- 시뮬레이션 vs 실측 그래프: (예정)
- 동작 영상: (예정)
