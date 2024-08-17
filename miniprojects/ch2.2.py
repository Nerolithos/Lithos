import requests
from urllib.parse import quote
import sqlite3

GITLAB_URL = "https://gitlab.com"
PROJECT_PATH = "101camp/7py/tasks"  
ACCESS_TOKEN = "......"  
ENCODED_PROJECT_PATH = quote(PROJECT_PATH, safe='')

# 构建 URL
issues_url = f"{GITLAB_URL}/api/v4/projects/{ENCODED_PROJECT_PATH}/issues?per_page=100"

headers = {
    "PRIVATE-TOKEN": ACCESS_TOKEN
}

response = requests.get(issues_url, headers=headers)

# 检查响应状态码
if response.status_code == 404:
    print("Error 404: Project not found. Please check the project path or your access token.")
    exit()
elif response.status_code != 200:
    print(f"Failed to fetch issues: {response.status_code}, {response.text}")
    exit()

'''
# 直接保存下载的 JSON 数据到本地
with open('issues_raw.json', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("Issue data has been saved to issues_raw.json")
'''

issues = response.json()

# 连接到 SQLite 数据库
conn = sqlite3.connect('issues.db')
cursor = conn.cursor()

# 创建表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY,
        iid INTEGER,
        project_id INTEGER,
        title TEXT,
        description TEXT,
        state TEXT,
        created_at TEXT,
        updated_at TEXT,
        labels TEXT,
        milestone TEXT,
        assignee INTEGER,
        author INTEGER,
        user_notes_count INTEGER,
        web_url TEXT
    )
''')

# 插入数据到表格中
for issue in issues:
    cursor.execute('''
        INSERT INTO issues (
            id, iid, project_id, title, description, state, created_at, updated_at,
            labels, milestone, assignee, author, user_notes_count, web_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        issue['id'], issue['iid'], issue['project_id'], issue['title'], issue['description'],
        issue['state'], issue['created_at'], issue['updated_at'], ','.join(issue['labels']),
        issue['milestone']['title'] if issue.get('milestone') else None,
        issue['assignee']['id'] if issue.get('assignee') else None,
        issue['author']['id'], issue['user_notes_count'], issue['web_url']
    ))

# 提交更改并关闭数据库连接
conn.commit()
conn.close()

print("Issue data has been saved to issues.db")