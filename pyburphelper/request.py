import io
import re
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


@dataclass
class Request:
    _raw: str
    addr: str            # https://example.com:443
    method: str          # GET
    _path_and_query: str # /aaa/bbb?one=1&two=2#/zzz/lol
    protocol: str        # HTTP/1.1
    headers: list        # [("User-Agent", "me")]
    body:str             # ...

    @classmethod
    def from_string(cls, text):
        method, _path_and_query, protocol, headers, body = "", "", "", [], []
        with io.StringIO(text) as f:
            state='first'
            while line := f.readline():
                if state == 'first':
                    method, _path_and_query, protocol = re.split(r'\s+', line[:-1], 2)
                    state = 'headers'
                elif state == 'headers':
                    if line == "\n":
                        state = "body"
                        continue
                    headers.append(line[:-1].split(": ", 1))
                elif state == 'body':
                    body.append(line)
        return cls("https://---------UNKNOWN.ORG-----------:686",
                   text,
                   method,
                   _path_and_query,
                   protocol,
                   headers,
                   ''.join(body))

    def dump(self):
        res = f"{self.method} {self._path_and_query} {self.protocol}\r\n"
        for k, v in self.headers:
            res += f"{k}: {v}\r\n"
        res += "\r\n"
        res += self.body
        return res

    @property
    def url(self):
        return f"{self.addr}{self._path_and_query}"

    @url.setter
    def url(self, val):
        url_splited = urlsplit(val)
        self.addr = urlunsplit((
            url_splited.scheme,
            url_splited.netloc,
            '',
            '',
            '',
        ))
        self._path_and_query = urlunsplit((
            '',
            '',
            url_splited.path,
            url_splited.query,
            url_splited.fragment,
        ))
