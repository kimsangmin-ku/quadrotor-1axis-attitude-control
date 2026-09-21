// firmware/src/main.cpp
// 1단계: 보드 생존 확인 - LED 점멸 + 시리얼 출력
// 이후 단계에서 imu / filter / pid / logger 모듈로 확장한다.

#include "mbed.h"

static DigitalOut led(LED1);                     // Nucleo 온보드 LD2 (PA_5)
static BufferedSerial pc(USBTX, USBRX, 115200);  // ST-LINK 가상 COM 포트

int main()
{
    const char banner[] = "\r\n[quadrotor-1axis] Nucleo-F446RE alive\r\n";
    pc.write(banner, sizeof(banner) - 1);

    Timer t;
    t.start();
    uint32_t count = 0;

    while (true) {
        led = !led;

        char line[64];
        int n = snprintf(line, sizeof(line), "tick %lu  t=%lld ms\r\n",
                         (unsigned long)count++,
                         (long long)t.elapsed_time().count() / 1000);
        pc.write(line, n);

        ThisThread::sleep_for(500ms);
    }
}
