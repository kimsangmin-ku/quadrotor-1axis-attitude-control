// MPU-6050 (I2C) 최소 드라이버 - 원시값 읽기 전용
#pragma once
#include "mbed.h"

struct ImuRaw {
    int16_t ax, ay, az;   // 가속도 원시값 (±4g 설정 시 8192 LSB/g)
    int16_t gx, gy, gz;   // 자이로 원시값 (±500 dps 설정 시 65.5 LSB/(°/s))
    int16_t temp;         // 온도 원시값 (temp/340 + 36.53 = °C)
};

class Mpu6050 {
public:
    static constexpr int   ADDR_8BIT   = 0x68 << 1;   // AD0=GND → 0x68
    static constexpr int   ACC_LSB_G   = 8192;        // AFS_SEL=1 (±4g)
    static constexpr int   GYRO_LSB_DPS10 = 655;      // FS_SEL=1 (±500 dps): 65.5 LSB/dps ×10

    Mpu6050(PinName sda, PinName scl);

    // 센서 깨우고 레인지·DLPF 설정. WHO_AM_I가 0x68이면 true.
    bool init();
    uint8_t whoAmI();
    bool read(ImuRaw &out);
    int  lastErr() const { return _lastErr; }
    uint8_t id() const { return _whoAmI; }   // init()에서 읽은 WHO_AM_I (0x68=정품, 0x72 등=클론)   // 0=OK, 1=WHO_AM_I, 2=wake, 3~6=config, 7=still asleep

private:
    I2C _i2c;
    int _lastErr = -1;
    uint8_t _whoAmI = 0;
    bool writeReg(uint8_t reg, uint8_t val);
    bool readRegs(uint8_t reg, uint8_t *buf, int len);
};
