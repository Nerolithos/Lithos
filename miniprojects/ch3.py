'''
import requests
import os

# 设置 API URL 和请求头
headers = {
    "PRIVATE-TOKEN": "......"
}

# 获取所有分支信息
url_branches = "https://gitlab.com/api/v4/projects/....../repository/branches" # Your Project ID
response_branches = requests.get(url_branches, headers = headers)

if response_branches.status_code == 200:
    branches = response_branches.json()
else:
    print(f"Failed to retrieve branches: {response_branches.status_code}")
    exit()

# 为每个分支获取提交数据
for branch in branches:
    branch_name = branch['name']
    url_commits = f"https://gitlab.com/api/v4/projects/....../repository/commits?ref_name={branch_name}"
    response_commits = requests.get(url_commits, headers = headers, timeout = 60)

    if response_commits.status_code == 200:
        commits_data = response_commits.json()
        
        # 创建分支文件夹以保存提交信息
        if not os.path.exists("branches_commits"):
            os.makedirs("branches_commits")

        # 保存提交信息到文件
        with open(f"branches_commits/{branch_name}_commits.json", "w") as file:
            file.write(response_commits.text)
        
        print(f"Saved commit data for branch: {branch_name}")
    else:
        print(f"Failed to retrieve commits for branch {branch_name}: {response_commits.status_code}")

'''










import requests

# 设置 API URL 和请求头
headers = {
    "PRIVATE-TOKEN": "......"
}

# 确保禁用代理
proxies = {
    "http": None,
    "https": None,
}

# 获取所有分支信息
url_branches = "https://gitlab.com/api/v4/projects/....../repository/branches"
response_branches = requests.get(url_branches, headers=headers, proxies=proxies, timeout=60)

if response_branches.status_code == 200:
    branches = response_branches.json()
    for branch in branches:
        branch_name = branch['name']
        url_commits = f"https://gitlab.com/api/v4/projects/....../repository/commits?ref_name={branch_name}" # Your Project ID
        try:
            response_commits = requests.get(url_commits, headers=headers, proxies=proxies, timeout=60)
            if response_commits.status_code == 200:
                # 确保目录存在
                import os
                if not os.path.exists("branches_commits"):
                    os.makedirs("branches_commits")

                with open(f"branches_commits/{branch_name}_commits.json", "w") as file:
                    file.write(response_commits.text)
                print(f"Saved commit data for branch: {branch_name}")
            else:
                print(f"Failed to retrieve commits for branch {branch_name}: {response_commits.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving commits for branch {branch_name}: {e}")
else:
    print(f"Failed to retrieve branches: {response_branches.status_code}")
