import requests
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup
import markdown

def get_dev_quote():
    """获取随机编程名言"""
    quotes = [
        "简单是可靠的先决条件。 —— Edsger W. Dijkstra",
        "软件就像做爱，一次犯错，你需要用余生来维护。 —— Michael Sinz",
        "任何傻瓜都能写出计算机能理解的代码。优秀的程序员能写出人能理解的代码。 —— Martin Fowler",
        "调试代码比写代码难两倍。因此，如果你写代码时尽可能聪明，那么你在调试时会显得不够聪明。 —— Brian W. Kernighan",
        "先让它工作，再让它正确，最后让它快速工作。 —— Kent Beck",
        "编程不是关于你知道什么，而是关于你能解决什么问题。 —— V. Anton Spraul",
    ]
    return random.choice(quotes)

def get_github_trending(language=None, since="daily"):
    """获取GitHub趋势项目"""
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"
    url += f"?since={since}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    trending_repos = []
    repo_list = soup.select('article.Box-row')
    
    for repo in repo_list[:5]:  # 只获取前5个
        name_element = repo.select_one('h2 a')
        if name_element:
            repo_name = name_element.text.strip().replace('\n', '').replace(' ', '')
            repo_url = f"https://github.com{name_element['href']}"
            
            description_element = repo.select_one('p')
            description = description_element.text.strip() if description_element else "No description"
            
            trending_repos.append({
                'name': repo_name,
                'url': repo_url,
                'description': description
            })
    
    return trending_repos

def get_dev_tip():
    """获取随机开发技巧"""
    tips = [
        "使用版本控制系统（如Git）来跟踪代码更改。",
        "编写单元测试以确保代码质量和防止回归。",
        "遵循DRY（Don't Repeat Yourself）原则，避免代码重复。",
        "定期重构代码以提高可维护性。",
        "使用有意义的变量名和函数名，提高代码可读性。",
        "学习使用键盘快捷键，提高编码效率。",
        "定期备份你的工作，防止数据丢失。",
        "使用代码检查工具来发现潜在问题。",
        "保持学习新技术和最佳实践。",
        "在编写代码前先规划和设计。",
        "使用注释解释为什么这样做，而不是做了什么。",
        "遵循KISS原则（Keep It Simple, Stupid）。",
        "使用持续集成来自动化测试和部署。",
        "学习阅读文档的技巧，这比搜索答案更有效。",
        "定期休息，避免长时间连续编码导致的疲劳。"
    ]
    return random.choice(tips)

def update_readme():
    """更新README.md文件"""
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = "# 开发者日常助手\n\n自动更新的开发资源和提示\n\n"
    
    # 更新日期
    today = datetime.now().strftime("%Y-%m-%d")
    date_pattern = r"## 今日更新 \(\d{4}-\d{2}-\d{2}\)"
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, f"## 今日更新 ({today})", content)
    else:
        content += f"\n## 今日更新 ({today})\n\n"
    
    # 更新名言
    quote = get_dev_quote()
    quote_pattern = r"### 今日名言\n\n> .*?\n"
    if re.search(quote_pattern, content, re.DOTALL):
        content = re.sub(quote_pattern, f"### 今日名言\n\n> {quote}\n", content)
    else:
        content += f"### 今日名言\n\n> {quote}\n\n"
    
    # 更新开发技巧
    tip = get_dev_tip()
    tip_pattern = r"### 开发技巧\n\n.*?\n\n"
    if re.search(tip_pattern, content, re.DOTALL):
        content = re.sub(tip_pattern, f"### 开发技巧\n\n{tip}\n\n", content)
    else:
        content += f"### 开发技巧\n\n{tip}\n\n"
    
    # 更新GitHub趋势项目
    try:
        trending_repos = get_github_trending()
        trending_section = "### GitHub 趋势项目\n\n"
        for repo in trending_repos:
            trending_section += f"- [{repo['name']}]({repo['url']}) - {repo['description']}\n"
        
        trending_pattern = r"### GitHub 趋势项目\n\n- \[.*?\n\n"
        if re.search(trending_pattern, content, re.DOTALL):
            content = re.sub(trending_pattern, trending_section + "\n\n", content)
        else:
            content += trending_section + "\n\n"
    except Exception as e:
        print(f"获取GitHub趋势项目失败: {e}")
    
    # 写入更新后的内容
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("README.md 已更新")

if __name__ == "__main__":
    update_readme() 