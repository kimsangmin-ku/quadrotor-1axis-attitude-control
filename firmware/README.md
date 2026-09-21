# firmware

개인 소유 **STM32 Nucleo-F446RE** 용 PlatformIO 프로젝트.
항공우주종합설계 수업의 LPC1768 프로젝트와는 폴더·플랫폼(`ststm32` vs `nxplpc`)·코드 모두 별개이며,
수업 코드를 복사하지 않고 처음부터 작성한다.

## 빌드·업로드

1. VS Code에서 **이 저장소 루트가 아니라 `firmware` 폴더**를 연다 (File → Open Folder).
2. Nucleo를 ST-LINK 쪽 USB(보드 위쪽)로 PC에 연결한다. 수업 보드는 동시에 꽂지 않는다.
3. PlatformIO 상태바의 → (Upload) 클릭. 첫 빌드는 mbed 라이브러리를 받느라 수 분 걸린다.
4. 플러그 아이콘 (Serial Monitor) 클릭. 115200 bps.

성공 기준: 초록 LED(LD2)가 0.5초마다 깜빡이고, 모니터에 `tick N  t=... ms` 가 흐른다.

## 구조 (예정)

```
firmware/
├── platformio.ini
├── src/
│   ├── main.cpp        제어 루프 (100 Hz)          ← 현재: LED + 시리얼 생존 확인
│   ├── imu.cpp/.h      MPU-6050 I2C 읽기
│   ├── filter.cpp/.h   상보필터
│   ├── pid.cpp/.h      PID 제어기
│   └── logger.cpp/.h   UART CSV 로깅
└── docs/wiring.md      배선도
```

## 진행

- [x] platformio.ini + main.cpp 생성 (2026-09-21)
- [x] 보드 업로드·시리얼 출력 확인 (2026-09-21, mbed 드라이브 복사 방식)
- [x] MPU-6050 읽기 (2026-09-21, 클론 칩 WHO_AM_I=0x72)
- [ ] 상보필터 roll 각도 추정
