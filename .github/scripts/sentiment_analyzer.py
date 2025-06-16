"""
技术新闻情感分析和热度评分模块
"""

import re
import random
from datetime import datetime

class TechSentimentAnalyzer:
    def __init__(self):
        # 积极词汇
        self.positive_keywords = [
            '突破', '创新', '提升', '优化', '成功', '领先', '革命性', '高效',
            '强大', '卓越', '先进', '智能', '便捷', '安全', '稳定', '快速',
            '发布', '推出', '升级', '改进', '增强', '扩展', '开源', '免费'
        ]
        
        # 消极词汇
        self.negative_keywords = [
            '漏洞', '攻击', '泄露', '故障', '问题', '风险', '威胁', '危险',
            '下降', '减少', '失败', '错误', '缺陷', '延迟', '停机', '崩溃',
            '警告', '限制', '禁止', '取消', '关闭', '删除', '移除', '废弃'
        ]
        
        # 技术热词权重
        self.tech_hotwords = {
            'AI': 10, '人工智能': 10, '机器学习': 8, '深度学习': 8,
            '区块链': 6, '云计算': 7, '大数据': 6, '物联网': 5,
            '5G': 7, '量子计算': 9, '边缘计算': 6, '自动驾驶': 8,
            'ChatGPT': 9, 'GPT': 9, 'OpenAI': 8, '神经网络': 7,
            'Kubernetes': 6, 'Docker': 5, '微服务': 6, 'DevOps': 5,
            '网络安全': 7, '数据安全': 6, '隐私保护': 6, '零信任': 7,
            'Web3': 8, 'NFT': 4, '元宇宙': 5, 'VR': 6, 'AR': 6,
            '芯片': 8, '半导体': 7, '新能源': 6, '电动车': 7
        }
    
    def analyze_sentiment(self, text):
        """分析文本情感"""
        if not text:
            return {'score': 0, 'sentiment': 'neutral'}
        
        text = text.lower()
        positive_count = sum(1 for word in self.positive_keywords if word in text)
        negative_count = sum(1 for word in self.negative_keywords if word in text)
        
        # 计算情感分数 (-1 到 1)
        total_words = len(text.split())
        if total_words == 0:
            return {'score': 0, 'sentiment': 'neutral'}
        
        score = (positive_count - negative_count) / max(total_words / 10, 1)
        score = max(-1, min(1, score))  # 限制在-1到1之间
        
        if score > 0.2:
            sentiment = 'positive'
        elif score < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'score': round(score, 2),
            'sentiment': sentiment,
            'positive_words': positive_count,
            'negative_words': negative_count
        }
    
    def calculate_hotness_score(self, title, description=""):
        """计算新闻热度分数"""
        text = (title + " " + description).lower()
        hotness_score = 0
        matched_keywords = []
        
        for keyword, weight in self.tech_hotwords.items():
            if keyword.lower() in text:
                hotness_score += weight
                matched_keywords.append(keyword)
        
        # 基于关键词数量的额外加分
        if len(matched_keywords) > 1:
            hotness_score += len(matched_keywords) * 2
        
        # 基于文本长度的调整
        text_length_factor = min(len(text) / 100, 2)  # 最多2倍加成
        hotness_score *= text_length_factor
        
        return {
            'score': min(100, int(hotness_score)),  # 最高100分
            'keywords': matched_keywords,
            'level': self._get_hotness_level(hotness_score)
        }
    
    def _get_hotness_level(self, score):
        """根据分数获取热度等级"""
        if score >= 50:
            return '🔥🔥🔥 超热'
        elif score >= 30:
            return '🔥🔥 很热'
        elif score >= 15:
            return '🔥 热门'
        elif score >= 5:
            return '📈 关注'
        else:
            return '📊 普通'
    
    def analyze_news_batch(self, news_list):
        """批量分析新闻"""
        analyzed_news = []
        
        for news in news_list:
            title = news.get('title', '')
            description = news.get('description', '')
            
            sentiment = self.analyze_sentiment(title + " " + description)
            hotness = self.calculate_hotness_score(title, description)
            
            analyzed_news.append({
                **news,
                'sentiment': sentiment,
                'hotness': hotness,
                'analysis_time': datetime.now().isoformat()
            })
        
        # 按热度排序
        analyzed_news.sort(key=lambda x: x['hotness']['score'], reverse=True)
        return analyzed_news
    
    def generate_trend_summary(self, analyzed_news):
        """生成趋势摘要"""
        if not analyzed_news:
            return "暂无新闻数据进行分析"
        
        total_news = len(analyzed_news)
        positive_news = len([n for n in analyzed_news if n['sentiment']['sentiment'] == 'positive'])
        negative_news = len([n for n in analyzed_news if n['sentiment']['sentiment'] == 'negative'])
        
        # 统计热门关键词
        all_keywords = []
        for news in analyzed_news:
            all_keywords.extend(news['hotness']['keywords'])
        
        keyword_count = {}
        for keyword in all_keywords:
            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 计算平均热度
        avg_hotness = sum(n['hotness']['score'] for n in analyzed_news) / total_news
        
        summary = f"""
📊 **今日技术新闻分析报告**

- 📰 新闻总数: {total_news}
- 😊 积极新闻: {positive_news} ({positive_news/total_news*100:.1f}%)
- 😟 消极新闻: {negative_news} ({negative_news/total_news*100:.1f}%)
- 🔥 平均热度: {avg_hotness:.1f}/100

🏷️ **热门关键词**:
"""
        
        for keyword, count in top_keywords:
            summary += f"- {keyword} ({count}次)\n"
        
        return summary.strip()
    
    def get_sentiment_emoji(self, sentiment):
        """根据情感获取表情符号"""
        emoji_map = {
            'positive': '😊',
            'negative': '😟',
            'neutral': '😐'
        }
        return emoji_map.get(sentiment, '😐')

# 创建全局分析器实例
sentiment_analyzer = TechSentimentAnalyzer()
