import logging
import subprocess

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import template
from homeassistant.exceptions import TemplateError

DOMAIN = 'templated_shell_command'

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

SHELL_COMMAND_SCHEMA = vol.Schema({})


def setup(hass, config):
    """Setup the shell_command component."""
    conf = config.get(DOMAIN, {})

    def service_handler(call):
        """Execute a shell command service."""
        try:
            cmd = template.render(hass, conf[call.service])
            subprocess.call(cmd, shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        except TemplateError as ex:
            if ex.args and ex.args[0].startswith("UndefinedError: 'None' has no attribute"):
                # Common during HA startup - so just a warning
                _LOGGER.warning(ex)
                return
            _LOGGER.error(ex)
        except subprocess.SubprocessError:
            _LOGGER.exception('Error running command')

    for name in conf.keys():
        hass.services.register(DOMAIN, name, service_handler,
                               schema=SHELL_COMMAND_SCHEMA)
    return True
