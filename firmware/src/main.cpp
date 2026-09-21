// firmware/src/main.cpp
// 2단계: MPU-6050 I2C 읽기 - WHO_AM_I 확인 후 가속도·자이로 원시값을 10 Hz로 출력
//
// 배선 (Nucleo-F446RE Arduino 헤더 기준)
//   MPU-6050 VCC → 3.3V
//   MPU-6050 GND → GND
//   MPU-6050 SDA → D14 (PB_9)
//   MPU-6050 SCL → D15 (PB_8)
//   (AD0, INT, XDA, XCL은 비워둠)

#include "mbed.h"
#include "imu.h"

static DigitalOut led(LED1);
static BufferedSerial pc(USBTX, USBRX, 115200);
static Mpu6050 imu(I2C_SDA, I2C_SCL);   // = D14, D15

static void print(const char *s) { pc.write(s, strlen(s)); }

int main()
{
    char line[128];
    print("\r\n[quadrotor-1axis] stage 2: MPU-6050 raw read\r\n");

    // I2C 버스 스캔: 응답하는 주소를 전부 출력 (배선 진단용)
    {
        I2C bus(I2C_SDA, I2C_SCL);
        bus.frequency(100000);
        print("I2C scan: ");
        int found = 0;
        for (int a = 0x08; a < 0x78; a++) {
            char dummy = 0;
            if (bus.read(a << 1, &dummy, 1) == 0) {
                snprintf(line, sizeof(line), "0x%02X ", a);
                print(line);
                found++;
            }
        }
        if (found == 0) print("(none - check VCC/GND/SDA/SCL)");
        print("\r\n");
    }

    bool ok = imu.init();
    snprintf(line, sizeof(line), "WHO_AM_I = 0x%02X (%s)  init=%s (err %d)\r\n",
             imu.whoAmI(), imu.whoAmI() == 0x68 ? "MPU-6050" : "MPU-6050 clone",
             ok ? "OK" : "FAIL", imu.lastErr());
    print(line);

    Timer t;
    t.start();

    while (true) {
        led = !led;

        if (ok) {
            ImuRaw r;
            if (imu.read(r)) {
                // mbed 기본 printf는 %f 미지원 → 정수로 출력 (mg, 0.1 dps, 0.1 C)
                int ax = (int)(r.ax * 1000L / (long)Mpu6050::ACC_LSB_G);
                int ay = (int)(r.ay * 1000L / (long)Mpu6050::ACC_LSB_G);
                int az = (int)(r.az * 1000L / (long)Mpu6050::ACC_LSB_G);
                int gx = (int)(r.gx * 100L / Mpu6050::GYRO_LSB_DPS10);   // 0.1 dps 단위
                int gy = (int)(r.gy * 100L / Mpu6050::GYRO_LSB_DPS10);
                int gz = (int)(r.gz * 100L / Mpu6050::GYRO_LSB_DPS10);
                int tc = (int)(r.temp * 10L / 340 + 365);
                snprintf(line, sizeof(line),
                         "t=%6lld ms  acc[mg] %+5d %+5d %+5d  gyro[0.1dps] %+5d %+5d %+5d  T=%d.%dC\r\n",
                         (long long)t.elapsed_time().count() / 1000,
                         ax, ay, az, gx, gy, gz, tc / 10, tc % 10);
            } else {
                snprintf(line, sizeof(line), "read fail\r\n");
            }
        } else {
            ok = imu.init();
            snprintf(line, sizeof(line), "IMU init retry: %s (err %d)\r\n",
                     ok ? "OK" : "FAIL", imu.lastErr());
        }
        print(line);

        ThisThread::sleep_for(100ms);   // 10 Hz 출력 (확인용)
    }
}
