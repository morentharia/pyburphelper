import io
from dataclasses import dataclass
from .request import Request
from .response import Response

@dataclass
class BurpLogRecord:
    time: str
    addr: str #TODO:remove me
    ip: str
    request: Request
    response: Response
