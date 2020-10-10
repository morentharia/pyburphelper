import trio
import httpx
from furl import furl

from pyburphelper import burp_log, tail_f_burp_log

HTTP_PROXY = "http://localhost:8080"
BURP_LOG_FILE = '/tmp/burp_requests.log'


async def main():
    to_resend_list = []

    for row in burp_log(BURP_LOG_FILE):
        if "XXX" in dict(row.request.headers):
            continue

        if all(h not in row.request.addr for h in ["mail.ru", "ok.ru"]):
            continue

        f = furl(row.request.url)
        f.add({'come': "to daddy 1"})
        f.add({'come': "to daddy 2"})
        f.path.segments =f.path.segments[:1] + ["come", "to", "daddy"] + f.path.segments[1:]
        row.request.url = f.url
        row.request.headers.append(('XXX', "come to daddy"))

        print(row.request.url)
        to_resend_list.append(row.request)

    limit = trio.CapacityLimiter(20)

    async def fetch(method, url, content, headers):
        try:
            res = await client.request(req.method,
                                       req.url,
                                       content=req.body,
                                       headers=headers,
                                       timeout=30,
                                       allow_redirects=False)
            print(f"{req.method:8} {req.url} [{res.status_code}]")
        except httpx.ReadTimeout:
            print(f"{req.method:8} {req.url} [ timeout -1 ]")

    async with httpx.AsyncClient(proxies=httpx.Proxy(url=HTTP_PROXY), verify=False) as client:
        async with trio.open_nursery() as nursery:
            for req in to_resend_list:
                async with limit:
                    headers = dict(req.headers)
                    headers.pop('Content-Length', None)
                    nursery.start_soon(fetch, req.method, req.url, req.body, headers)

if __name__ == "__main__":
    trio.run(main)
    print("__the_end__")
