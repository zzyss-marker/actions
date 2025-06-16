"""
互动功能模块 - 为技术视野助手添加更多互动元素
"""

import random
import json
from datetime import datetime, timedelta
import hashlib

class InteractiveFeatures:
    def __init__(self):
        self.weekly_challenges = self.load_weekly_challenges()
        self.tech_polls = self.load_tech_polls()
        self.achievement_system = self.load_achievements()
    
    def load_weekly_challenges(self):
        """加载每周技术挑战"""
        challenges = [
            {
                "week": 1,
                "title": "算法优化挑战",
                "description": "优化一个排序算法，使其在大数据集上的性能提升50%",
                "difficulty": "中等",
                "tags": ["算法", "性能优化"],
                "reward_points": 100,
                "estimated_time": "2-4小时"
            },
            {
                "week": 2,
                "title": "微服务架构设计",
                "description": "设计一个电商系统的微服务架构，包含用户、订单、支付等服务",
                "difficulty": "高级",
                "tags": ["架构设计", "微服务"],
                "reward_points": 150,
                "estimated_time": "4-8小时"
            },
            {
                "week": 3,
                "title": "AI模型部署",
                "description": "将一个机器学习模型部署到云端，实现API调用",
                "difficulty": "中等",
                "tags": ["AI", "部署", "云计算"],
                "reward_points": 120,
                "estimated_time": "3-6小时"
            },
            {
                "week": 4,
                "title": "安全漏洞修复",
                "description": "识别并修复一个Web应用中的安全漏洞",
                "difficulty": "高级",
                "tags": ["安全", "Web开发"],
                "reward_points": 130,
                "estimated_time": "2-5小时"
            }
        ]
        return challenges
    
    def load_tech_polls(self):
        """加载技术投票话题"""
        polls = [
            {
                "question": "2025年最值得学习的编程语言是？",
                "options": ["Rust", "Go", "TypeScript", "Python", "Kotlin"],
                "category": "编程语言"
            },
            {
                "question": "最喜欢的代码编辑器是？",
                "options": ["VS Code", "IntelliJ IDEA", "Vim", "Sublime Text", "Atom"],
                "category": "开发工具"
            },
            {
                "question": "云服务提供商首选？",
                "options": ["AWS", "Azure", "Google Cloud", "阿里云", "腾讯云"],
                "category": "云计算"
            },
            {
                "question": "前端框架的未来趋势？",
                "options": ["React", "Vue.js", "Angular", "Svelte", "Solid.js"],
                "category": "前端开发"
            }
        ]
        return polls
    
    def load_achievements(self):
        """加载成就系统"""
        achievements = [
            {
                "id": "early_bird",
                "name": "早起的鸟儿",
                "description": "连续7天在早上8点前查看技术资讯",
                "icon": "🐦",
                "points": 50
            },
            {
                "id": "knowledge_seeker",
                "name": "知识探索者",
                "description": "阅读了100篇技术文章",
                "icon": "📚",
                "points": 100
            },
            {
                "id": "trend_follower",
                "name": "趋势追随者",
                "description": "关注了50个GitHub趋势项目",
                "icon": "📈",
                "points": 75
            },
            {
                "id": "security_expert",
                "name": "安全专家",
                "description": "完成了10个安全相关的挑战",
                "icon": "🔒",
                "points": 150
            }
        ]
        return achievements
    
    def get_current_week_challenge(self):
        """获取当前周的挑战"""
        # 基于当前日期计算周数
        current_date = datetime.now()
        week_number = current_date.isocalendar()[1] % len(self.weekly_challenges)
        return self.weekly_challenges[week_number]
    
    def get_random_poll(self):
        """获取随机投票话题"""
        return random.choice(self.tech_polls)
    
    def generate_tech_quiz(self):
        """生成技术小测验"""
        quizzes = [
            {
                "question": "以下哪个不是Python的特性？",
                "options": ["动态类型", "解释执行", "静态编译", "面向对象"],
                "correct": 2,
                "explanation": "Python是解释型语言，不需要静态编译"
            },
            {
                "question": "REST API中，PUT和PATCH的主要区别是？",
                "options": ["没有区别", "PUT用于完整更新，PATCH用于部分更新", "PUT更安全", "PATCH更快"],
                "correct": 1,
                "explanation": "PUT通常用于完整资源更新，PATCH用于部分更新"
            },
            {
                "question": "Docker容器和虚拟机的主要区别是？",
                "options": ["容器更重", "容器共享宿主机内核", "虚拟机更快", "没有区别"],
                "correct": 1,
                "explanation": "Docker容器共享宿主机内核，而虚拟机有独立的操作系统"
            }
        ]
        return random.choice(quizzes)
    
    def get_coding_tip_of_day(self):
        """获取每日编程小贴士"""
        tips = [
            {
                "title": "使用有意义的变量名",
                "content": "好的变量名应该能够清楚地表达其用途，避免使用a、b、temp等无意义的名称。",
                "example": "// 好的命名\nconst userAge = 25;\n// 不好的命名\nconst a = 25;"
            },
            {
                "title": "遵循单一职责原则",
                "content": "每个函数应该只做一件事，这样代码更容易理解、测试和维护。",
                "example": "// 好的做法\nfunction calculateTax(amount) { ... }\nfunction formatCurrency(amount) { ... }"
            },
            {
                "title": "使用版本控制",
                "content": "即使是个人项目，也要使用Git等版本控制工具，养成频繁提交的好习惯。",
                "example": "git add .\ngit commit -m \"Add user authentication feature\""
            },
            {
                "title": "写测试用例",
                "content": "测试驱动开发(TDD)能帮助你写出更可靠的代码，减少bug。",
                "example": "// 先写测试\ntest('should calculate tax correctly', () => {\n  expect(calculateTax(100)).toBe(15);\n});"
            }
        ]
        return random.choice(tips)
    
    def get_tech_career_advice(self):
        """获取技术职业建议"""
        advice_list = [
            {
                "category": "技能发展",
                "advice": "专注于深度学习一门技术栈，同时保持对新技术的敏感度",
                "action": "选择一个主要技术方向，每周花2-3小时学习相关新知识"
            },
            {
                "category": "项目经验",
                "advice": "参与开源项目是提升技能和建立声誉的最佳方式",
                "action": "在GitHub上找到感兴趣的项目，从小的issue开始贡献"
            },
            {
                "category": "网络建设",
                "advice": "参加技术会议和meetup，建立专业人脉网络",
                "action": "每月参加至少一次技术聚会或在线会议"
            },
            {
                "category": "持续学习",
                "advice": "技术更新很快，保持学习习惯是职业发展的关键",
                "action": "制定学习计划，每天至少花30分钟学习新技术"
            }
        ]
        return random.choice(advice_list)
    
    def generate_daily_challenge_badge(self):
        """生成每日挑战徽章"""
        today = datetime.now()
        day_hash = hashlib.md5(today.strftime("%Y-%m-%d").encode()).hexdigest()[:6]
        
        badges = [
            {"name": "代码忍者", "emoji": "🥷", "color": "#FF6B6B"},
            {"name": "算法大师", "emoji": "🧠", "color": "#4ECDC4"},
            {"name": "架构师", "emoji": "🏗️", "color": "#45B7D1"},
            {"name": "调试专家", "emoji": "🔍", "color": "#96CEB4"},
            {"name": "性能优化师", "emoji": "⚡", "color": "#FFEAA7"},
            {"name": "安全卫士", "emoji": "🛡️", "color": "#DDA0DD"},
            {"name": "创新者", "emoji": "💡", "color": "#FFB347"}
        ]
        
        # 基于日期哈希选择徽章
        badge_index = int(day_hash, 16) % len(badges)
        selected_badge = badges[badge_index]
        
        return {
            "badge": selected_badge,
            "challenge_id": day_hash,
            "date": today.strftime("%Y-%m-%d"),
            "message": f"今日挑战徽章：{selected_badge['emoji']} {selected_badge['name']}"
        }

# 创建全局实例
interactive_features = InteractiveFeatures()
