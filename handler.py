"""
A override HTTPHandler of original HTTPHandler.
This can format record message with args, so message can be more friendly.
"""
import logging


class HTTPHandler(logging.handlers.HTTPHandler):
    def mapLogRecord(self, record):
        record.msg = record.getMessage()
        return record.__dict__
