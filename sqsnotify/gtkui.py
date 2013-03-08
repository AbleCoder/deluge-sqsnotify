import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common
import deluge.configmanager

from common import get_resource

class GtkUI(GtkPluginBase):
    def enable(self):

        self.glade = gtk.glade.XML(get_resource("config.glade"))

        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)
        component.get("Preferences").add_page("SQSNotify", self.glade.get_widget("prefs_box"))

    def disable(self):

        component.get("Preferences").remove_page("SQSNotify")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    def on_show_prefs(self):

        client.sqsnotify.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, core_config):

        self.glade.get_widget("aws_connect_to_region").set_text(core_config["aws_connect_to_region"])
        self.glade.get_widget("aws_access_key_id").set_text(core_config["aws_access_key_id"])
        self.glade.get_widget("aws_secret_access_key").set_text(core_config["aws_secret_access_key"])
        self.glade.get_widget("on_added_queue").set_text(core_config["on_added_queue"])
        self.glade.get_widget("on_complete_queue").set_text(core_config["on_complete_queue"])

    def on_apply_prefs(self):

        core_config = {
            "aws_connect_to_region": self.glade.get_widget("aws_connect_to_region").get_text(),
            "aws_access_key_id": self.glade.get_widget("aws_access_key_id").get_text(),
            "aws_secret_access_key": self.glade.get_widget("aws_secret_access_key").get_text(),
            "on_added_queue": self.glade.get_widget("on_added_queue").get_text(),
            "on_complete_queue": self.glade.get_widget("on_complete_queue").get_text(),
        }

        client.sqsnotify.set_config(core_config)
