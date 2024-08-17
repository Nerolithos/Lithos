GITLAB_URL="https://gitlab.com"
PROJECT_PATH="101camp/7py/tasks"
ACCESS_TOKEN="......"

# 对项目路径进行 URL 编码
ENCODED_PROJECT_PATH=$(echo $PROJECT_PATH | sed 's/\//%2F/g')

# 使用 curl 获取项目下的所有 Issues
response=$(curl --header "PRIVATE-TOKEN: $ACCESS_TOKEN" "$GITLAB_URL/api/v4/projects/$ENCODED_PROJECT_PATH/issues?per_page=500")

# 解析并统计 Issue 的数量
issue_count=$(echo $response | grep -o '"id":' | wc -l)

# 输出 Issue 的数量
echo "Total number of issues: $issue_count"



# put these below into terminal to run:

# chmod +x list_issues.sh
# ./list_issues.sh