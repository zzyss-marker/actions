import requests
import random
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import markdown
import feedparser

def get_programming_quote():
    """从编程语录API获取名言"""
    try:
        response = requests.get("https://programming-quotes-api.herokuapp.com/Quotes/random")
        if response.status_code == 200:
            data = response.json()
            return f"{data['en']} —— {data['author']}"
    except:
        pass
    
    # 备用名言列表
    quotes = [
        "简单是可靠的先决条件。 —— Edsger W. Dijkstra",
        "软件就像做爱，一次犯错，你需要用余生来维护。 —— Michael Sinz",
        "任何傻瓜都能写出计算机能理解的代码。优秀的程序员能写出人能理解的代码。 —— Martin Fowler",
        "调试代码比写代码难两倍。因此，如果你写代码时尽可能聪明，那么你在调试时会显得不够聪明。 —— Brian W. Kernighan",
        "先让它工作，再让它正确，最后让它快速工作。 —— Kent Beck",
        "编程不是关于你知道什么，而是关于你能解决什么问题。 —— V. Anton Spraul",
        "代码是写给人看的，只是顺便能在机器上运行。 —— Harold Abelson",
        "最好的程序员不仅是编程高手，还知道哪些代码不需要写。 —— Bill Gates",
        "编程的艺术就是处理复杂性的艺术。 —— Edsger W. Dijkstra",
        "软件设计的目标是控制复杂性，而不是增加复杂性。 —— Pamela Zave"
    ]
    return random.choice(quotes)

def get_github_trending(language=None, since="daily"):
    """获取GitHub趋势项目"""
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"
    url += f"?since={since}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
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

def get_ai_news():
    """获取AI相关新闻"""
    try:
        # 使用NewsAPI获取AI相关新闻
        api_key = "YOUR_NEWS_API_KEY"  # 需要替换为您的API密钥
        url = f"https://newsapi.org/v2/everything?q=artificial+intelligence&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])[:3]
    except:
        pass
    
    # 备用AI新闻
    return [
        {
            "title": "OpenAI发布GPT-4 Turbo，性能大幅提升",
            "url": "https://openai.com/blog/",
            "description": "新模型在推理能力和上下文窗口方面有显著改进"
        },
        {
            "title": "谷歌推出新一代AI模型Gemini",
            "url": "https://blog.google/technology/ai/",
            "description": "多模态能力超越现有大型语言模型"
        },
        {
            "title": "AI在医疗诊断领域取得突破性进展",
            "url": "https://www.nature.com/articles/",
            "description": "新研究表明AI可以提前预测某些疾病风险"
        }
    ]

def get_cybersecurity_tips():
    """获取网络安全提示"""
    tips = [
        "定期更新所有软件和操作系统，以修补已知的安全漏洞。",
        "使用密码管理器生成和存储强密码，避免在多个网站使用相同密码。",
        "启用双因素认证(2FA)，为账户添加额外的安全层。",
        "定期备份重要数据，并遵循3-2-1备份规则：3份数据副本，2种不同的存储介质，1份异地存储。",
        "使用VPN保护公共Wi-Fi连接时的网络流量。",
        "警惕钓鱼邮件，不要点击来源不明的链接或下载可疑附件。",
        "定期检查您的设备是否有恶意软件，使用可靠的安全软件。",
        "加密敏感数据，特别是在云存储或移动设备上的数据。",
        "了解社会工程学攻击手段，提高安全意识。",
        "为不同类型的账户使用不同级别的安全措施，重要账户采用更强的保护。",
        "定期审查应用程序权限，撤销不必要的访问权限。",
        "使用安全的DNS服务，如Cloudflare的1.1.1.1或Google的8.8.8.8。",
        "在处理敏感信息时，考虑使用隐私浏览模式或Tor浏览器。",
        "定期检查您的账户活动，及时发现可疑行为。",
        "使用防火墙和入侵检测系统保护网络边界。"
    ]
    return random.choice(tips)

