from twisted.internet import defer
from twisted.internet import reactor

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

import boto.sqs


DEFAULT_PREFS = {
    "aws_connect_to_region": "us-east-1",
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
    "on_added_queue": "",
    "on_added_msg_tpl": """
    {
        "EVENT": "__ADDED__"
        "name": "%(name)s",
        "num_files": "%(num_files)s"
    }
    """,
    "on_complete_queue": "",
    "on_complete_msg_tpl": """
    {
        "EVENT": "__COMPLETE__"
        "name": "%(name)s",
        "num_files": "%(num_files)s"
    }
    """,
}

class Core(CorePluginBase):

    def build_msg_body(self, torrent_id, msg_tpl):
        torrent        = component.get("TorrentManager")[torrent_id]
        torrent_status = torrent.get_status({})

        return msg_tpl % torrent_status

    def disable(self):
        log.debug("SQSNotify core plugin disabled!")

        event_manager = component.get("EventManager")
        event_manager.deregister_event_handler("TorrentFinishedEvent", self.on_torrent_finished)
        event_manager.deregister_event_handler("TorrentAddedEvent", self.on_torrent_added)

        self.config.save()

    def enable(self):
        self.config = deluge.configmanager.ConfigManager("sqsnotify.conf", DEFAULT_PREFS)

        event_manager = component.get("EventManager")
        event_manager.register_event_handler("TorrentFinishedEvent", self.on_torrent_finished)
        event_manager.register_event_handler("TorrentAddedEvent", self.on_torrent_added)

        log.debug("SQSNotify core plugin enabled!")

    def get_sqs_queue(self, queue_name):
        # TODO: test if we should cache queue objects
        return self.sqs_conn.get_queue(queue_name)

    def on_torrent_added(self, torrent_id):
        self.on_torrent_event(
                torrent_id,
                self.config['on_added_queue'],
                self.config['on_added_msg_tpl'])

    def on_torrent_event(self, torrent_id, sqs_queue_name, msg_tpl):
	if self.config["aws_connect_to_region"].strip() == "":
            return

	if self.config["aws_access_key_id"].strip() == "":
            return

	if self.config["aws_secret_access_key"].strip() == "":
            return

        # setup sqs connection
        self.sqs_conn = boto.sqs.connect_to_region(
                self.config['aws_connect_to_region'],
                aws_access_key_id=self.config['aws_access_key_id'],
                aws_secret_access_key=self.config['aws_secret_access_key'])

        if (sqs_queue_name.strip() == ""):
            return

        try:
            msg_body = self.build_msg_body(torrent_id, msg_tpl)

            self.send_msg(sqs_queue_name, msg_body)

        except Exception, e:
            log.error("SQSNotify error %s" % e)

    def on_torrent_finished(self, torrent_id):
        self.on_torrent_event(
                torrent_id,
                self.config['on_complete_queue'],
                self.config['on_complete_msg_tpl'])

    def send_msg(self, sqs_queue_name, msg_body):
        msg = boto.sqs.message.Message()
        msg.set_body(msg_body)

        sqs_q  = self.get_sqs_queue(sqs_queue_name)
        status = sqs_q.write(msg)

    def update(self):
        pass

    ### Exported RPC methods ###
    @export
    def set_config(self, config):
        log.debug("saving config: %s" % config)
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        log.debug("sending config: %s" % self.config.config)
        return self.config.config
