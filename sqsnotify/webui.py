from deluge.log import LOG as log
from deluge.ui.client import client
from deluge import component
from deluge.plugins.pluginbase import WebPluginBase

from common import get_resource

class WebUI(WebPluginBase):

    scripts = [get_resource("sqsnotify.js")]

    def enable(self):
        log.debug("SQSNotify Web plugin enabled!")

    def disable(self):
        log.debug("SQSNotify Web plugin disabled!")
