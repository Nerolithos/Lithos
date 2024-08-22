# [ch3]完成 commits 数据库建立

补充胡乱记笔记导致的探索过程记录的空缺

注：“后续”中尚留有未解决的问题(240822)

## 日志

240818   试图将所有 issues 数据以 json 全抄到本地，但没有仔细读原文，屡次报错，[JSON 原文件](https://postimg.cc/cvTDZ5mD)未经过格式化处理是难以理解的。

240819   用[JSON Editor Online](https://jsoneditoronline.org)处理过之后：[以我 ch2 的 issue 为例](https://postimg.cc/mPf5w5Zk)，会发现作为每一篇 issue 字典里的属性 “assignee” 和 “author” 本身套着又一个字典。决定建立两个数据库，现在取出其中用户 ID 作为指针数据，放在“issues”数据库，指向另外一个数据库“users”，其中另行显示用户信息。这样节省空间且结构清晰。**对于ch3, comments的数据结构与 author 类似。**

240820   [SQLite database](https://postimg.cc/nCydLJKh)建立，但尚未研究对它检索或总结的功能。

240822   继续拉 commits 数据，[project_ID](https://gitlab.com/101camp/7py/tasks/edit) 我以前一直编程序让 gitlab 返还给我，结果 UI 界面上可以直接找到。发现 curl 不能直接用 f-string ，虽然无关紧要。最后修改完 run 时报错：

```shell
(base) ➜  lpthw python commits.py
Saved commit data for branch: LPTHW
Saved commit data for branch: byakunine
Saved commit data for branch: dama
Saved commit data for branch: hll101
Saved commit data for branch: jiaqili
Saved commit data for branch: kittypang
Saved commit data for branch: liyuxin
Saved commit data for branch: magico101
Saved commit data for branch: master
Saved commit data for branch: patch-1
Saved commit data for branch: py101
Traceback (most recent call last):
  File "/opt/anaconda3/lib/python3.12/site-packages/urllib3/connectionpool.py", line 775, in urlopen
    self._prepare_proxy(conn)
  File "/opt/anaconda3/lib/python3.12/site-packages/urllib3/connectionpool.py", line 1044, in _prepare_proxy
    conn.connect()
  File "/opt/anaconda3/lib/python3.12/site-packages/urllib3/connection.py", line 632, in connect
    self._tunnel()  # type: ignore[attr-defined]
    ^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/http/client.py", line 979, in _tunnel
    raise OSError(f"Tunnel connection failed: {code} {message.strip()}")
OSError: Tunnel connection failed: 408 Request Time-out

The above exception was the direct cause of the following exception:

urllib3.exceptions.ProxyError: ('Unable to connect to proxy', OSError('Tunnel connection failed: 408 Request Time-out'))

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/adapters.py", line 589, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/urllib3/connectionpool.py", line 843, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/urllib3/util/retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='gitlab.com', port=443): Max retries exceeded with url: /api/v4/projects/17730311/repository/commits?ref_name=sunnyseed (Caused by ProxyError('Unable to connect to proxy', OSError('Tunnel connection failed: 408 Request Time-out')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/Lithos/Documents/lpthw/commits.py", line 24, in <module>
    response_commits = requests.get(url_commits, headers=headers)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/requests/adapters.py", line 616, in send
    raise ProxyError(e, request=request)
requests.exceptions.ProxyError: HTTPSConnectionPool(host='gitlab.com', port=443): Max retries exceeded with url: /api/v4/projects/17730311/repository/commits?ref_name=sunnyseed (Caused by ProxyError('Unable to connect to proxy', OSError('Tunnel connection failed: 408 Request Time-out')))
```

上面摧枯拉朽的一大段终端的倒苦水其实主要就是两点：**os 报了 408 Request Time-out 以及 requests 报了 proxyerror。**
修改方案：修改参数——延长响应时间或者禁用代理(分开来各试了一次)：

```shell
response_commits = requests.get(url_commits, headers = headers, timeout = 30, proxies = {})
```

结果报错来的更快，连前几个原本保存的了的分支数据也408了,同时出现新报错：
```shell
(base) ➜  lpthw python commits.py
Traceback (most recent call last):
  File "/Users/Lithos/Documents/lpthw/commits.py", line 73, in <module>
    with open(f"branches_commits/{branch_name}_commits.json", "w") as file:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'branches_commits/LPTHW_commits.json'
```

修改方案(改)：直接用`proxies = { "http": None,  "https": None,}`，简单粗暴的禁止 proxy,  并增加检查确保目录存在：

```shell
import os
if not os.path.exists("branches_commits"):
    os.makedirs("branches_commits")
```

最后发现两个修改都是需要的，成功复制下来了18个分支上所有的 commit 数据并保存到本地数据库。不过，我还是不理解为什么要禁用proxy。

## 后续
未解决的问题：
为什么会需要禁用PROXY？代理服务器是什么？为什么代理服务器和VPN经常傻傻分不清(这个问题又偏离主题了……)?
