#pragma once

#include "esphome/core/automation.h"
#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/modbus/modbus.h"

#include <vector>

namespace esphome {
namespace mly_mppt_ch {


class MLY_MPPT_CH : public PollingComponent, public modbus::ModbusDevice {
 public:
  void set_pv_voltage_sensor(sensor::Sensor *pv_voltage_sensor) { pv_voltage_sensor_ = pv_voltage_sensor; }
  void set_battery_voltage_sensor(sensor::Sensor *battery_voltage_sensor) { battery_voltage_sensor_ = battery_voltage_sensor; }
  void set_charging_current_sensor(sensor::Sensor *charging_current_sensor) { charging_current_sensor_ = charging_current_sensor; }
  void set_charging_power_sensor(sensor::Sensor *charging_power_sensor) { charging_power_sensor_ = charging_power_sensor; }
  void set_total_energy_sensor(sensor::Sensor *total_energy_sensor) { total_energy_sensor_ = total_energy_sensor; }
  void set_internal_temperature_sensor(sensor::Sensor *internal_temperature_sensor) { internal_temperature_sensor_ = internal_temperature_sensor; }
  void set_external_temperature_sensor(sensor::Sensor *external_temperature_sensor) { external_temperature_sensor_ = external_temperature_sensor; }

  void update() override;

  void on_modbus_data(const std::vector<uint8_t> &data) override;

  void dump_config() override;

 protected:
  sensor::Sensor *pv_voltage_sensor_{nullptr};
  sensor::Sensor *battery_voltage_sensor_{nullptr};
  sensor::Sensor *charging_current_sensor_{nullptr};
  sensor::Sensor *charging_power_sensor_{nullptr};
  sensor::Sensor *total_energy_sensor_{nullptr};
  sensor::Sensor *internal_temperature_sensor_{nullptr};
  sensor::Sensor *external_temperature_sensor_{nullptr};

  void reset_energy_();
};

}  // namespace MLY_MPPT_CH
}  // namespace esphome