def get_tech_job_trends():
    """获取技术就业趋势"""
    trends = [
        "人工智能和机器学习工程师需求持续增长，尤其是具有大型语言模型经验的专业人才。",
        "云计算专家仍然是就业市场的热门，AWS、Azure和GCP认证价值显著。",
        "网络安全人才缺口扩大，零信任安全模型专家需求激增。",
        "数据科学和分析角色持续热门，特别是能够将数据洞察转化为业务价值的专业人士。",
        "DevOps和SRE工程师需求稳定增长，自动化和基础设施即代码技能备受青睐。",
        "全栈开发者仍然是市场主力，React、Node.js和Python技能组合特别受欢迎。",
        "区块链和Web3开发者虽经历市场波动，但在金融科技领域仍有稳定需求。",
        "远程工作机会持续增加，但混合工作模式成为许多科技公司的新标准。",
        "软技能如沟通、团队协作和问题解决能力在技术招聘中的重要性日益提升。",
        "量子计算专家虽然是小众领域，但薪资水平和增长潜力显著。",
        "边缘计算和IoT专家在制造业和智能城市项目中需求增加。",
        "具备多语言编程能力和跨平台开发经验的工程师更具竞争力。",
        "敏捷和Scrum认证在项目管理角色中价值提升。",
        "低代码/无代码平台专家需求增长，尤其在企业数字化转型项目中。",
        "可持续技术和绿色IT专家在环保意识增强的企业中机会增多。"
    ]
    return random.choice(trends)

def get_tech_news():
    """获取科技热点新闻"""
    try:
        # 使用NewsAPI获取科技新闻
        api_key = "YOUR_NEWS_API_KEY"  # 需要替换为您的API密钥
        url = f"https://newsapi.org/v2/top-headlines?category=technology&pageSize=3&apiKey={api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])[:3]
    except:
        pass
    
    # 备用科技新闻
    return [
        {
            "title": "苹果发布新一代M3芯片，性能大幅提升",
            "url": "https://www.apple.com/newsroom/",
            "description": "新芯片采用先进工艺，能效比创历史新高"
        },
        {
            "title": "SpaceX成功发射新一批星链卫星",
            "url": "https://www.spacex.com/updates/",
            "description": "全球互联网覆盖计划进入新阶段"
        },
        {
            "title": "微软推出新一代Windows功能更新",
            "url": "https://blogs.windows.com/",
            "description": "集成更多AI功能，用户体验全面提升"
        }
    ]

def update_readme():
    """更新README.md文件"""
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = "# 技术视野助手\n\n自动更新的技术资讯和资源\n\n"
    
    # 更新日期
    today = datetime.now().strftime("%Y-%m-%d")
    date_pattern = r"## 今日更新 \(\d{4}-\d{2}-\d{2}\)"
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, f"## 今日更新 ({today})", content)
    else:
        content += f"\n## 今日更新 ({today})\n\n"
    
    # 更新名言
    quote = get_programming_quote()
    quote_pattern = r"### 今日名言\n\n> .*?\n"
    if re.search(quote_pattern, content, re.DOTALL):
        content = re.sub(quote_pattern, f"### 今日名言\n\n> {quote}\n", content)
    else:
        content += f"### 今日名言\n\n> {quote}\n\n"
    
    # 更新AI新闻
    ai_news = get_ai_news()
    ai_news_section = "### AI 技术动态\n\n"
    for news in ai_news:
        ai_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
    
    ai_pattern = r"### AI 技术动态\n\n- \[.*?\n\n"
    if re.search(ai_pattern, content, re.DOTALL):
        content = re.sub(ai_pattern, ai_news_section + "\n\n", content)
    else:
        content += ai_news_section + "\n\n"
    
    # 更新网络安全提示
    security_tip = get_cybersecurity_tips()
    security_pattern = r"### 网络安全提示\n\n.*?\n\n"
    if re.search(security_pattern, content, re.DOTALL):
        content = re.sub(security_pattern, f"### 网络安全提示\n\n{security_tip}\n\n", content)
    else:
        content += f"### 网络安全提示\n\n{security_tip}\n\n"
    
    # 更新就业趋势
    job_trend = get_tech_job_trends()
    job_pattern = r"### 技术就业趋势\n\n.*?\n\n"
    if re.search(job_pattern, content, re.DOTALL):
        content = re.sub(job_pattern, f"### 技术就业趋势\n\n{job_trend}\n\n", content)
    else:
        content += f"### 技术就业趋势\n\n{job_trend}\n\n"
    
    # 更新科技新闻
    tech_news = get_tech_news()
    tech_news_section = "### 科技热点\n\n"
    for news in tech_news:
        tech_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
    
    tech_pattern = r"### 科技热点\n\n- \[.*?\n\n"
    if re.search(tech_pattern, content, re.DOTALL):
        content = re.sub(tech_pattern, tech_news_section + "\n\n", content)
    else:
        content += tech_news_section + "\n\n"
    
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