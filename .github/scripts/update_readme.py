import requests
import random
import re
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import markdown
import feedparser
import time
import urllib.parse
import hashlib
import base64
import sys
import os

# 添加脚本目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from interactive_features import interactive_features
except ImportError:
    print("警告: 无法导入互动功能模块")
    interactive_features = None

try:
    from sentiment_analyzer import sentiment_analyzer
except ImportError:
    print("警告: 无法导入情感分析模块")
    sentiment_analyzer = None

try:
    from html_generator import html_generator
except ImportError:
    print("警告: 无法导入HTML生成模块")
    html_generator = None

try:
    from api_generator import api_generator
except ImportError:
    print("警告: 无法导入API生成模块")
    api_generator = None

try:
    from rss_generator import rss_generator
except ImportError:
    print("警告: 无法导入RSS生成模块")
    rss_generator = None

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
    # 优先使用CSDN的AI资讯源
    primary_source = "https://api.dbot.pp.ua/v1/rss/csdn/ai"
    
    # 定义headers变量
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    
    try:
        print(f"尝试获取 AI 新闻 RSS: {primary_source}")
        response = requests.get(primary_source, headers=headers, timeout=15)
        print(f"RSS 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"RSS 响应内容: {response.text[:500]}...")
            
            # 解析Atom格式
            feed = feedparser.parse(response.text)
            
            if feed.entries:
                ai_news = []
                print(f"成功获取 {len(feed.entries)} 条 AI 新闻")
                
                for entry in feed.entries[:20]:  # 最多获取20条
                    title = entry.title
                    url = entry.link if isinstance(entry.link, str) else entry.link[0]['href']
                    
                    # 获取描述
                    description = ""
                    if hasattr(entry, "summary"):
                        soup = BeautifulSoup(entry.summary, "html.parser")
                        description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                    
                    if not description:
                        description = "AI技术动态，详情请点击链接查看完整内容"
                    
                    print(f"添加文章: {title} - URL: {url}")
                    ai_news.append({
                        "title": title,
                        "url": url,
                        "description": description
                    })
                    
                    if len(ai_news) >= 5:  # 只取前5条
                        break
                
                if ai_news:
                    print(f"最终获取到 {len(ai_news)} 条 AI 新闻")
                    for news in ai_news:
                        print(f"- {news['title']} ({news['url']})")
                    return ai_news
    except Exception as e:
        print(f"获取RSS源 {primary_source} 失败: {e}")
    
    # 如果主源失败，使用备用新闻
    print("使用备用 AI 新闻内容")
    ai_news = [
        {
            "title": "OpenAI发布GPT-4 Turbo，性能大幅提升",
            "url": "https://openai.com/blog/",
            "description": "新模型在推理能力和上下文窗口方面有显著改进"
        },
        # 可以添加更多备用新闻
    ]
    
    return ai_news

def get_cybersecurity_news_from_rss():
    """从RSS订阅源获取网络安全新闻"""
    # 网络安全相关RSS订阅源列表 - 更新为更可靠的源
    rss_feeds = [
        "https://www.freebuf.com/feed",
        "https://api.anquanke.com/data/v1/rss",
        "https://paper.seebug.org/rss",
        "https://www.4hou.com/feed",
        "https://xlab.tencent.com/cn/atom.xml",
        "https://www.sec-wiki.com/news/rss",
        "http://blog.knownsec.com/feed",
        "https://vipread.com/feed",
        "https://www.aqniu.com/feed",
        "https://keenlab.tencent.com/zh/atom.xml",
        "https://blog.netlab.360.com/rss",
        "https://www.seebug.org/rss/new",
        "https://www.secpulse.com/feed",
        "https://tttang.com/rss.xml"
    ]
    
    security_news = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    
    for feed_url in rss_feeds:
        try:
            print(f"尝试获取网络安全新闻 RSS: {feed_url}")
            response = requests.get(feed_url, headers=headers, timeout=15)
            print(f"RSS 响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"RSS 响应内容: {response.text[:200]}...")
                continue
                
            print(f"RSS 响应内容: {response.text[:200]}...")
            
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                print(f"RSS 源没有条目: {feed_url}")
                continue
                
            print(f"成功获取 {len(feed.entries)} 条网络安全新闻")
            
            for entry in feed.entries[:1]:  # 每个源取前1条
                if len(security_news) >= 3:  # 最多获取3条新闻
                    break
                    
                title = entry.title
                
                # 处理 Atom 格式的链接
                if hasattr(entry, "link") and not entry.link.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    url = entry.link
                elif hasattr(entry, "links") and entry.links:
                    # 尝试找到非图片链接
                    for link in entry.links:
                        if hasattr(link, "href") and not link.href.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            url = link.href
                            break
                    else:
                        # 如果所有链接都是图片，使用第一个链接
                        url = entry.links[0].href
                else:
                    # 尝试从 id 字段获取链接
                    url = entry.id if hasattr(entry, "id") else "#"
                
                # 检查 URL 是否为图片链接
                if url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    print(f"跳过图片链接: {url}")
                    continue
                
                # 尝试获取描述
                description = ""
                if hasattr(entry, "summary"):
                    soup = BeautifulSoup(entry.summary, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "description"):
                    soup = BeautifulSoup(entry.description, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "content") and entry.content:
                    soup = BeautifulSoup(entry.content[0].value, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                
                if not description:
                    description = "安全公告，详情请点击链接查看完整内容"
                
                print(f"添加网络安全文章: {title} - URL: {url}")
                
                security_news.append({
                    "title": title,
                    "url": url,
                    "description": description
                })
                
            if len(security_news) >= 3:
                break
                
            time.sleep(2)
            
        except Exception as e:
            print(f"获取RSS源 {feed_url} 失败: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"请求详情: {e.request.method} {e.request.url}")
                if hasattr(e, 'response') and e.response:
                    print(f"响应状态码: {e.response.status_code}")
                    print(f"响应头: {e.response.headers}")
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

def get_tech_news_from_rss():
    """从RSS订阅源获取科技新闻"""
    # 科技新闻相关RSS订阅源列表
    rss_feeds = [
        "https://api.dbot.pp.ua/v1/rss/tencent_cloud",
        "https://api.dbot.pp.ua/v1/rss/cnbeta",  # 添加这个可能更可靠的源
        "https://rsshub.app/36kr/technology", # 36氪科技频道
        "https://rsshub.app/ifanr/app", # 爱范儿
        "https://rsshub.app/sspai/matrix", # 少数派Matrix
        "https://rsshub.app/cnbeta", # cnBeta
        "https://rsshub.app/geekpark/breakingnews" # 极客公园
    ]
    
    tech_news = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*'
    }
    
    for feed_url in rss_feeds:
        try:
            print(f"尝试获取科技新闻 RSS: {feed_url}")
            response = requests.get(feed_url, headers=headers, timeout=15)
            print(f"RSS 响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"RSS 响应内容: {response.text[:200]}...")
                continue
                
            print(f"RSS 响应内容: {response.text[:200]}...")
            
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                print(f"RSS 源没有条目: {feed_url}")
                continue
                
            print(f"成功获取 {len(feed.entries)} 条科技新闻")
            
            for entry in feed.entries[:3]:  # 直接获取前3条
                title = entry.title
                
                # 处理 Atom 格式的链接
                if hasattr(entry, "link") and not entry.link.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    url = entry.link
                elif hasattr(entry, "links") and entry.links:
                    # 尝试找到非图片链接
                    for link in entry.links:
                        if hasattr(link, "href") and not link.href.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            url = link.href
                            break
                    else:
                        # 如果所有链接都是图片，使用第一个链接
                        url = entry.links[0].href
                else:
                    # 尝试从 id 字段获取链接
                    url = entry.id if hasattr(entry, "id") else "#"
                
                # 检查 URL 是否为图片链接
                if url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    print(f"跳过图片链接: {url}")
                    continue
                
                # 尝试获取描述
                description = ""
                if hasattr(entry, "summary"):
                    soup = BeautifulSoup(entry.summary, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "description"):
                    soup = BeautifulSoup(entry.description, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                elif hasattr(entry, "content") and entry.content:
                    soup = BeautifulSoup(entry.content[0].value, "html.parser")
                    description = soup.get_text()[:100] + "..." if len(soup.get_text()) > 100 else soup.get_text()
                
                print(f"添加科技文章: {title} - URL: {url}")
                
                tech_news.append({
                    "title": title,
                    "url": url,
                    "description": description
                })
                
                if len(tech_news) >= 3:
                    break
            
            if len(tech_news) >= 3:
                break
                
            time.sleep(2)
            
        except Exception as e:
            print(f"获取RSS源 {feed_url} 失败: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            if isinstance(e, requests.exceptions.RequestException):
                print(f"请求详情: {e.request.method} {e.request.url}")
                if hasattr(e, 'response') and e.response:
                    print(f"响应状态码: {e.response.status_code}")
                    print(f"响应头: {e.response.headers}")
            continue
    
    # 如果没有获取到足够的新闻，使用备用新闻
    if len(tech_news) == 0:
        print("未能获取任何科技新闻，使用备用内容")
        tech_news = [
            {
                "title": "苹果发布新一代M3芯片，性能大幅提升",
                "url": "https://www.apple.com/newsroom/",
                "description": "新芯片采用先进工艺，能效比创历史新高"
            },
            # ... 其他备用新闻 ...
        ]
    
    print(f"最终获取到 {len(tech_news)} 条科技新闻")
    for news in tech_news:
        print(f"- {news['title']} ({news['url']})")
    
    return tech_news[:3]  # 返回最多3条新闻

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
    
    # 更新AI新闻（带情感分析）
    try:
        ai_news = get_ai_news_from_rss()
        if ai_news and sentiment_analyzer:
            # 进行情感分析
            analyzed_ai_news = sentiment_analyzer.analyze_news_batch(ai_news)
            ai_news_section = "### AI 技术动态\n\n"

            for news in analyzed_ai_news:
                sentiment_emoji = sentiment_analyzer.get_sentiment_emoji(news['sentiment']['sentiment'])
                hotness_level = news['hotness']['level']
                ai_news_section += f"- {sentiment_emoji} [{news['title']}]({news['url']}) {hotness_level}\n"
                ai_news_section += f"  {news['description']}\n"

            # 打印将要更新的内容
            print("将更新 AI 技术动态为:")
            print(ai_news_section)
        elif ai_news:
            # 没有情感分析器时的备用方案
            ai_news_section = "### AI 技术动态\n\n"
            for news in ai_news:
                ai_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
        else:
            ai_news_section = "### AI 技术动态\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"更新 AI 新闻时出错: {e}")
        ai_news_section = "### AI 技术动态\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    
    # 定义缺失的正则表达式
    ai_pattern = r"### AI 技术动态\n\n[\s\S]*?(?=\n\n###|\Z)"
    
    if re.search(ai_pattern, content):
        content = re.sub(ai_pattern, ai_news_section, content)
        print("已替换 AI 技术动态内容")
    else:
        content += ai_news_section + "\n\n"
        print("已添加 AI 技术动态内容")
    
    # 更新网络安全新闻
    try:
        security_news = get_cybersecurity_news_from_rss()
        if security_news:
            security_news_section = "### 网络安全资讯\n\n"
            for news in security_news:
                security_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
            
            # 打印将要更新的内容
            print("将更新网络安全资讯为:")
            print(security_news_section)
        else:
            security_news_section = "### 网络安全资讯\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"更新网络安全新闻时出错: {e}")
        security_news_section = "### 网络安全资讯\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    
    # 使用更精确的正则表达式
    security_pattern = r"### 网络安全(提示|资讯)\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(security_pattern, content, re.DOTALL):
        content = re.sub(security_pattern, security_news_section, content)
        print("已替换网络安全资讯内容")
    else:
        content += security_news_section + "\n\n"
        print("已添加网络安全资讯内容")
    
    # 更新就业趋势
    job_trend = get_tech_job_trends()
    job_pattern = r"### 技术就业趋势\n\n.*?\n\n"
    if re.search(job_pattern, content, re.DOTALL):
        content = re.sub(job_pattern, f"### 技术就业趋势\n\n{job_trend}\n\n", content)
    else:
        content += f"### 技术就业趋势\n\n{job_trend}\n\n"
    
    # 更新科技新闻（带情感分析）
    try:
        tech_news = get_tech_news_from_rss()
        if tech_news and sentiment_analyzer:
            # 进行情感分析
            analyzed_tech_news = sentiment_analyzer.analyze_news_batch(tech_news)
            tech_news_section = "### 科技热点\n\n"

            for news in analyzed_tech_news:
                sentiment_emoji = sentiment_analyzer.get_sentiment_emoji(news['sentiment']['sentiment'])
                hotness_level = news['hotness']['level']
                tech_news_section += f"- {sentiment_emoji} [{news['title']}]({news['url']}) {hotness_level}\n"
                tech_news_section += f"  {news['description']}\n"

            # 打印将要更新的内容
            print("将更新科技热点为:")
            print(tech_news_section)
        elif tech_news:
            # 没有情感分析器时的备用方案
            tech_news_section = "### 科技热点\n\n"
            for news in tech_news:
                tech_news_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
        else:
            tech_news_section = "### 科技热点\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    except Exception as e:
        print(f"更新科技新闻时出错: {e}")
        tech_news_section = "### 科技热点\n\n- RSS 订阅源暂时不可用，请稍后再查看\n"
    
    # 使用更精确的正则表达式
    tech_pattern = r"### 科技热点\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(tech_pattern, content):
        content = re.sub(tech_pattern, tech_news_section, content)
        print("已替换科技热点内容")
    else:
        content += tech_news_section + "\n\n"
        print("已添加科技热点内容")
    
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
    
    # 定义缺失的正则表达式
    trending_pattern = r"### GitHub 趋势项目\n\n[\s\S]*?(?=\n\n###|\Z)"
    
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
            
            # 打印将要更新的内容
            print("将更新 AI 研究论文为:")
            print(ai_papers_section)
        else:
            ai_papers_section = "### AI 研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    except Exception as e:
        print(f"更新 AI 论文时出错: {e}")
        ai_papers_section = "### AI 研究论文\n\n- arXiv 论文数据暂时不可用，请稍后再查看\n\n"
    
    # 使用更精确的正则表达式
    ai_papers_pattern = r"### AI 研究论文\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(ai_papers_pattern, content, re.DOTALL):
        content = re.sub(ai_papers_pattern, ai_papers_section, content)
        print("已替换 AI 研究论文内容")
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
    
    # 添加新功能内容

    # 技术股票追踪
    try:
        tech_stocks = get_tech_stocks()
        if tech_stocks:
            stocks_section = "### 📈 科技股票追踪\n\n"
            for stock in tech_stocks:
                change_symbol = "📈" if stock['change'] >= 0 else "📉"
                stocks_section += f"- **{stock['symbol']}**: ${stock['price']:.2f} {change_symbol} {stock['change']:+.2f} ({stock['change_percent']:+.1f}%)\n"
        else:
            stocks_section = "### 📈 科技股票追踪\n\n- 股票数据暂时不可用\n"
    except Exception as e:
        print(f"获取股票信息失败: {e}")
        stocks_section = "### 📈 科技股票追踪\n\n- 股票数据暂时不可用\n"

    stocks_pattern = r"### 📈 科技股票追踪\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(stocks_pattern, content):
        content = re.sub(stocks_pattern, stocks_section, content)
    else:
        content += stocks_section + "\n\n"

    # 开发者工具推荐
    try:
        dev_tools = get_dev_tools()
        tools_section = "### 🛠️ 开发者工具推荐\n\n"
        for tool in dev_tools:
            tools_section += f"- **[{tool['name']}]({tool['url']})** ({tool['category']}) - {tool['description']}\n"
    except Exception as e:
        print(f"获取开发工具失败: {e}")
        tools_section = "### 🛠️ 开发者工具推荐\n\n- 工具推荐暂时不可用\n"

    tools_pattern = r"### 🛠️ 开发者工具推荐\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(tools_pattern, content):
        content = re.sub(tools_pattern, tools_section, content)
    else:
        content += tools_section + "\n\n"

    # 编程挑战
    try:
        challenge = get_coding_challenge()
        challenge_section = f"### 🎯 今日编程挑战\n\n"
        challenge_section += f"**{challenge['title']}** (难度: {challenge['difficulty']})\n\n"
        challenge_section += f"{challenge['description']}\n\n"
        challenge_section += f"标签: {', '.join(challenge['tags'])}\n"
    except Exception as e:
        print(f"获取编程挑战失败: {e}")
        challenge_section = "### 🎯 今日编程挑战\n\n- 编程挑战暂时不可用\n"

    challenge_pattern = r"### 🎯 今日编程挑战\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(challenge_pattern, content):
        content = re.sub(challenge_pattern, challenge_section, content)
    else:
        content += challenge_section + "\n\n"

    # 移动开发动态
    try:
        mobile_news = get_mobile_dev_news()
        mobile_section = "### 📱 移动开发动态\n\n"
        for news in mobile_news:
            mobile_section += f"- [{news['title']}]({news['url']}) - {news['description']}\n"
    except Exception as e:
        print(f"获取移动开发新闻失败: {e}")
        mobile_section = "### 📱 移动开发动态\n\n- 移动开发资讯暂时不可用\n"

    mobile_pattern = r"### 📱 移动开发动态\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(mobile_pattern, content):
        content = re.sub(mobile_pattern, mobile_section, content)
    else:
        content += mobile_section + "\n\n"

    # 技术趣闻
    try:
        trivia = get_tech_trivia()
        trivia_section = f"### 🎪 技术趣闻\n\n{trivia}\n"
    except Exception as e:
        print(f"获取技术趣闻失败: {e}")
        trivia_section = "### 🎪 技术趣闻\n\n- 技术趣闻暂时不可用\n"

    trivia_pattern = r"### 🎪 技术趣闻\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(trivia_pattern, content):
        content = re.sub(trivia_pattern, trivia_section, content)
    else:
        content += trivia_section + "\n\n"

    # 技术书籍推荐
    try:
        book = get_tech_books()
        book_section = f"### 📚 技术书籍推荐\n\n"
        book_section += f"**《{book['title']}》** - {book['author']}\n\n"
        book_section += f"{book['description']} (分类: {book['category']})\n"
    except Exception as e:
        print(f"获取书籍推荐失败: {e}")
        book_section = "### 📚 技术书籍推荐\n\n- 书籍推荐暂时不可用\n"

    book_pattern = r"### 📚 技术书籍推荐\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(book_pattern, content):
        content = re.sub(book_pattern, book_section, content)
    else:
        content += book_section + "\n\n"

    # 技术会议日历
    try:
        conferences = get_tech_conferences()
        if conferences:
            conf_section = "### 🌍 即将举行的技术会议\n\n"
            for conf in conferences:
                conf_section += f"- **{conf['name']}** ({conf['date']}) - {conf['location']}\n"
                conf_section += f"  主题: {', '.join(conf['topics'])} | 还有 {conf['days_until']} 天\n"
        else:
            conf_section = "### 🌍 即将举行的技术会议\n\n- 暂无即将举行的会议信息\n"
    except Exception as e:
        print(f"获取技术会议失败: {e}")
        conf_section = "### 🌍 即将举行的技术会议\n\n- 会议信息暂时不可用\n"

    conf_pattern = r"### 🌍 即将举行的技术会议\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(conf_pattern, content):
        content = re.sub(conf_pattern, conf_section, content)
    else:
        content += conf_section + "\n\n"

    # 创业公司动态
    try:
        startup_news = get_startup_news()
        startup_section = "### 🚀 创业公司动态\n\n"
        for news in startup_news:
            startup_section += f"- **{news['company']}**: {news['news']}"
            if news['amount'] != 'N/A':
                startup_section += f" ({news['amount']})"
            startup_section += f" - {news['description']}\n"
    except Exception as e:
        print(f"获取创业动态失败: {e}")
        startup_section = "### 🚀 创业公司动态\n\n- 创业动态暂时不可用\n"

    startup_pattern = r"### 🚀 创业公司动态\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(startup_pattern, content):
        content = re.sub(startup_pattern, startup_section, content)
    else:
        content += startup_section + "\n\n"

    # 设计资源推荐
    try:
        design_resources = get_design_resources()
        design_section = "### 🎨 设计资源推荐\n\n"
        for resource in design_resources:
            design_section += f"- **[{resource['name']}]({resource['url']})** ({resource['type']}) - {resource['description']}\n"
    except Exception as e:
        print(f"获取设计资源失败: {e}")
        design_section = "### 🎨 设计资源推荐\n\n- 设计资源暂时不可用\n"

    design_pattern = r"### 🎨 设计资源推荐\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(design_pattern, content):
        content = re.sub(design_pattern, design_section, content)
    else:
        content += design_section + "\n\n"

    # 学习路径推荐
    try:
        learning_path = get_learning_path()
        learning_section = f"### 🎓 技能学习路径\n\n"
        learning_section += f"**{learning_path['skill']}** (难度: {learning_path['level']}, 预计时间: {learning_path['duration']})\n\n"
        learning_section += f"学习步骤: {' → '.join(learning_path['steps'])}\n"
    except Exception as e:
        print(f"获取学习路径失败: {e}")
        learning_section = "### 🎓 技能学习路径\n\n- 学习路径推荐暂时不可用\n"

    learning_pattern = r"### 🎓 技能学习路径\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(learning_pattern, content):
        content = re.sub(learning_pattern, learning_section, content)
    else:
        content += learning_section + "\n\n"

    # 编程音乐推荐
    try:
        music = get_programming_music()
        music_section = f"### 🎵 编程音乐推荐\n\n"
        music_section += f"**{music['title']}** - {music['artist']}\n\n"
        music_section += f"类型: {music['genre']} | {music['description']}\n"
    except Exception as e:
        print(f"获取音乐推荐失败: {e}")
        music_section = "### 🎵 编程音乐推荐\n\n- 音乐推荐暂时不可用\n"

    music_pattern = r"### 🎵 编程音乐推荐\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(music_pattern, content):
        content = re.sub(music_pattern, music_section, content)
    else:
        content += music_section + "\n\n"

    # 添加统计信息
    stats_section = f"### 📊 今日统计\n\n"
    stats_section += f"- 📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    stats_section += f"- 🔄 自动更新: 每日 08:00 (UTC+8)\n"
    stats_section += f"- 📈 功能模块: 15+ 个活跃功能\n"
    stats_section += f"- 🌟 数据源: 多个RSS源和API接口\n"

    stats_pattern = r"### 📊 今日统计\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(stats_pattern, content):
        content = re.sub(stats_pattern, stats_section, content)
    else:
        content += stats_section + "\n\n"

    # 技术热词趋势
    try:
        tech_trends = get_tech_trends()
        trends_section = "### 🔥 技术热词趋势\n\n"
        for trend in tech_trends:
            trends_section += f"- **{trend['keyword']}** {trend['trend']} {trend['change']} - {trend['description']}\n"
    except Exception as e:
        print(f"获取技术趋势失败: {e}")
        trends_section = "### 🔥 技术热词趋势\n\n- 趋势数据暂时不可用\n"

    trends_pattern = r"### 🔥 技术热词趋势\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(trends_pattern, content):
        content = re.sub(trends_pattern, trends_section, content)
    else:
        content += trends_section + "\n\n"

    # 开源项目聚焦
    try:
        spotlight_project = get_open_source_spotlight()
        spotlight_section = f"### ⭐ 开源项目聚焦\n\n"
        spotlight_section += f"**{spotlight_project['name']}** ({spotlight_project['language']}) - ⭐ {spotlight_project['stars']}\n\n"
        spotlight_section += f"{spotlight_project['description']}\n\n"
        spotlight_section += f"💡 亮点: {spotlight_project['why_interesting']}\n"
    except Exception as e:
        print(f"获取开源项目失败: {e}")
        spotlight_section = "### ⭐ 开源项目聚焦\n\n- 项目信息暂时不可用\n"

    spotlight_pattern = r"### ⭐ 开源项目聚焦\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(spotlight_pattern, content):
        content = re.sub(spotlight_pattern, spotlight_section, content)
    else:
        content += spotlight_section + "\n\n"

    # 薪资报告
    try:
        salary_info = get_tech_salary_info()
        salary_section = f"### 💰 技术薪资快报\n\n"
        salary_section += f"**{salary_info['position']}** ({salary_info['level']}) {salary_info['trend']}\n\n"
        salary_section += f"薪资范围: {salary_info['salary_range']} | 热门技能: {', '.join(salary_info['hot_skills'])}\n"
    except Exception as e:
        print(f"获取薪资信息失败: {e}")
        salary_section = "### 💰 技术薪资快报\n\n- 薪资信息暂时不可用\n"

    salary_pattern = r"### 💰 技术薪资快报\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(salary_pattern, content):
        content = re.sub(salary_pattern, salary_section, content)
    else:
        content += salary_section + "\n\n"

    # 程序员笑话
    try:
        joke = get_developer_joke()
        joke_section = f"### 😄 程序员笑话\n\n{joke}\n"
    except Exception as e:
        print(f"获取笑话失败: {e}")
        joke_section = "### 😄 程序员笑话\n\n- 笑话暂时不可用\n"

    joke_pattern = r"### 😄 程序员笑话\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(joke_pattern, content):
        content = re.sub(joke_pattern, joke_section, content)
    else:
        content += joke_section + "\n\n"

    # GitHub统计信息
    try:
        github_stats = get_github_stats()
        if github_stats:
            github_section = "### 🐙 GitHub 生态统计\n\n"
            github_section += f"- 📦 总仓库数: {github_stats['total_repos']}\n"
            github_section += f"- 👥 活跃开发者: {github_stats['active_developers']}\n"
            github_section += f"- 💻 每日提交: {github_stats['daily_commits']}\n"
            github_section += f"- 🌐 编程语言: {github_stats['languages_used']}\n"
            github_section += f"- 🔓 开源项目: {github_stats['open_source_projects']}\n"
        else:
            github_section = "### 🐙 GitHub 生态统计\n\n- 统计数据暂时不可用\n"
    except Exception as e:
        print(f"获取GitHub统计失败: {e}")
        github_section = "### 🐙 GitHub 生态统计\n\n- 统计数据暂时不可用\n"

    github_pattern = r"### 🐙 GitHub 生态统计\n\n[\s\S]*?(?=\n\n###|\Z)"
    if re.search(github_pattern, content):
        content = re.sub(github_pattern, github_section, content)
    else:
        content += github_section + "\n\n"

    # 互动功能部分
    if interactive_features:
        # 每周挑战
        try:
            weekly_challenge = interactive_features.get_current_week_challenge()
            challenge_section = f"### 🏆 本周技术挑战\n\n"
            challenge_section += f"**{weekly_challenge['title']}** (难度: {weekly_challenge['difficulty']})\n\n"
            challenge_section += f"{weekly_challenge['description']}\n\n"
            challenge_section += f"🏷️ 标签: {', '.join(weekly_challenge['tags'])} | "
            challenge_section += f"⏱️ 预计时间: {weekly_challenge['estimated_time']} | "
            challenge_section += f"🎯 奖励积分: {weekly_challenge['reward_points']}\n"
        except Exception as e:
            print(f"获取每周挑战失败: {e}")
            challenge_section = "### 🏆 本周技术挑战\n\n- 挑战信息暂时不可用\n"

        weekly_challenge_pattern = r"### 🏆 本周技术挑战\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(weekly_challenge_pattern, content):
            content = re.sub(weekly_challenge_pattern, challenge_section, content)
        else:
            content += challenge_section + "\n\n"

        # 技术小测验
        try:
            quiz = interactive_features.generate_tech_quiz()
            quiz_section = f"### 🧠 技术小测验\n\n"
            quiz_section += f"**问题**: {quiz['question']}\n\n"
            for i, option in enumerate(quiz['options']):
                quiz_section += f"{chr(65+i)}. {option}\n"
            quiz_section += f"\n💡 答案将在明天公布\n"
        except Exception as e:
            print(f"获取技术测验失败: {e}")
            quiz_section = "### 🧠 技术小测验\n\n- 测验内容暂时不可用\n"

        quiz_pattern = r"### 🧠 技术小测验\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(quiz_pattern, content):
            content = re.sub(quiz_pattern, quiz_section, content)
        else:
            content += quiz_section + "\n\n"

        # 编程小贴士
        try:
            tip = interactive_features.get_coding_tip_of_day()
            tip_section = f"### 💡 今日编程小贴士\n\n"
            tip_section += f"**{tip['title']}**\n\n"
            tip_section += f"{tip['content']}\n\n"
            if 'example' in tip:
                tip_section += f"```\n{tip['example']}\n```\n"
        except Exception as e:
            print(f"获取编程小贴士失败: {e}")
            tip_section = "### 💡 今日编程小贴士\n\n- 小贴士暂时不可用\n"

        tip_pattern = r"### 💡 今日编程小贴士\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(tip_pattern, content):
            content = re.sub(tip_pattern, tip_section, content)
        else:
            content += tip_section + "\n\n"

        # 职业建议
        try:
            career_advice = interactive_features.get_tech_career_advice()
            career_section = f"### 🚀 职业发展建议\n\n"
            career_section += f"**{career_advice['category']}**: {career_advice['advice']}\n\n"
            career_section += f"📋 行动建议: {career_advice['action']}\n"
        except Exception as e:
            print(f"获取职业建议失败: {e}")
            career_section = "### 🚀 职业发展建议\n\n- 职业建议暂时不可用\n"

        career_pattern = r"### 🚀 职业发展建议\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(career_pattern, content):
            content = re.sub(career_pattern, career_section, content)
        else:
            content += career_section + "\n\n"

        # 每日挑战徽章
        try:
            badge_info = interactive_features.generate_daily_challenge_badge()
            badge_section = f"### 🏅 今日挑战徽章\n\n"
            badge_section += f"{badge_info['message']}\n\n"
            badge_section += f"挑战ID: `{badge_info['challenge_id']}` | 日期: {badge_info['date']}\n"
        except Exception as e:
            print(f"获取挑战徽章失败: {e}")
            badge_section = "### 🏅 今日挑战徽章\n\n- 徽章信息暂时不可用\n"

        badge_pattern = r"### 🏅 今日挑战徽章\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(badge_pattern, content):
            content = re.sub(badge_pattern, badge_section, content)
        else:
            content += badge_section + "\n\n"

        # 技术投票
        try:
            poll = interactive_features.get_random_poll()
            poll_section = f"### 📊 技术话题投票\n\n"
            poll_section += f"**{poll['question']}** (分类: {poll['category']})\n\n"
            for i, option in enumerate(poll['options']):
                poll_section += f"- [ ] {option}\n"
            poll_section += f"\n💬 在Issues中参与讨论和投票！\n"
        except Exception as e:
            print(f"获取技术投票失败: {e}")
            poll_section = "### 📊 技术话题投票\n\n- 投票内容暂时不可用\n"

        poll_pattern = r"### 📊 技术话题投票\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(poll_pattern, content):
            content = re.sub(poll_pattern, poll_section, content)
        else:
            content += poll_section + "\n\n"

    # 新闻分析摘要
    if sentiment_analyzer:
        try:
            # 收集所有新闻进行综合分析
            all_news = []

            # 重新获取新闻数据进行分析
            try:
                ai_news = get_ai_news_from_rss()
                if ai_news:
                    all_news.extend(ai_news)
            except:
                pass

            try:
                tech_news = get_tech_news_from_rss()
                if tech_news:
                    all_news.extend(tech_news)
            except:
                pass

            if all_news:
                trend_summary = sentiment_analyzer.generate_trend_summary(
                    sentiment_analyzer.analyze_news_batch(all_news)
                )

                analysis_section = f"### 📈 今日新闻分析\n\n{trend_summary}\n"
            else:
                analysis_section = "### 📈 今日新闻分析\n\n- 暂无足够数据进行分析\n"

        except Exception as e:
            print(f"生成新闻分析失败: {e}")
            analysis_section = "### 📈 今日新闻分析\n\n- 分析功能暂时不可用\n"

        analysis_pattern = r"### 📈 今日新闻分析\n\n[\s\S]*?(?=\n\n###|\Z)"
        if re.search(analysis_pattern, content):
            content = re.sub(analysis_pattern, analysis_section, content)
        else:
            content += analysis_section + "\n\n"

    # 添加页脚信息
    footer_section = "---\n\n"
    footer_section += "### 🤖 关于此项目\n\n"
    footer_section += "这是一个由 GitHub Actions 驱动的自动化技术资讯聚合项目。\n\n"
    footer_section += "- 🔄 **自动更新**: 每天自动抓取最新技术资讯\n"
    footer_section += "- 🌐 **多源聚合**: 整合多个权威技术媒体和平台\n"
    footer_section += "- 🎯 **智能筛选**: AI辅助内容筛选和分类\n"
    footer_section += "- 📊 **数据可视**: 趋势分析和统计展示\n\n"
    footer_section += "**数据来源**: RSS订阅、API接口、网页抓取\n\n"
    footer_section += "**更新频率**: 每日 08:00 (UTC+8)\n\n"
    footer_section += "**项目维护**: 由 GitHub Actions 自动维护，欢迎 Star ⭐ 和 Fork 🍴\n\n"

    # 检查是否已有页脚，如果没有则添加
    if "### 🤖 关于此项目" not in content:
        content += footer_section

    # 写入更新后的内容
    try:
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(content)
        print("README.md 已更新")
    except Exception as e:
        print(f"写入 README.md 失败: {e}")

    # 生成HTML页面
    if html_generator:
        try:
            # 收集数据用于HTML生成
            html_data = {
                'ai_news': [],
                'tech_news': [],
                'tech_trends': [],
                'dev_tools': [],
                'github_repos': []
            }

            # 重新获取数据
            try:
                ai_news = get_ai_news_from_rss()
                if ai_news:
                    html_data['ai_news'] = ai_news
            except:
                pass

            try:
                tech_news = get_tech_news_from_rss()
                if tech_news:
                    html_data['tech_news'] = tech_news
            except:
                pass

            try:
                html_data['tech_trends'] = get_tech_trends()
            except:
                pass

            try:
                html_data['dev_tools'] = get_dev_tools()
            except:
                pass

            try:
                html_data['github_repos'] = get_github_trending()
            except:
                pass

            # 生成HTML
            html_content = html_generator.generate_html_page(html_data)
            html_generator.save_html_file(html_content, 'docs/index.html')

            print("HTML页面已生成")

        except Exception as e:
            print(f"生成HTML页面失败: {e}")

    # 生成API数据
    if api_generator:
        try:
            # 收集所有数据用于API
            api_data = {
                'ai_news': [],
                'tech_news': [],
                'security_news': [],
                'github_repos': [],
                'tech_trends': [],
                'dev_tools': []
            }

            # 重新获取数据
            try:
                ai_news = get_ai_news_from_rss()
                if ai_news:
                    api_data['ai_news'] = ai_news
            except:
                pass

            try:
                tech_news = get_tech_news_from_rss()
                if tech_news:
                    api_data['tech_news'] = tech_news
            except:
                pass

            try:
                security_news = get_security_news_from_rss()
                if security_news:
                    api_data['security_news'] = security_news
            except:
                pass

            try:
                api_data['github_repos'] = get_github_trending()
            except:
                pass

            try:
                api_data['tech_trends'] = get_tech_trends()
            except:
                pass

            try:
                api_data['dev_tools'] = get_dev_tools()
            except:
                pass

            # 生成API文件
            api_generator.save_api_files(api_data)
            print("API数据已生成")

        except Exception as e:
            print(f"生成API数据失败: {e}")

    # 生成RSS订阅源
    if rss_generator:
        try:
            # 使用相同的数据生成RSS
            rss_data = {
                'ai_news': [],
                'tech_news': [],
                'security_news': [],
                'github_repos': []
            }

            # 重新获取数据
            try:
                ai_news = get_ai_news_from_rss()
                if ai_news:
                    rss_data['ai_news'] = ai_news
            except:
                pass

            try:
                tech_news = get_tech_news_from_rss()
                if tech_news:
                    rss_data['tech_news'] = tech_news
            except:
                pass

            try:
                security_news = get_security_news_from_rss()
                if security_news:
                    rss_data['security_news'] = security_news
            except:
                pass

            try:
                github_repos = get_github_trending()
                if github_repos:
                    rss_data['github_repos'] = github_repos
            except:
                pass

            # 生成RSS文件
            rss_generator.save_rss_files(rss_data)
            print("RSS订阅源已生成")

        except Exception as e:
            print(f"生成RSS订阅源失败: {e}")

# 新增功能函数

def get_tech_stocks():
    """获取科技股票信息"""
    # 使用免费的股票API获取科技公司股价
    tech_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'META']
    stock_info = []

    try:
        # 使用Yahoo Finance的免费API
        for symbol in tech_stocks[:3]:  # 只获取前3个避免请求过多
            try:
                # 简单的股票信息获取
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if 'chart' in data and data['chart']['result']:
                        result = data['chart']['result'][0]
                        meta = result['meta']
                        current_price = meta.get('regularMarketPrice', 0)
                        prev_close = meta.get('previousClose', 0)
                        change = current_price - prev_close if current_price and prev_close else 0
                        change_percent = (change / prev_close * 100) if prev_close else 0

                        stock_info.append({
                            'symbol': symbol,
                            'price': current_price,
                            'change': change,
                            'change_percent': change_percent
                        })

                time.sleep(1)  # 避免请求过快
            except Exception as e:
                print(f"获取 {symbol} 股价失败: {e}")
                continue

    except Exception as e:
        print(f"获取股票信息失败: {e}")

    return stock_info

def get_dev_tools():
    """获取开发者工具推荐"""
    tools = [
        {
            'name': 'GitHub Copilot',
            'description': 'AI代码助手，提高编程效率',
            'category': 'AI工具',
            'url': 'https://github.com/features/copilot'
        },
        {
            'name': 'Postman',
            'description': 'API开发和测试平台',
            'category': 'API工具',
            'url': 'https://www.postman.com/'
        },
        {
            'name': 'Figma',
            'description': '协作式界面设计工具',
            'category': '设计工具',
            'url': 'https://www.figma.com/'
        },
        {
            'name': 'Docker',
            'description': '容器化应用部署平台',
            'category': '部署工具',
            'url': 'https://www.docker.com/'
        },
        {
            'name': 'VS Code',
            'description': '轻量级代码编辑器',
            'category': '编辑器',
            'url': 'https://code.visualstudio.com/'
        },
        {
            'name': 'Notion',
            'description': '全能工作空间和笔记工具',
            'category': '效率工具',
            'url': 'https://www.notion.so/'
        }
    ]

    # 随机选择2-3个工具
    selected_tools = random.sample(tools, min(3, len(tools)))
    return selected_tools

def get_coding_challenge():
    """获取编程挑战题目"""
    challenges = [
        {
            'title': '两数之和',
            'difficulty': '简单',
            'description': '给定一个整数数组和目标值，找出数组中和为目标值的两个数的索引',
            'tags': ['数组', '哈希表']
        },
        {
            'title': '最长回文子串',
            'difficulty': '中等',
            'description': '给定字符串，找出其中最长的回文子串',
            'tags': ['字符串', '动态规划']
        },
        {
            'title': '二叉树的最大深度',
            'difficulty': '简单',
            'description': '给定二叉树，找出其最大深度',
            'tags': ['树', '递归']
        },
        {
            'title': '合并两个有序链表',
            'difficulty': '简单',
            'description': '将两个升序链表合并为一个新的升序链表',
            'tags': ['链表', '递归']
        },
        {
            'title': '有效的括号',
            'difficulty': '简单',
            'description': '判断字符串中的括号是否有效匹配',
            'tags': ['栈', '字符串']
        }
    ]

    return random.choice(challenges)

def get_mobile_dev_news():
    """获取移动开发相关新闻"""
    mobile_news = []

    # 移动开发相关RSS源
    rss_feeds = [
        "https://rsshub.app/juejin/category/android",
        "https://rsshub.app/juejin/category/ios",
        "https://developer.android.com/feeds/all.atom.xml"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for feed_url in rss_feeds[:1]:  # 只获取一个源避免请求过多
        try:
            response = requests.get(feed_url, headers=headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)

                for entry in feed.entries[:2]:  # 每个源取2条
                    title = entry.title
                    url = entry.link if hasattr(entry, 'link') else '#'

                    # 获取描述
                    if hasattr(entry, 'summary'):
                        soup = BeautifulSoup(entry.summary, 'html.parser')
                        description = soup.get_text()[:100] + "..."
                    else:
                        description = "移动开发相关资讯"

                    mobile_news.append({
                        'title': title,
                        'url': url,
                        'description': description
                    })

                    if len(mobile_news) >= 2:
                        break

        except Exception as e:
            print(f"获取移动开发新闻失败: {e}")
            continue

    # 如果没有获取到新闻，提供默认内容
    if not mobile_news:
        mobile_news = [
            {
                'title': 'Flutter 3.0 发布重大更新',
                'url': 'https://flutter.dev/',
                'description': 'Google发布Flutter 3.0，带来更好的性能和新特性'
            },
            {
                'title': 'iOS 17 开发者预览版发布',
                'url': 'https://developer.apple.com/',
                'description': '苹果发布iOS 17开发者预览版，包含多项新功能'
            }
        ]

    return mobile_news

def get_tech_trivia():
    """获取技术趣闻"""
    trivia_list = [
        "第一个计算机bug是由一只真正的虫子引起的 - 1947年Grace Hopper在Harvard Mark II计算机中发现了一只飞蛾",
        "JavaScript最初只用了10天时间就被创造出来，由Brendan Eich在1995年完成",
        "第一个网站至今仍在运行：http://info.cern.ch/hypertext/WWW/TheProject.html",
        "Python语言的名字来源于英国喜剧团体Monty Python，而不是蟒蛇",
        "世界上第一个域名是symbolics.com，注册于1985年3月15日",
        "Linux企鹅吉祥物Tux的名字来源于Torvalds UniX的缩写",
        "第一个计算机病毒叫做Creeper，创建于1971年，它会显示'I'm the creeper, catch me if you can!'",
        "WiFi这个名字实际上不代表任何东西，它只是一个朗朗上口的品牌名称"
    ]

    return random.choice(trivia_list)

def get_tech_books():
    """获取技术书籍推荐"""
    books = [
        {
            'title': '代码整洁之道',
            'author': 'Robert C. Martin',
            'description': '编写可读、可维护代码的实践指南',
            'category': '软件工程'
        },
        {
            'title': '深度学习',
            'author': 'Ian Goodfellow',
            'description': '深度学习领域的权威教材',
            'category': '人工智能'
        },
        {
            'title': '设计模式',
            'author': 'Gang of Four',
            'description': '面向对象设计的经典模式',
            'category': '软件设计'
        },
        {
            'title': 'Kubernetes权威指南',
            'author': '龚正等',
            'description': '容器编排平台的完整指南',
            'category': '云原生'
        },
        {
            'title': 'Python编程：从入门到实践',
            'author': 'Eric Matthes',
            'description': 'Python学习的最佳入门书籍',
            'category': '编程语言'
        }
    ]

    return random.choice(books)

def get_cloud_pricing():
    """获取云服务价格信息"""
    # 模拟云服务价格数据（实际应用中可以调用各云服务商API）
    cloud_services = [
        {
            'provider': 'AWS',
            'service': 'EC2 t3.micro',
            'price': '$0.0104/hour',
            'region': 'us-east-1',
            'change': '无变化'
        },
        {
            'provider': 'Azure',
            'service': 'B1S Virtual Machine',
            'price': '$0.0104/hour',
            'region': 'East US',
            'change': '无变化'
        },
        {
            'provider': 'Google Cloud',
            'service': 'e2-micro',
            'price': '$0.0084/hour',
            'region': 'us-central1',
            'change': '无变化'
        }
    ]

    return cloud_services

def get_tech_conferences():
    """获取技术会议信息"""
    # 模拟技术会议数据
    conferences = [
        {
            'name': 'Google I/O 2025',
            'date': '2025-05-14',
            'location': 'Mountain View, CA',
            'type': '开发者大会',
            'topics': ['AI', 'Android', 'Web']
        },
        {
            'name': 'Apple WWDC 2025',
            'date': '2025-06-05',
            'location': 'San Jose, CA',
            'type': '开发者大会',
            'topics': ['iOS', 'macOS', 'AI']
        },
        {
            'name': 'Microsoft Build 2025',
            'date': '2025-05-21',
            'location': 'Seattle, WA',
            'type': '开发者大会',
            'topics': ['Azure', 'AI', '.NET']
        }
    ]

    # 返回即将举行的会议
    today = datetime.now()
    upcoming = []

    for conf in conferences:
        conf_date = datetime.strptime(conf['date'], '%Y-%m-%d')
        if conf_date > today:
            days_until = (conf_date - today).days
            conf['days_until'] = days_until
            upcoming.append(conf)

    return sorted(upcoming, key=lambda x: x['days_until'])[:3]

def get_programming_music():
    """获取编程音乐推荐"""
    music_recommendations = [
        {
            'title': 'Lofi Hip Hop Radio',
            'artist': 'ChilledCow',
            'genre': 'Lo-fi',
            'description': '适合专注编程的轻松背景音乐'
        },
        {
            'title': 'Brain.fm Focus',
            'artist': 'Brain.fm',
            'genre': '专注音乐',
            'description': '科学设计的专注力提升音乐'
        },
        {
            'title': 'Synthwave Mix',
            'artist': 'Various Artists',
            'genre': 'Synthwave',
            'description': '复古未来主义电子音乐，激发创造力'
        },
        {
            'title': 'Ambient Coding',
            'artist': 'Various Artists',
            'genre': 'Ambient',
            'description': '环境音乐，营造平静的编程氛围'
        }
    ]

    return random.choice(music_recommendations)

def get_startup_news():
    """获取创业公司动态"""
    # 模拟创业公司新闻
    startup_news = [
        {
            'company': 'OpenAI',
            'news': '完成新一轮融资',
            'amount': '$10B',
            'description': '估值达到$80B，继续领跑AI领域'
        },
        {
            'company': 'Anthropic',
            'news': '发布Claude 3.5',
            'amount': 'N/A',
            'description': '在多项基准测试中超越GPT-4'
        },
        {
            'company': 'Mistral AI',
            'news': '推出开源大模型',
            'amount': 'N/A',
            'description': '挑战OpenAI的市场地位'
        }
    ]

    return random.sample(startup_news, min(2, len(startup_news)))

def get_design_resources():
    """获取设计资源推荐"""
    design_resources = [
        {
            'name': 'Dribbble',
            'type': '设计灵感',
            'url': 'https://dribbble.com/',
            'description': '全球设计师作品展示平台'
        },
        {
            'name': 'Unsplash',
            'type': '免费图片',
            'url': 'https://unsplash.com/',
            'description': '高质量免费图片资源'
        },
        {
            'name': 'Coolors',
            'type': '配色工具',
            'url': 'https://coolors.co/',
            'description': '智能配色方案生成器'
        },
        {
            'name': 'Figma Community',
            'type': '设计模板',
            'url': 'https://www.figma.com/community/',
            'description': '免费设计模板和组件库'
        }
    ]

    return random.sample(design_resources, min(2, len(design_resources)))

def get_learning_path():
    """获取技能学习路径推荐"""
    learning_paths = [
        {
            'skill': '全栈开发',
            'level': '初级到中级',
            'duration': '6-12个月',
            'steps': ['HTML/CSS基础', 'JavaScript', 'React/Vue', 'Node.js', '数据库', '部署']
        },
        {
            'skill': 'AI/机器学习',
            'level': '中级',
            'duration': '8-15个月',
            'steps': ['Python基础', '数学基础', 'TensorFlow/PyTorch', '深度学习', '项目实践']
        },
        {
            'skill': '云原生开发',
            'level': '中级到高级',
            'duration': '4-8个月',
            'steps': ['Docker', 'Kubernetes', '微服务', 'DevOps', '监控运维']
        },
        {
            'skill': '网络安全',
            'level': '初级到中级',
            'duration': '6-10个月',
            'steps': ['网络基础', '系统安全', '渗透测试', '安全工具', '合规认证']
        }
    ]

    return random.choice(learning_paths)

def get_tech_trends():
    """获取技术热词趋势"""
    # 模拟技术热词数据
    tech_keywords = [
        {'keyword': 'AI', 'trend': '🔥', 'change': '+15%', 'description': '人工智能持续火热'},
        {'keyword': 'Kubernetes', 'trend': '📈', 'change': '+8%', 'description': '容器编排需求增长'},
        {'keyword': 'Rust', 'trend': '🚀', 'change': '+12%', 'description': '系统编程语言崛起'},
        {'keyword': 'WebAssembly', 'trend': '⭐', 'change': '+6%', 'description': 'Web性能优化技术'},
        {'keyword': 'Edge Computing', 'trend': '📊', 'change': '+10%', 'description': '边缘计算应用扩展'},
        {'keyword': 'Quantum Computing', 'trend': '🔬', 'change': '+4%', 'description': '量子计算研究进展'},
        {'keyword': 'Blockchain', 'trend': '📉', 'change': '-3%', 'description': '区块链热度回落'},
        {'keyword': 'Serverless', 'trend': '☁️', 'change': '+7%', 'description': '无服务器架构普及'}
    ]

    # 随机选择5个热词
    selected_trends = random.sample(tech_keywords, min(5, len(tech_keywords)))
    return sorted(selected_trends, key=lambda x: int(x['change'].replace('%', '').replace('+', '').replace('-', '')), reverse=True)

def get_github_stats():
    """获取GitHub统计信息"""
    try:
        # 获取一些有趣的GitHub统计
        stats = {
            'total_repos': '100M+',
            'active_developers': '73M+',
            'daily_commits': '1M+',
            'languages_used': '500+',
            'open_source_projects': '28M+'
        }
        return stats
    except Exception as e:
        print(f"获取GitHub统计失败: {e}")
        return None

def get_developer_joke():
    """获取程序员笑话"""
    jokes = [
        "为什么程序员喜欢黑暗？因为光会产生bug！",
        "程序员的三大美德：懒惰、急躁和傲慢。",
        "世界上有10种人：懂二进制的和不懂二进制的。",
        "调试就像是犯罪电影中的侦探，你既是侦探，也是凶手。",
        "程序员最讨厌的两件事：1. 写文档 2. 没有文档",
        "如果调试是去除bug的过程，那么编程就是放入bug的过程。",
        "真正的程序员不需要注释，代码就是最好的文档。",
        "程序员的口头禅：在我的机器上运行得很好！"
    ]

    return random.choice(jokes)

def get_tech_salary_info():
    """获取技术薪资信息"""
    salary_data = [
        {
            'position': 'AI工程师',
            'level': '中级',
            'salary_range': '25-40万',
            'trend': '📈',
            'hot_skills': ['Python', 'TensorFlow', 'PyTorch']
        },
        {
            'position': '全栈开发',
            'level': '中级',
            'salary_range': '20-35万',
            'trend': '📊',
            'hot_skills': ['React', 'Node.js', 'TypeScript']
        },
        {
            'position': '云架构师',
            'level': '高级',
            'salary_range': '35-60万',
            'trend': '🚀',
            'hot_skills': ['AWS', 'Kubernetes', 'DevOps']
        },
        {
            'position': '安全工程师',
            'level': '中级',
            'salary_range': '22-38万',
            'trend': '📈',
            'hot_skills': ['渗透测试', '安全审计', 'Python']
        }
    ]

    return random.choice(salary_data)

def get_open_source_spotlight():
    """获取开源项目聚焦"""
    projects = [
        {
            'name': 'Tauri',
            'description': '使用Rust构建跨平台桌面应用',
            'language': 'Rust',
            'stars': '70k+',
            'why_interesting': '比Electron更轻量的桌面应用解决方案'
        },
        {
            'name': 'SvelteKit',
            'description': '现代Web应用框架',
            'language': 'JavaScript',
            'stars': '15k+',
            'why_interesting': '编译时优化，运行时性能优异'
        },
        {
            'name': 'Deno',
            'description': '现代JavaScript/TypeScript运行时',
            'language': 'Rust/TypeScript',
            'stars': '90k+',
            'why_interesting': 'Node.js创始人的新作品，内置TypeScript支持'
        },
        {
            'name': 'Zed',
            'description': '高性能代码编辑器',
            'language': 'Rust',
            'stars': '25k+',
            'why_interesting': '专为协作编程设计的现代编辑器'
        }
    ]

    return random.choice(projects)

if __name__ == "__main__":
    update_readme()