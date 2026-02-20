from esphome import automation
from esphome.automation import maybe_simple_id
import esphome.codegen as cg
from esphome.components import modbus, sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    ICON_CURRENT_AC,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_VOLT,
    UNIT_WATT,
    UNIT_WATT_HOURS,
)

CONF_PV_VOLTAGE = 'pv_voltage'
CONF_BATTERY_VOLTAGE = 'battery_voltage'
CONF_CHARGING_CURRENT = 'charging_current'
CONF_TOTAL_ENERGY = 'total_energy'
CONF_CHARGING_POWER = 'charging_power'
CONF_INTERNAL_TEMPERATURE = 'internal_temperature'
CONF_EXTERNAL_TEMPERATURE = 'external_temperature'

ICON_TEMPERATURE = "mdi:thermometer"

AUTO_LOAD = ["modbus"]

mly_mppt_ch_ns = cg.esphome_ns.namespace("mly_mppt_ch")
MLY_MPPT_CH = mly_mppt_ch_ns.class_("MLY_MPPT_CH", cg.PollingComponent, modbus.ModbusDevice)

# Actions
ResetEnergyAction = mly_mppt_ch_ns.class_("ResetEnergyAction", automation.Action)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(MLY_MPPT_CH),
            cv.Optional(CONF_PV_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CHARGING_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CHARGING_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TOTAL_ENERGY): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT_HOURS,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_INTERNAL_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_TEMPERATURE,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_EXTERNAL_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_TEMPERATURE,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(modbus.modbus_device_schema(0x09))
)


@automation.register_action(
    "mly_mppt_ch.reset_energy",
    ResetEnergyAction,
    maybe_simple_id(
        {
            cv.Required(CONF_ID): cv.use_id(MLY_MPPT_CH),
        }
    ),
)
async def reset_energy_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)

    if CONF_PV_VOLTAGE in config:
        conf = config[CONF_PV_VOLTAGE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_pv_voltage_sensor(sens))
    if CONF_BATTERY_VOLTAGE in config:
        conf = config[CONF_BATTERY_VOLTAGE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_battery_voltage_sensor(sens))
    if CONF_CHARGING_CURRENT in config:
        conf = config[CONF_CHARGING_CURRENT]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_charging_current_sensor(sens))
    if CONF_CHARGING_POWER in config:
        conf = config[CONF_CHARGING_POWER]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_charging_power_sensor(sens))
    if CONF_TOTAL_ENERGY in config:
        conf = config[CONF_TOTAL_ENERGY]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_total_energy_sensor(sens))
    if CONF_INTERNAL_TEMPERATURE in config:
        conf = config[CONF_INTERNAL_TEMPERATURE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_internal_temperature_sensor(sens))
    if CONF_EXTERNAL_TEMPERATURE in config:
        conf = config[CONF_EXTERNAL_TEMPERATURE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_external_temperature_sensor(sens))

