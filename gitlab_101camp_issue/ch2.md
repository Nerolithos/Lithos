# [ch2] [note] 字典与列表，JSON 格式

## 现象
ch2 中有一系列关于 issues 的 task，与之前几课不同的是，收到的信息需要合理保存到本地以便能随时从本地加载展开统计分析。以下是截止到获取所有 issues 并解析为 JSON 的命令行：

```shell
import requests
import json
from urllib.parse import quote
import pprint
GITLAB_URL = "https://gitlab.com"
PROJECT_PATH = "101camp/7py/tasks"
ACCESS_TOKEN = "......"  

ENCODED_PROJECT_PATH = quote(PROJECT_PATH, safe='')

issues_url = f"{GITLAB_URL}/api/v4/projects/{ENCODED_PROJECT_PATH}/issues?per_page=100"

headers = {
    "PRIVATE-TOKEN": ACCESS_TOKEN
}

response = requests.get(issues_url, headers=headers)
issues = response.json()
```

以上程序没有bug。接下来的程序过长，我简单描述一下，我为收集到的数据建了个列表，把字典的各类属性各自提取出来并储存，然后再运行时就报错：

```shell
typeError: string indices must be integers, not 'str'
```
(“字符串函数的索引必须是整数，而非字符串。”)

## 分析
结论很简单，没必要为数据建列表，**因为字典本身就被列表套着，而新建一层列表导致我使用字典的索引去操作一个列表，于是便报错。**

获取的关于 issues 的数据是 JSON 语法写的，基本格式是许多 dict(字典) 并列在 list(列表) 中，大致类似这样：**{[…], […], […], …}**。

这种默认格式在使用 REST API(此处为 URL地址 API) 返回多个资源时非常常见，这也符合我们讨论的情况（即读取 task 仓库下多个 issue 信息。）

通常，当从 GitLab 获取数据时，如果请求的是单个资源（例如，一个具体的 issue、一个具体的用户），API 返回的数据会是一个字典，以我学 ch1 时发的 issue 为例，API返回的数据是：

```shell
{"id":150755915,"iid":106,"project_id":17730311,"title":"[ch1][note]创造编程环境，anaconda3 的屡次报错","description":"240801\n在后记中我留下了问题......}
```

也就是一个含有关于这个 issue 的所有角度的描述信息的字典，清晰地表示单个资源的所有属性，很方便调用和整理。

那也就不难理解，当我们请求多个 issue 的信息，返回多个字典时，默认用列表囊括它们是合理的。所以，直接继续运行以下命令行即可：

```shell
for issue in issues:
    issue_id = issue['id']
    issue_title = issue['title']
    issue_author = issue['author']['username']
    issue_comments_count = issue['user_notes_count']
......
```
(基础的字典索引，历遍所有字典。)

## 建议
**print(type(issues))** 可以查看当前数据格式是str, list, dict, tuple 还是啥的。

代码一定要写一段 run 一段。如果一定要为大段代码手工 debug ，那也要逐个排除可能的出错段。

在线 JSON： [edit JSON, format JSON, query JSON](https://jsoneditoronline.org/)

## Reference
1、《Learn Python3 the Hard Way》(2018) (Zed A.Shaw) Lesson 39
2、https://stackoverflow.com/questions/6077675/why-am-i-seeing-typeerror-string-indices-must-be-integers

