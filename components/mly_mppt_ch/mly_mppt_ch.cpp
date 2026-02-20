#include "mly_mppt_ch.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mly_mppt_ch {

static const char *const TAG = "mly_mppt_ch";

static const uint8_t MPPT_CMD_READ_IN_REGISTERS = 0x03;
static const uint8_t MPPT_REGISTER_COUNT = 20;

void MLY_MPPT_CH::on_modbus_data(const std::vector<uint8_t> &data) {
  if (data.size() < 40) {
    ESP_LOGW(TAG, "Invalid size for MPPT!");
    return;
  }

  auto mppt_get_16bit = [&](size_t i) -> uint16_t {
    return (uint16_t(data[i + 0]) << 8) | (uint16_t(data[i + 1]) << 0);
  };
  auto mppt_get_32bit = [&](size_t i) -> uint32_t {
    return (uint32_t(mppt_get_16bit(i + 0)) << 16) | (uint32_t(mppt_get_16bit(i + 2)) << 0);
  };

  uint16_t raw_pv_voltage = mppt_get_16bit(22);
  float pv_voltage = raw_pv_voltage / 10.0f;

  uint16_t raw_bat_voltage = mppt_get_16bit(28);
  float bat_voltage = raw_bat_voltage / 10.0f;

  uint32_t raw_charg_current = mppt_get_16bit(26);
  float charg_current = raw_charg_current / 10.0f;

  float power = bat_voltage * charg_current;

  float power_generation = mppt_get_32bit(36);

  float in_temperature = mppt_get_16bit(32);
  float out_temperature = mppt_get_16bit(34);

  if (this->pv_voltage_sensor_ != nullptr)
    this->pv_voltage_sensor_->publish_state(pv_voltage);
    ESP_LOGD(TAG, "PV voltage: %.1f V", pv_voltage);
  if (this->battery_voltage_sensor_ != nullptr)
    this->battery_voltage_sensor_->publish_state(bat_voltage);
    ESP_LOGD(TAG, "Battery voltage: %.1f V", bat_voltage);
  if (this->charging_current_sensor_ != nullptr)
    this->charging_current_sensor_->publish_state(charg_current);
    ESP_LOGD(TAG, "Charging current: %.1f A", charg_current);
  if (this->charging_power_sensor_ != nullptr)
    this->charging_power_sensor_->publish_state(power);
    ESP_LOGD(TAG, "Charging power: %.1f W", power);
  if (this->total_energy_sensor_ != nullptr)
    this->total_energy_sensor_->publish_state(power_generation);
    ESP_LOGD(TAG, "Total energy: %.0f Wh", power_generation);
  if (this->internal_temperature_sensor_ != nullptr)
    this->internal_temperature_sensor_->publish_state(in_temperature);
    ESP_LOGD(TAG, "Internal temperature: %.0f °C", in_temperature);
  if (this->external_temperature_sensor_ != nullptr)
    this->external_temperature_sensor_->publish_state(out_temperature);
    ESP_LOGD(TAG, "External temperature: %.0f °C", out_temperature);
}

void MLY_MPPT_CH::update() { this->send(MPPT_CMD_READ_IN_REGISTERS, 0, MPPT_REGISTER_COUNT); }

void MLY_MPPT_CH::dump_config() {
  ESP_LOGCONFIG(TAG,
                "MLY_MPPT_CH:\n"
                "  Address: 0x%02X",
                this->address_);
  LOG_SENSOR("", "PV voltage", this->pv_voltage_sensor_);
  LOG_SENSOR("", "Battery voltage", this->battery_voltage_sensor_);
  LOG_SENSOR("", "Charging current", this->charging_current_sensor_);
  LOG_SENSOR("", "Charging power", this->charging_power_sensor_);
  LOG_SENSOR("", "Total energy", this->total_energy_sensor_);
  LOG_SENSOR("", "Internal temperature", this->internal_temperature_sensor_);
  LOG_SENSOR("", "External temperature", this->external_temperature_sensor_);
}

}  // namespace mly_mppt_ch
}  // namespace esphome
