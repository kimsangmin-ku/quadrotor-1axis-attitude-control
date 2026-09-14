# firmware

Nucleo-F446RE 용 PlatformIO 프로젝트가 이 폴더에 들어갑니다.

VS Code → PlatformIO → New Project 에서
- Board: ST Nucleo F446RE
- Framework: Mbed (수업 환경과 동일) 또는 STM32Cube
- Location: 이 폴더(`firmware`) 선택

예정 구조
```
firmware/
├── platformio.ini
├── src/
│   ├── main.cpp        제어 루프 (100 Hz)
│   ├── imu.cpp/.h      MPU-6050 I2C 읽기
│   ├── filter.cpp/.h   상보필터
│   ├── pid.cpp/.h      PID 제어기
│   └── logger.cpp/.h   UART CSV 로깅
└── docs/wiring.md      배선도
```
