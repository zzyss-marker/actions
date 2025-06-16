"""
RSS订阅生成器 - 为技术视野助手生成RSS订阅源
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import html

class RSSGenerator:
    def __init__(self):
        self.channel_info = {
            'title': '技术视野助手',
            'description': '每日技术资讯聚合，AI驱动的技术新闻和趋势分析',
            'link': 'https://zzyss-marker.github.io/actions',
            'language': 'zh-CN',
            'copyright': 'Copyright 2025 技术视野助手',
            'managingEditor': 'tech-insights@example.com',
            'webMaster': 'tech-insights@example.com',
            'category': 'Technology',
            'generator': '技术视野助手 RSS Generator v1.0',
            'docs': 'https://www.rssboard.org/rss-specification',
            'ttl': '60'  # 缓存时间（分钟）
        }
    
    def create_rss_feed(self, items, feed_title=None, feed_description=None):
        """创建RSS订阅源"""
        # 创建根元素
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        
        # 创建channel元素
        channel = ET.SubElement(rss, 'channel')
        
        # 添加channel信息
        title = feed_title or self.channel_info['title']
        description = feed_description or self.channel_info['description']
        
        ET.SubElement(channel, 'title').text = title
        ET.SubElement(channel, 'description').text = description
        ET.SubElement(channel, 'link').text = self.channel_info['link']
        ET.SubElement(channel, 'language').text = self.channel_info['language']
        ET.SubElement(channel, 'copyright').text = self.channel_info['copyright']
        ET.SubElement(channel, 'managingEditor').text = self.channel_info['managingEditor']
        ET.SubElement(channel, 'webMaster').text = self.channel_info['webMaster']
        ET.SubElement(channel, 'category').text = self.channel_info['category']
        ET.SubElement(channel, 'generator').text = self.channel_info['generator']
        ET.SubElement(channel, 'docs').text = self.channel_info['docs']
        ET.SubElement(channel, 'ttl').text = self.channel_info['ttl']
        
        # 添加构建日期
        build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'lastBuildDate').text = build_date
        ET.SubElement(channel, 'pubDate').text = build_date
        
        # 添加atom:link自引用
        atom_link = ET.SubElement(channel, 'atom:link')
        atom_link.set('href', f"{self.channel_info['link']}/rss.xml")
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')
        
        # 添加图片
        image = ET.SubElement(channel, 'image')
        ET.SubElement(image, 'url').text = f"{self.channel_info['link']}/assets/logo.png"
        ET.SubElement(image, 'title').text = title
        ET.SubElement(image, 'link').text = self.channel_info['link']
        ET.SubElement(image, 'width').text = '144'
        ET.SubElement(image, 'height').text = '144'
        
        # 添加新闻项目
        for item_data in items[:20]:  # 限制为最新20条
            item = ET.SubElement(channel, 'item')
            
            # 基本信息
            ET.SubElement(item, 'title').text = html.escape(item_data.get('title', '无标题'))
            ET.SubElement(item, 'link').text = item_data.get('url', '#')
            ET.SubElement(item, 'guid').text = item_data.get('url', f"#{hash(item_data.get('title', ''))}")
            
            # 描述
            description = item_data.get('description', '无描述')
            ET.SubElement(item, 'description').text = html.escape(description)
            
            # 内容（如果有的话）
            if 'content' in item_data:
                content_elem = ET.SubElement(item, 'content:encoded')
                content_elem.text = f"<![CDATA[{item_data['content']}]]>"
            
            # 发布日期
            pub_date = item_data.get('pub_date', datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000'))
            ET.SubElement(item, 'pubDate').text = pub_date
            
            # 分类
            if 'category' in item_data:
                ET.SubElement(item, 'category').text = item_data['category']
            
            # 作者
            if 'author' in item_data:
                ET.SubElement(item, 'author').text = item_data['author']
            
            # 情感分析和热度（如果有的话）
            if 'sentiment' in item_data or 'hotness' in item_data:
                comments = []
                if 'sentiment' in item_data:
                    sentiment = item_data['sentiment']
                    comments.append(f"情感: {sentiment.get('sentiment', 'neutral')} ({sentiment.get('score', 0)})")
                if 'hotness' in item_data:
                    hotness = item_data['hotness']
                    comments.append(f"热度: {hotness.get('score', 0)}/100 {hotness.get('level', '')}")
                
                if comments:
                    ET.SubElement(item, 'comments').text = ' | '.join(comments)
        
        return rss
    
    def generate_category_feeds(self, data_dict):
        """生成分类RSS订阅源"""
        feeds = {}
        
        categories = {
            'ai_news': ('AI技术动态', 'AI技术相关的最新动态和新闻'),
            'tech_news': ('科技热点', '科技行业的热点新闻和趋势'),
            'security_news': ('网络安全资讯', '网络安全相关的资讯和警报'),
            'github_repos': ('GitHub趋势', 'GitHub上的热门开源项目'),
        }
        
        for category, (title, desc) in categories.items():
            if category in data_dict and data_dict[category]:
                # 为RSS格式化数据
                rss_items = []
                for item in data_dict[category]:
                    rss_item = {
                        'title': item.get('title', item.get('name', '无标题')),
                        'url': item.get('url', '#'),
                        'description': item.get('description', '无描述'),
                        'category': title,
                        'pub_date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                    }
                    
                    # 添加情感分析和热度信息
                    if 'sentiment' in item:
                        rss_item['sentiment'] = item['sentiment']
                    if 'hotness' in item:
                        rss_item['hotness'] = item['hotness']
                    
                    rss_items.append(rss_item)
                
                feeds[category] = self.create_rss_feed(rss_items, title, desc)
        
        return feeds
    
    def save_rss_files(self, data_dict):
        """保存RSS文件"""
        # 确保RSS目录存在
        import os
        rss_dir = "docs/rss"
        os.makedirs(rss_dir, exist_ok=True)
        
        # 生成主RSS文件（包含所有新闻）
        all_items = []
        for category in ['ai_news', 'tech_news', 'security_news']:
            if category in data_dict and data_dict[category]:
                for item in data_dict[category]:
                    rss_item = {
                        'title': item.get('title', '无标题'),
                        'url': item.get('url', '#'),
                        'description': item.get('description', '无描述'),
                        'category': category.replace('_', ' ').title(),
                        'pub_date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                    }
                    
                    if 'sentiment' in item:
                        rss_item['sentiment'] = item['sentiment']
                    if 'hotness' in item:
                        rss_item['hotness'] = item['hotness']
                    
                    all_items.append(rss_item)
        
        # 按时间排序（最新的在前）
        all_items.sort(key=lambda x: x['pub_date'], reverse=True)
        
        # 生成主RSS文件
        main_rss = self.create_rss_feed(all_items)
        self.save_xml_file(main_rss, f"{rss_dir}/all.xml")
        
        # 生成分类RSS文件
        category_feeds = self.generate_category_feeds(data_dict)
        for category, feed in category_feeds.items():
            self.save_xml_file(feed, f"{rss_dir}/{category}.xml")
        
        # 生成RSS索引页面
        self.generate_rss_index(rss_dir, category_feeds.keys())
        
        print(f"RSS文件已生成到 {rss_dir} 目录")
    
    def save_xml_file(self, xml_element, filepath):
        """保存XML文件"""
        try:
            # 格式化XML
            self.indent_xml(xml_element)
            
            # 创建XML声明
            xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
            xml_str += ET.tostring(xml_element, encoding='unicode')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            return True
        except Exception as e:
            print(f"保存RSS文件失败 {filepath}: {e}")
            return False
    
    def indent_xml(self, elem, level=0):
        """格式化XML缩进"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def generate_rss_index(self, rss_dir, categories):
        """生成RSS索引页面"""
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS订阅 - 技术视野助手</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .rss-item {{ background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; }}
        .rss-item h3 {{ color: #333; margin-bottom: 10px; }}
        .rss-item a {{ color: #007bff; text-decoration: none; }}
        .rss-item a:hover {{ text-decoration: underline; }}
        .copy-btn {{ background: #28a745; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-left: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 技术视野助手 RSS 订阅</h1>
        <p>选择您感兴趣的RSS订阅源，获取最新的技术资讯。</p>
        
        <div class="rss-item">
            <h3>📰 全部资讯</h3>
            <p>包含所有类别的技术资讯</p>
            <a href="all.xml">all.xml</a>
            <button class="copy-btn" onclick="copyToClipboard('{self.channel_info['link']}/rss/all.xml')">复制链接</button>
        </div>
"""
        
        category_names = {
            'ai_news': ('🤖 AI技术动态', 'AI技术相关的最新动态和新闻'),
            'tech_news': ('🔥 科技热点', '科技行业的热点新闻和趋势'),
            'security_news': ('🔒 网络安全资讯', '网络安全相关的资讯和警报'),
            'github_repos': ('📊 GitHub趋势', 'GitHub上的热门开源项目')
        }
        
        for category in categories:
            if category in category_names:
                name, desc = category_names[category]
                index_html += f"""
        <div class="rss-item">
            <h3>{name}</h3>
            <p>{desc}</p>
            <a href="{category}.xml">{category}.xml</a>
            <button class="copy-btn" onclick="copyToClipboard('{self.channel_info['link']}/rss/{category}.xml')">复制链接</button>
        </div>
"""
        
        index_html += """
    </div>
    
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('RSS链接已复制到剪贴板！');
            });
        }
    </script>
</body>
</html>"""
        
        try:
            with open(f"{rss_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(index_html)
            print("RSS索引页面已生成")
        except Exception as e:
            print(f"生成RSS索引页面失败: {e}")

# 创建全局实例
rss_generator = RSSGenerator()
