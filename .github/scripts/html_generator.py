"""
HTML页面生成器 - 为技术视野助手生成美观的Web界面
"""

import json
import os
from datetime import datetime

class HTMLGenerator:
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技术视野助手 - 每日技术资讯</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card .icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .stat-card .number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-card .label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .section-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .section-card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .news-item {
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }
        
        .news-item:last-child {
            border-bottom: none;
        }
        
        .news-item h3 {
            color: #333;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        
        .news-item a {
            color: #667eea;
            text-decoration: none;
        }
        
        .news-item a:hover {
            text-decoration: underline;
        }
        
        .news-item p {
            color: #666;
            font-size: 0.9rem;
            margin-top: 5px;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            background: #667eea;
            color: white;
            border-radius: 12px;
            font-size: 0.8rem;
            margin-right: 5px;
        }
        
        .trend-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .trend-item:last-child {
            border-bottom: none;
        }
        
        .trend-name {
            font-weight: 500;
        }
        
        .trend-change {
            font-weight: bold;
        }
        
        .trend-up {
            color: #28a745;
        }
        
        .trend-down {
            color: #dc3545;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
            
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 技术视野助手</h1>
            <p>每日技术资讯 · AI驱动 · 自动更新</p>
            <p>最后更新: {update_time}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📰</div>
                <div class="number">{total_news}</div>
                <div class="label">今日新闻</div>
            </div>
            <div class="stat-card">
                <div class="icon">🔥</div>
                <div class="number">{hot_topics}</div>
                <div class="label">热门话题</div>
            </div>
            <div class="stat-card">
                <div class="icon">📈</div>
                <div class="number">{trending_repos}</div>
                <div class="label">趋势项目</div>
            </div>
            <div class="stat-card">
                <div class="icon">🎯</div>
                <div class="number">{active_features}</div>
                <div class="label">活跃功能</div>
            </div>
        </div>
        
        <div class="content-grid">
            {content_sections}
        </div>
        
        <div class="footer">
            <p>🤖 由 GitHub Actions 自动生成 | 数据来源: 多个技术媒体和API</p>
            <p>⭐ <a href="https://github.com/your-username/tech-insights" style="color: white;">Star this project on GitHub</a></p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_section_html(self, title, icon, items, item_type="news"):
        """生成内容区块的HTML"""
        items_html = ""
        
        if item_type == "news":
            for item in items[:5]:  # 只显示前5条
                items_html += f"""
                <div class="news-item">
                    <h3><a href="{item.get('url', '#')}" target="_blank">{item.get('title', 'No title')}</a></h3>
                    <p>{item.get('description', 'No description')[:100]}...</p>
                </div>
                """
        elif item_type == "trends":
            for item in items[:5]:
                change_class = "trend-up" if "+" in str(item.get('change', '')) else "trend-down"
                items_html += f"""
                <div class="trend-item">
                    <span class="trend-name">{item.get('keyword', 'Unknown')} {item.get('trend', '')}</span>
                    <span class="trend-change {change_class}">{item.get('change', 'N/A')}</span>
                </div>
                """
        elif item_type == "tools":
            for item in items[:3]:
                items_html += f"""
                <div class="news-item">
                    <h3><a href="{item.get('url', '#')}" target="_blank">{item.get('name', 'Unknown')}</a></h3>
                    <span class="badge">{item.get('category', 'Tool')}</span>
                    <p>{item.get('description', 'No description')}</p>
                </div>
                """
        
        return f"""
        <div class="section-card">
            <h2>{icon} {title}</h2>
            {items_html}
        </div>
        """
    
    def generate_html_page(self, data):
        """生成完整的HTML页面"""
        # 统计数据
        stats = {
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_news': len(data.get('ai_news', [])) + len(data.get('tech_news', [])),
            'hot_topics': len(data.get('tech_trends', [])),
            'trending_repos': len(data.get('github_repos', [])),
            'active_features': 15
        }
        
        # 生成内容区块
        sections = []
        
        if data.get('ai_news'):
            sections.append(self.generate_section_html("AI 技术动态", "🤖", data['ai_news']))
        
        if data.get('tech_news'):
            sections.append(self.generate_section_html("科技热点", "🔥", data['tech_news']))
        
        if data.get('tech_trends'):
            sections.append(self.generate_section_html("技术热词趋势", "📈", data['tech_trends'], "trends"))
        
        if data.get('dev_tools'):
            sections.append(self.generate_section_html("开发者工具", "🛠️", data['dev_tools'], "tools"))
        
        if data.get('github_repos'):
            sections.append(self.generate_section_html("GitHub 趋势", "📊", data['github_repos']))
        
        # 填充模板
        html_content = self.template.format(
            content_sections='\n'.join(sections),
            **stats
        )
        
        return html_content
    
    def save_html_file(self, html_content, filename="index.html"):
        """保存HTML文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML文件已生成: {filename}")
            return True
        except Exception as e:
            print(f"保存HTML文件失败: {e}")
            return False

# 创建全局实例
html_generator = HTMLGenerator()
