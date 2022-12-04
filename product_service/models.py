import mongoengine
import logging
from pymongo import monitoring

log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class CommandLogger(monitoring.CommandListener):

    def started(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} started on server "
                  "{0.connection_id}".format(event))

    def succeeded(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "succeeded in {0.duration_micros} "
                  "microseconds".format(event))

    def failed(self, event):
        log.debug("Command {0.command_name} with request id "
                  "{0.request_id} on server {0.connection_id} "
                  "failed in {0.duration_micros} "
                  "microseconds".format(event))


monitoring.register(CommandLogger())


class Product(mongoengine.Document):
    meta = {
        'db_alias': 'mydb',
        'collection': 'products',
    }

    product_uuid = mongoengine.UUIDField(primary_key=True)
    name = mongoengine.StringField(max_length=200, required=True)
    description = mongoengine.StringField(max_length=200, required=True)
    price = mongoengine.IntField(required=True)
