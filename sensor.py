# encoding: utf-8

""" @exlab247@gmail.com
Công cụ [covid19] hiển thị thông tin về tình hình dịch Coronavirus COVID-19 ở Việt Nam, Trung Quốc và thế giới, số liệu cập nhật theo Bộ Y tế Việt Nam. 
Version 1.0 09 Mar 2020
Version 2.0 14 Apr 2020, remove type TQ, add content of notification.

# [your_config]/custom_components/covid19
.homeassistant/
|-- custom_components/
|   |-- covid19/
|       |-- __init__.py
|       |-- sensor.py
|       |-- manifest.json

# Config in configuration.yaml file for Home Assistant
sensor:
  - platform: covid19
    display_options:
      - "VN"
      - "QT"
"""
import datetime
import logging
from . import coronavirus

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_RESOURCES, CONF_TYPE, CONF_SCAN_INTERVAL
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=300)   # 5 minutes

SENSOR_TYPES = {
    'VN': ['Việt Nam', 'mdi:account-search'],
    'TG': ['Thế giới', 'mdi:account-search'],
}
DEFAULT_TYPE_ = 'VN'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_RESOURCES, default={CONF_TYPE: DEFAULT_TYPE_}):
        vol.All(cv.ensure_list, [vol.Schema({
            vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
        })])
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the system monitor sensors."""
    dev = []
    for resource in config[CONF_RESOURCES]:
        dev.append(convid19_class(resource[CONF_TYPE]))

    add_entities(dev, True)

class convid19_class(Entity):

    def __init__(self, sensor_type):
        self._name = SENSOR_TYPES[sensor_type][0]
        self.type = sensor_type
        self._state = None
        self._author = 'exlab247@gmail.com'
        self._thongbaoVN = None
        self._thongbaoQT = None
        self.update()

    @property
    def name(self):
        return self._name.rstrip()

    @property
    def state(self):
        return self._state
		
    @property
    def icon(self):
        """Return the icon of the sensor"""
        return SENSOR_TYPES[self.type][1]
		
    @property
    def device_state_attributes(self):
        return {'thongbaoVN': self._thongbaoVN,'thongbaoQT': self._thongbaoQT,'Tác giả': self._author}

    @Throttle(SCAN_INTERVAL)
    def update(self):
        data_ncov = coronavirus.ncov.get()
        data_vn = data_ncov[0]
        data_qt = data_ncov[1]
        self._thongbaoVN = "Thông tin dịch Covid 19, Việt Nam số ca nhiễm: " + str(data_vn[0]).replace(".","") + " người, đang điều trị: " + str(data_vn[1]).replace(".","") + " người, khỏi bệnh: " + str(data_vn[2]).replace(".","") + " người, tử vong: " + str(data_vn[3]).replace(".","") + " người."
        self._thongbaoQT = "Thông tin dịch Covid 19, Thế giới số ca nhiễm: " + str(data_qt[0]).replace(".","") + " người, đang nhiễm: " + str(data_qt[1]).replace(".","") + " người, khỏi bệnh: " + str(data_qt[2]).replace(".","") + " người, tử vong: " + str(data_qt[3]).replace(".","") + " người."
        if self.type == 'VN':
            self._state = " - ".join(data_vn).replace(".",",")
        elif self.type == 'TG':
            self._state = " - ".join(data_qt).replace(".",",")
                        
        


