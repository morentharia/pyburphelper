# pyburphelper

pyburphelper 0.1

```bash
pip install git+https://github.com/morentharia/pyburphelper
```

![burp option](/img/burp_log_option.png)
```python
from pyburphelper import burp_log, tail_f_burp_log

for r in burp_log('/tmp/burp_requests.log'):
    print(r.request.url)
for r in tail_f_burp_log('/tmp/burp_requests.log'):
    print(r.time, r.request.url)
```
