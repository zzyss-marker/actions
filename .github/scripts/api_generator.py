"""
API数据生成器 - 为技术视野助手生成JSON API数据
"""

import json
import os
from datetime import datetime

class APIGenerator:
    def __init__(self):
        self.api_version = "1.0"
        self.base_structure = {
            "meta": {
                "version": self.api_version,
                "generated_at": "",
                "update_frequency": "daily",
                "next_update": "",
                "total_sources": 0,
                "status": "active"
            },
            "data": {},
            "statistics": {},
            "endpoints": {
                "all": "/api/all.json",
                "ai_news": "/api/ai_news.json",
                "tech_news": "/api/tech_news.json",
                "security_news": "/api/security_news.json",
                "github_trending": "/api/github_trending.json",
                "tech_trends": "/api/tech_trends.json",
                "dev_tools": "/api/dev_tools.json"
            }
        }
    
    def generate_api_data(self, data_dict):
        """生成完整的API数据结构"""
        current_time = datetime.now()
        
        api_data = self.base_structure.copy()
        api_data["meta"]["generated_at"] = current_time.isoformat()
        api_data["meta"]["next_update"] = current_time.replace(
            hour=8, minute=0, second=0, microsecond=0
        ).isoformat()
        
        # 统计信息
        stats = {
            "total_news": 0,
            "ai_news_count": len(data_dict.get('ai_news', [])),
            "tech_news_count": len(data_dict.get('tech_news', [])),
            "security_news_count": len(data_dict.get('security_news', [])),
            "github_repos_count": len(data_dict.get('github_repos', [])),
            "tech_trends_count": len(data_dict.get('tech_trends', [])),
            "dev_tools_count": len(data_dict.get('dev_tools', [])),
            "sentiment_analysis": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
        }
        
        stats["total_news"] = (stats["ai_news_count"] + 
                              stats["tech_news_count"] + 
                              stats["security_news_count"])
        
        api_data["statistics"] = stats
        api_data["data"] = data_dict
        api_data["meta"]["total_sources"] = len([k for k in data_dict.keys() if data_dict[k]])
        
        return api_data
    
    def save_api_files(self, data_dict):
        """保存各种API文件"""
        # 确保API目录存在
        api_dir = "docs/api"
        os.makedirs(api_dir, exist_ok=True)
        
        # 生成主API文件
        main_api_data = self.generate_api_data(data_dict)
        self.save_json_file(main_api_data, f"{api_dir}/all.json")
        
        # 生成分类API文件
        categories = {
            "ai_news": "AI技术动态",
            "tech_news": "科技热点",
            "security_news": "网络安全资讯",
            "github_repos": "GitHub趋势项目",
            "tech_trends": "技术热词趋势",
            "dev_tools": "开发者工具推荐"
        }
        
        for category, title in categories.items():
            if category in data_dict and data_dict[category]:
                category_data = {
                    "meta": {
                        "category": category,
                        "title": title,
                        "generated_at": datetime.now().isoformat(),
                        "count": len(data_dict[category])
                    },
                    "data": data_dict[category]
                }
                self.save_json_file(category_data, f"{api_dir}/{category}.json")
        
        # 生成API文档
        self.generate_api_docs(api_dir)
        
        print(f"API文件已生成到 {api_dir} 目录")
    
    def save_json_file(self, data, filepath):
        """保存JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存JSON文件失败 {filepath}: {e}")
            return False
    
    def generate_api_docs(self, api_dir):
        """生成API文档"""
        docs_content = """# 技术视野助手 API 文档

## 概述

技术视野助手提供RESTful API接口，方便开发者获取最新的技术资讯数据。

## 基础信息

- **API版本**: v1.0
- **更新频率**: 每日 08:00 (UTC+8)
- **数据格式**: JSON
- **字符编码**: UTF-8

## 端点列表

### 1. 获取所有数据
```
GET /api/all.json
```
返回所有类别的完整数据，包括元数据和统计信息。

### 2. AI技术动态
```
GET /api/ai_news.json
```
返回最新的AI技术相关新闻和动态。

### 3. 科技热点
```
GET /api/tech_news.json
```
返回科技行业的热点新闻。

### 4. 网络安全资讯
```
GET /api/security_news.json
```
返回网络安全相关的资讯和警报。

### 5. GitHub趋势项目
```
GET /api/github_repos.json
```
返回GitHub上的趋势开源项目。

### 6. 技术热词趋势
```
GET /api/tech_trends.json
```
返回技术关键词的热度趋势分析。

### 7. 开发者工具推荐
```
GET /api/dev_tools.json
```
返回推荐的开发者工具和资源。

## 数据结构

### 主API响应结构
```json
{
  "meta": {
    "version": "1.0",
    "generated_at": "2025-06-16T08:00:00",
    "update_frequency": "daily",
    "next_update": "2025-06-17T08:00:00",
    "total_sources": 6,
    "status": "active"
  },
  "data": {
    "ai_news": [...],
    "tech_news": [...],
    "security_news": [...],
    "github_repos": [...],
    "tech_trends": [...],
    "dev_tools": [...]
  },
  "statistics": {
    "total_news": 15,
    "ai_news_count": 5,
    "tech_news_count": 5,
    "security_news_count": 5,
    "github_repos_count": 5,
    "tech_trends_count": 5,
    "dev_tools_count": 3
  },
  "endpoints": {
    "all": "/api/all.json",
    "ai_news": "/api/ai_news.json",
    ...
  }
}
```

### 新闻项目结构
```json
{
  "title": "新闻标题",
  "url": "https://example.com/news",
  "description": "新闻描述",
  "sentiment": {
    "score": 0.5,
    "sentiment": "positive"
  },
  "hotness": {
    "score": 75,
    "level": "🔥🔥 很热"
  }
}
```

## 使用示例

### JavaScript
```javascript
// 获取所有数据
fetch('/api/all.json')
  .then(response => response.json())
  .then(data => {
    console.log('总新闻数:', data.statistics.total_news);
    console.log('AI新闻:', data.data.ai_news);
  });

// 获取特定类别
fetch('/api/ai_news.json')
  .then(response => response.json())
  .then(data => {
    console.log('AI新闻数量:', data.meta.count);
    data.data.forEach(news => {
      console.log(news.title);
    });
  });
```

### Python
```python
import requests

# 获取所有数据
response = requests.get('https://your-domain.com/api/all.json')
data = response.json()

print(f"总新闻数: {data['statistics']['total_news']}")
for news in data['data']['ai_news']:
    print(f"- {news['title']}")
```

### cURL
```bash
# 获取所有数据
curl -X GET "https://your-domain.com/api/all.json"

# 获取AI新闻
curl -X GET "https://your-domain.com/api/ai_news.json"
```

## 错误处理

API使用标准HTTP状态码：

- `200 OK`: 请求成功
- `404 Not Found`: 端点不存在
- `500 Internal Server Error`: 服务器错误

## 限制和注意事项

1. **更新频率**: 数据每日更新一次
2. **缓存**: 建议客户端缓存数据，避免频繁请求
3. **CORS**: API支持跨域请求
4. **免费使用**: 当前API完全免费，无需认证

## 联系方式

如有问题或建议，请通过GitHub Issues联系我们。

---

*最后更新: {update_time}*
""".format(update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        try:
            with open(f"{api_dir}/README.md", 'w', encoding='utf-8') as f:
                f.write(docs_content)
            print("API文档已生成")
        except Exception as e:
            print(f"生成API文档失败: {e}")

# 创建全局实例
api_generator = APIGenerator()
