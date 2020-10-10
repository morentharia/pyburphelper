import io
from dataclasses import dataclass
from pprint import pformat
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

@dataclass
class Response:
    raw: str
    status: str
    headers: dict
    body:str

    @classmethod
    def from_string(cls, text):
        status, headers, body = "", {}, []
        with io.StringIO(text) as f:
            state='first'
            while line := f.readline():
                if state == 'first':
                    try:
                        _, status, *_ = line[:-1].split(" ")
                        status = int(status)
                    except:
                        logger.error("error line -> %s ", pformat(line))
                        raise
                    state = 'headers'
                elif state == 'headers':
                    if  len(res := line[:-1].split(": ", 2)) == 2:
                        headers[res[0]] = res[1]
                    if line == "\n":
                        state = "body"
                elif state == 'body':
                    body.append(line)
        return cls(text, status, headers, ''.join(body))


