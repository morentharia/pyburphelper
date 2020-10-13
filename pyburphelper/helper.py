import re
from pprint import pformat
# from pprint import pprint as pp
import io
import logging
from dataclasses import dataclass

import tailer

from .request import Request
from .response import Response
from .burplogrecord import BurpLogRecord

logging.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

SEPARATOR = "======================================================\n"

class UnreadIter:
    def __init__(self, f):
        self._f = f
        self.__unread_lines = []

    def __next__(self):
        if self.__unread_lines:
            return self.__unread_lines.pop(0)
        return next(self._f)

    def __iter__(self):
        return self

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_f"), name)

    def readline(self):
        try:
            return next(self)
        except StopIteration:
            return ""

    def unreadline(self, *args):
        self.__unread_lines.extend(args)


def read_burp_log_gen(f):
    line_num = 1
    state, req, resp, r = None, [], [], BurpLogRecord(None, None, None, None, None)
    f = UnreadIter(f)
    while line := f.readline():
        try:
            logger.debug("%5d: [%8s] %s", line_num, state, line[:-1])
            line_num += 1

            if line == SEPARATOR:
                line1, line2 = f.readline(), f.readline()
                logger.debug("%5d: [        ] %s", line_num + 1, line1[:-1])
                logger.debug("%5d: [        ] %s", line_num + 2, line2[:-1])
                line_num += 2
                if not all([line1, line2]):
                    break

                if line2 == SEPARATOR:
                    try:
                        r.time, r.addr, r.ip  = re.split(r'\s+', line1[:-1], 2)
                        r.ip = r.ip[1:-1]
                    except:
                        f.unreadline(line1, line2)
                        line_num -= 2
                        raise

                    state, req, resp = 'request', [], []
                    continue

                f.unreadline(line1,line2)
                line_num -= 2

            if state == 'request':
                if line != SEPARATOR:
                    req.append(line)
                    continue

                r.request = Request.from_string(''.join(req))
                r.request.addr = r.addr

                state = 'response'

            elif state == 'response':
                if line != SEPARATOR:
                    resp.append(line)
                    continue

                r.response = Response.from_string(''.join(resp))
                yield r
                state, req, resp, r = None, [], [], BurpLogRecord(None, None, None, None, None)

        except Exception as e:
            logger.exception(e)
            logger.error(f"state    = {pformat(state)}")
            logger.error(f"request  = {pformat(''.join(req))}")
            logger.error(f"response = {pformat(''.join(resp))}")
            logger.error(f"file line: {line_num}")
            # yield r
            state, req, resp, r = None, [], [], BurpLogRecord(None, None, None, None, None)


def burp_log(filename):
    with open(filename) as f:
        yield from read_burp_log_gen(f)

def _tail_f(f):
    # TODO: rewrite with sh
    for l in tailer.follow(f):
        yield l + "\n"

def tail_f_burp_log(filename):
    with open(filename) as f:
        yield from read_burp_log_gen(_tail_f(f))
