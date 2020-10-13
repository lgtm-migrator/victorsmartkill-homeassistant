"""Binary sensor platform for Victor Smart-Kill."""
from typing import Callable, Iterable, List, Optional

from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType

from custom_components.victorsmartkill.const import (
    ATTR_LAST_KILL_DATE,
    DOMAIN,
    ICON_CAPTURED,
)
from custom_components.victorsmartkill.entity import VictorSmartKillEntity


async def async_setup_entry(
    hass: HomeAssistantType,
    entry: ConfigEntry,
    async_add_entities: Callable[[Iterable[Entity], Optional[bool]], None],
) -> None:
    """Set up binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        VictorSmartKillBinarySensor(trap.id, coordinator) for trap in coordinator.data
    ]
    async_add_entities(entities, False)


class VictorSmartKillBinarySensor(VictorSmartKillEntity, BinarySensorDevice):
    """Victor Smart-Kill occupancy binary sensor class."""

    @property
    def _exclude_device_state_attributes(self) -> List[str]:
        return [ATTR_LAST_KILL_DATE]

    @property
    def _name_suffix(self) -> str:
        return "capture"

    @property
    def _unique_id_suffix(self) -> str:
        return "capture"

    @property
    def device_class(self) -> str:
        """Return the class of this binary_sensor."""
        return "occupancy"

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.trap.trapstatistics.kills_present > 0

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_CAPTURED
