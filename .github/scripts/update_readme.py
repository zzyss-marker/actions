import requests
import random
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import markdown
import feedparser
import time
import urllib.parse

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
    
    try:
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
    except Exception as e:
        print(f"获取GitHub趋势项目失败: {e}")
        return []

def get_ai_news_from_rss():
    """从RSS订阅源获取AI相关新闻"""
    # AI相关RSS订阅源列表 - 更新为更可靠的源
    rss_feeds = [
        "https://api.dbot.pp.ua/v1/rss/csdn/ai",
        "https://rsshub.app/36kr/ai", # 36氪AI频道
        "https://rsshub.app/sspai/topic/268", # 少数派AI话题
        "https://rsshub.app/juejin/category/ai", # 掘金AI分类
        "https://rsshub.app/zhihu/topic/19551275", # 知乎AI话题
        "https://rsshub.app/baidu/research/ai" # 百度研究院AI动态
    ]
    
    ai_news = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    
    for feed_url in rss_feeds:
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:2]:  # 每个源取前2条
                if len(ai_news) >= 5:  # 最多获取5条新闻
                    break
                    
                title = entry.title
                url = entry.link
                
                # 尝试获取描述
                description = ""
                if hasattr(entry, "summary"):
                    soup = BeautifulSoup(entry.summary, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "description"):
                    soup = BeautifulSoup(entry.description, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                
                ai_news.append({
                    "title": title,
                    "url": url,
                    "description": description
                })
                
            if len(ai_news) >= 5:
                break
                
            # 避免过快请求多个RSS源
            time.sleep(1)
            
        except Exception as e:
            print(f"获取RSS源 {feed_url} 失败: {e}")
            continue
    
    # 如果没有获取到足够的新闻，使用备用新闻
    if len(ai_news) == 0:
        ai_news = [
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
    
    return ai_news[:5]  # 返回最多5条新闻

def get_cybersecurity_news_from_rss():
    """从RSS订阅源获取网络安全新闻"""
    # 网络安全相关RSS订阅源列表 - 更新为更可靠的源
    rss_feeds = [
        "https://api.dbot.pp.ua/v1/rss/tencent_cloud",
        "https://rsshub.app/freebuf", # FreeBuf
        "https://rsshub.app/4hou", # 嘶吼
        "https://rsshub.app/anquanke/all", # 安全客
        "https://rsshub.app/secrss/all", # SecRSS
        "https://rsshub.app/hackernews" # Hacker News
    ]
    
    security_news = []
    
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:1]:  # 每个源取前1条
                if len(security_news) >= 3:  # 最多获取3条新闻
                    break
                    
                title = entry.title
                url = entry.link
                
                # 尝试获取描述
                description = ""
                if hasattr(entry, "summary"):
                    soup = BeautifulSoup(entry.summary, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "description"):
                    soup = BeautifulSoup(entry.description, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                
                security_news.append({
                    "title": title,
                    "url": url,
                    "description": description
                })
                
            if len(security_news) >= 3:
                break
                
            # 避免过快请求多个RSS源
            time.sleep(1)
            
        except Exception as e:
            print(f"获取RSS源 {feed_url} 失败: {e}")
            continue
    
    # 如果没有获取到足够的新闻，添加网络安全提示
    if len(security_news) == 0:
        tips = [
            "定期更新所有软件和操作系统，以修补已知的安全漏洞。",
            "使用密码管理器生成和存储强密码，避免在多个网站使用相同密码。",
            "启用双因素认证(2FA)，为账户添加额外的安全层。",
            "定期备份重要数据，并遵循3-2-1备份规则：3份数据副本，2种不同的存储介质，1份异地存储。",
            "使用VPN保护公共Wi-Fi连接时的网络流量。"
        ]
        
        for tip in tips[:3]:
            security_news.append({
                "title": "网络安全提示",
                "url": "https://www.cisa.gov/cybersecurity",
                "description": tip
            })
    
    return security_news[:3]  # 返回最多3条新闻

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

def get_tech_news_from_api():
    """从API获取科技新闻"""
    try:
        # 以36氪为例
        url = "https://36kr.com/api/newsflash"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            news_list = data.get('data', {}).get('items', [])
            
            tech_news = []
            for news in news_list[:3]:
                tech_news.append({
                    "title": news.get('title', ''),
                    "url": f"https://36kr.com/newsflash/{news.get('id')}",
                    "description": news.get('description', '')[:100] + "..."
                })
            
            return tech_news
    except Exception as e:
        print(f"从API获取科技新闻失败: {e}")
    
    # 返回备用新闻
    return [
        {
            "title": "苹果发布新一代M3芯片，性能大幅提升",
            "url": "https://www.apple.com/newsroom/",
            "description": "新芯片采用先进工艺，能效比创历史新高"
        },
        # ... 其他备用新闻 ...
    ]

def get_arxiv_papers(category, max_results=3):
    """获取 arXiv 特定类别的最新论文"""
    base_url = "http://export.arxiv.org/api/query?"
    
    # 构建查询参数
    query_params = {
        'search_query': f'cat:{category}',
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'max_results': max_results
    }
    
    # 构建完整 URL
    query_url = base_url + urllib.parse.urlencode(query_params)
    
    try:
        response = requests.get(query_url)
        feed = feedparser.parse(response.content)
        
        papers = []
        for entry in feed.entries:
            title = entry.title
            url = entry.link
            
            # 获取摘要并清理格式
            if hasattr(entry, "summary"):
                soup = BeautifulSoup(entry.summary, "html.parser")
                summary = soup.get_text()
                # 截断摘要
                description = summary[:150] + "..." if len(summary) > 150 else summary
            else:
                description = "无摘要"
            
            # 获取作者
            authors = ", ".join([author.name for author in entry.authors]) if hasattr(entry, "authors") else "未知作者"
            
            papers.append({
                "title": title,
                "url": url,
                "description": description,
                "authors": authors
            })
        
        return papers
    except Exception as e:
        print(f"获取 arXiv 论文失败: {e}")
        return []

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
    try:
        ai_news = get_ai_news_from_rss()
        if ai_news:
            ai_news_section = "### AI 技术动态\n\n"
            for news in ai_news:
                ai_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
        else:
            ai_news_section = "### AI 技术动态\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"更新 AI 新闻时出错: {e}")
        ai_news_section = "### AI 技术动态\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    
    ai_pattern = r"### AI 技术动态\n\n- \[.*?\n\n"
    if re.search(ai_pattern, content, re.DOTALL):
        content = re.sub(ai_pattern, ai_news_section + "\n\n", content)
    else:
        content += ai_news_section + "\n\n"
    
    # 更新网络安全新闻
    try:
        security_news = get_cybersecurity_news_from_rss()
        if security_news:
            security_news_section = "### 网络安全资讯\n\n"
            for news in security_news:
                security_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
        else:
            security_news_section = "### 网络安全资讯\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"更新网络安全新闻时出错: {e}")
        security_news_section = "### 网络安全资讯\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    
    security_pattern = r"### 网络安全(提示|资讯)\n\n.*?\n\n"
    if re.search(security_pattern, content, re.DOTALL):
        content = re.sub(security_pattern, security_news_section + "\n\n", content)
    else:
        content += security_news_section + "\n\n"
    
    # 更新就业趋势
    job_trend = get_tech_job_trends()
    job_pattern = r"### 技术就业趋势\n\n.*?\n\n"
    if re.search(job_pattern, content, re.DOTALL):
        content = re.sub(job_pattern, f"### 技术就业趋势\n\n{job_trend}\n\n", content)
    else:
        content += f"### 技术就业趋势\n\n{job_trend}\n\n"
    
    # 更新科技新闻
    try:
        tech_news = get_tech_news_from_api()
        if tech_news:
            tech_news_section = "### 科技热点\n\n"
            for news in tech_news:
                tech_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
        else:
            tech_news_section = "### 科技热点\n\n- API 获取科技新闻失败，请稍后再查看\n"
    except Exception as e:
        print(f"更新科技新闻时出错: {e}")
        tech_news_section = "### 科技热点\n\n- API 获取科技新闻失败，请稍后再查看\n"
    
    tech_pattern = r"### 科技热点\n\n- \[.*?\n\n"
    if re.search(tech_pattern, content, re.DOTALL):
        content = re.sub(tech_pattern, tech_news_section + "\n\n", content)
    else:
        content += tech_news_section + "\n\n"
    
    # 更新GitHub趋势项目
    try:
        trending_repos = get_github_trending()
        if trending_repos:
            trending_section = "### GitHub 趋势项目\n\n"
            for repo in trending_repos:
                trending_section += f"- [{repo['name']}]({repo['url']}) - {repo['description']}\n"
        else:
            trending_section = "### GitHub 趋势项目\n\n- GitHub 趋势数据暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"获取GitHub趋势项目失败: {e}")
        trending_section = "### GitHub 趋势项目\n\n- GitHub 趋势数据暂时不可用，请稍后再查看\n"
    
    trending_pattern = r"### GitHub 趋势项目\n\n- \[.*?\n\n"
    if re.search(trending_pattern, content, re.DOTALL):
        content = re.sub(trending_pattern, trending_section + "\n\n", content)
    else:
        content += trending_section + "\n\n"
    
    # 更新 AI 研究论文
    try:
        ai_papers = get_arxiv_papers("cs.AI", 3)  # 人工智能类别
        if ai_papers:
            ai_papers_section = "### AI 研究论文\n\n"
            for paper in ai_papers:
                ai_papers_section += f"- [{paper['title']}]({paper['url']}) - {paper['authors']}\n  {paper['description']}\n\n"
        else:
            ai_papers_section = "### AI 研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    except Exception as e:
        print(f"更新 AI 论文时出错: {e}")
        ai_papers_section = "### AI 研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    
    ai_papers_pattern = r"### AI 研究论文\n\n- \[.*?\n\n"
    if re.search(ai_papers_pattern, content, re.DOTALL):
        content = re.sub(ai_papers_pattern, ai_papers_section, content)
    else:
        content += ai_papers_section
    
    # 更新网络安全研究论文
    try:
        # 由于 arXiv 没有专门的网络安全类别，我们使用密码学和系统安全相关类别
        security_papers = get_arxiv_papers("cs.CR", 3)  # 密码学与安全类别
        if security_papers:
            security_papers_section = "### 网络安全研究论文\n\n"
            for paper in security_papers:
                security_papers_section += f"- [{paper['title']}]({paper['url']}) - {paper['authors']}\n  {paper['description']}\n\n"
        else:
            security_papers_section = "### 网络安全研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    except Exception as e:
        print(f"更新网络安全论文时出错: {e}")
        security_papers_section = "### 网络安全研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    
    security_papers_pattern = r"### 网络安全研究论文\n\n- \[.*?\n\n"
    if re.search(security_papers_pattern, content, re.DOTALL):
        content = re.sub(security_papers_pattern, security_papers_section, content)
    else:
        content += security_papers_section
    
    # 写入更新后的内容
    try:
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(content)
        print("README.md 已更新")
    except Exception as e:
        print(f"写入 README.md 失败: {e}")

if __name__ == "__main__":
    update_readme() 