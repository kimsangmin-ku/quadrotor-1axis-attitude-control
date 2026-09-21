#include "imu.h"

namespace {
    constexpr uint8_t REG_SMPLRT_DIV   = 0x19;
    constexpr uint8_t REG_CONFIG       = 0x1A;
    constexpr uint8_t REG_GYRO_CONFIG  = 0x1B;
    constexpr uint8_t REG_ACCEL_CONFIG = 0x1C;
    constexpr uint8_t REG_ACCEL_XOUT_H = 0x3B;
    constexpr uint8_t REG_PWR_MGMT_1   = 0x6B;
    constexpr uint8_t REG_WHO_AM_I     = 0x75;
}

Mpu6050::Mpu6050(PinName sda, PinName scl) : _i2c(sda, scl)
{
    _i2c.frequency(100000);   // 100 kHz (점퍼선 배선에서 안정적)
}

bool Mpu6050::writeReg(uint8_t reg, uint8_t val)
{
    char buf[2] = { (char)reg, (char)val };
    return _i2c.write(ADDR_8BIT, buf, 2) == 0;
}

bool Mpu6050::readRegs(uint8_t reg, uint8_t *buf, int len)
{
    char r = (char)reg;
    if (_i2c.write(ADDR_8BIT, &r, 1, true) != 0) return false;   // repeated start
    return _i2c.read(ADDR_8BIT, (char *)buf, len) == 0;
}

uint8_t Mpu6050::whoAmI()
{
    uint8_t v = 0;
    readRegs(REG_WHO_AM_I, &v, 1);
    return v;
}

bool Mpu6050::init()
{
    // 1) 먼저 살아있는지 확인
    //    정품 MPU-6050은 0x68. 시중 GY-521 클론 칩은 0x70/0x72/0x98 등을 돌려주지만
    //    레지스터 맵이 같아 동일하게 동작하므로 "응답이 있으면" 통과시킨다.
    uint8_t id = whoAmI();
    if (id == 0x00 || id == 0xFF) { _lastErr = 1; return false; }
    _whoAmI = id;

    // 2) 슬립 해제 (리셋은 생략 - 전원 인가 시 기본값이면 충분)
    if (!writeReg(REG_PWR_MGMT_1, 0x01)) { _lastErr = 2; return false; }   // 클럭 = X 자이로 PLL
    ThisThread::sleep_for(10ms);

    // 3) 설정 (하나라도 실패하면 단계 번호 기록)
    if (!writeReg(REG_SMPLRT_DIV, 0x04))   { _lastErr = 3; return false; }  // 200 Hz
    if (!writeReg(REG_CONFIG, 0x03))       { _lastErr = 4; return false; }  // DLPF 44 Hz
    if (!writeReg(REG_GYRO_CONFIG, 0x08))  { _lastErr = 5; return false; }  // ±500 dps
    if (!writeReg(REG_ACCEL_CONFIG, 0x08)) { _lastErr = 6; return false; }  // ±4 g

    // 4) 설정이 실제로 들어갔는지 읽어서 확인
    uint8_t v = 0;
    if (!readRegs(REG_PWR_MGMT_1, &v, 1) || (v & 0x40)) { _lastErr = 7; return false; } // 아직 슬립?
    _lastErr = 0;
    return true;
}

bool Mpu6050::read(ImuRaw &o)
{
    uint8_t b[14];
    if (!readRegs(REG_ACCEL_XOUT_H, b, 14)) return false;
    o.ax   = (int16_t)((b[0] << 8) | b[1]);
    o.ay   = (int16_t)((b[2] << 8) | b[3]);
    o.az   = (int16_t)((b[4] << 8) | b[5]);
    o.temp = (int16_t)((b[6] << 8) | b[7]);
    o.gx   = (int16_t)((b[8] << 8) | b[9]);
    o.gy   = (int16_t)((b[10] << 8) | b[11]);
    o.gz   = (int16_t)((b[12] << 8) | b[13]);
    return true;
}
