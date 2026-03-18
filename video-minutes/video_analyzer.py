#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频深度分析模块
提供智能内容理解、章节划分、核心观点提取等功能
"""

import re
from collections import defaultdict
from typing import List, Dict, Tuple, Any


class VideoAnalyzer:
    """视频内容深度分析器"""
    
    def __init__(self):
        # 章节识别关键词
        self.section_markers = {
            'opening': ['开场', '开始', '首先', '前言', '介绍', '大家好', '欢迎'],
            'problem': ['问题', '困扰', '痛点', '难题', '为什么', '怎么回事'],
            'solution': ['方法', '方案', '解决', '技巧', '秘诀', '窍门', '步骤'],
            'example': ['例如', '比如', '案例', '实例', '故事', '来看', '实际'],
            'conclusion': ['总结', '结论', '总之', '综上所述', '最后', '结尾']
        }
        
        # 重要内容指示词
        self.importance_indicators = {
            'critical': ['核心', '关键', '最重要', '必须', '一定', '千万'],
            'warning': ['注意', '警惕', '小心', '避免', '不要', '切记'],
            'emphasis': ['特别', '尤其', '重点', '牢记', '记住', '切记'],
            'contrast': ['但是', '然而', '相反', '不同', '区别', '对比']
        }
    
    def analyze_structure(self, segments: List[Dict], full_text: str) -> Dict[str, Any]:
        """
        分析视频内容结构
        返回章节划分和每个章节的核心内容
        """
        print("[ANALYSIS] Identifying content structure...")
        
        # 1. 识别章节边界
        chapters = self._identify_chapters(segments)
        
        # 2. 提取每个章节的核心观点
        chapter_insights = []
        for i, chapter in enumerate(chapters):
            insights = self._extract_chapter_insights(chapter)
            chapter_insights.append({
                'index': i + 1,
                'title': chapter['title'],
                'time_range': f"{chapter['start_time']} - {chapter['end_time']}",
                'key_points': insights['key_points'],
                'summary': insights['summary']
            })
        
        # 3. 识别整体主题和核心论点
        main_theme = self._identify_main_theme(full_text)
        core_arguments = self._extract_core_arguments(segments)
        
        # 4. 提取实用价值（方法、技巧、建议）
        practical_value = self._extract_practical_value(segments)
        
        print(f"[ANALYSIS] Found {len(chapters)} chapters, {len(core_arguments)} core arguments")
        
        return {
            'main_theme': main_theme,
            'chapters': chapter_insights,
            'core_arguments': core_arguments,
            'practical_value': practical_value,
            'content_type': self._classify_content_type(full_text)
        }
    
    def _identify_chapters(self, segments: List[Dict]) -> List[Dict]:
        """识别视频章节结构"""
        chapters = []
        current_chapter = {
            'title': '开场引入',
            'segments': [],
            'start_idx': 0,
            'type': 'opening'
        }
        
        for i, seg in enumerate(segments):
            text = seg['text'].strip()
            
            # 检测章节转换信号
            transition = self._detect_chapter_transition(text, i)
            
            if transition and current_chapter['segments']:
                # 结束当前章节
                current_chapter['end_idx'] = i - 1
                current_chapter['end_time'] = segments[i-1]['timestamp_str']
                chapters.append(current_chapter)
                
                # 开始新章节
                current_chapter = {
                    'title': transition['title'],
                    'segments': [seg],
                    'start_idx': i,
                    'start_time': seg['timestamp_str'],
                    'type': transition['type']
                }
            else:
                current_chapter['segments'].append(seg)
                if 'start_time' not in current_chapter:
                    current_chapter['start_time'] = seg['timestamp_str']
        
        # 添加最后一个章节
        if current_chapter['segments']:
            current_chapter['end_idx'] = len(segments) - 1
            current_chapter['end_time'] = segments[-1]['timestamp_str']
            chapters.append(current_chapter)
        
        return chapters
    
    def _detect_chapter_transition(self, text: str, position: int) -> Dict:
        """检测章节转换信号"""
        text_lower = text.lower()
        
        # 强转换信号（显式声明）
        strong_signals = [
            (r'(首先|第一|第一点|第一个)', '核心要点一', 'main_point'),
            (r'(其次|第二|第二点|第二个)', '核心要点二', 'main_point'),
            (r'(第三|第三点|第三个)', '核心要点三', 'main_point'),
            (r'(接下来|下面|然后)', '过渡段落', 'transition'),
            (r'(举个例子|比如说|来看案例)', '案例分析', 'example'),
            (r'(最后|总结|综上所述|结尾)', '总结结论', 'conclusion'),
            (r'(方法|技巧|步骤|教程)', '方法技巧', 'method'),
            (r'(重点|核心|关键)', '核心内容', 'key_concept')
        ]
        
        for pattern, title, section_type in strong_signals:
            if re.search(pattern, text):
                return {'title': title, 'type': section_type}
        
        # 弱转换信号（时间/逻辑标记）
        if position > 0 and position % 100 == 0:  # 每约100句话一个自然断点
            return {'title': f'内容段落 {position//100 + 1}', 'type': 'natural'}
        
        return {'title': None, 'type': None}
    
    def _extract_chapter_insights(self, chapter: Dict) -> Dict:
        """提取章节的核心洞察"""
        segments = chapter['segments']
        texts = [s['text'] for s in segments]
        full_text = ' '.join(texts)
        
        # 提取关键句子（包含重要性标记的）
        key_sentences = []
        for seg in segments:
            text = seg['text'].strip()
            score = self._calculate_importance_score(text)
            if score > 2:  # 重要性阈值
                key_sentences.append({
                    'text': text,
                    'timestamp': seg['timestamp_str'],
                    'score': score
                })
        
        # 按重要性排序，取前3个
        key_sentences.sort(key=lambda x: x['score'], reverse=True)
        key_points = key_sentences[:3]
        
        # 生成章节摘要（取前几句+后几句的组合）
        if len(texts) >= 3:
            summary_texts = texts[:2] + ['...'] + texts[-1:]
        else:
            summary_texts = texts
        
        summary = ' '.join(summary_texts)
        if len(summary) > 150:
            summary = summary[:150] + '...'
        
        return {
            'key_points': key_points,
            'summary': summary
        }
    
    def _calculate_importance_score(self, text: str) -> int:
        """计算文本的重要性得分"""
        score = 0
        text_lower = text.lower()
        
        # 检查重要性指示词
        for category, words in self.importance_indicators.items():
            for word in words:
                if word in text_lower:
                    score += 2 if category == 'critical' else 1
        
        # 包含数字和具体信息的句子更有价值
        if re.search(r'\d+', text):
            score += 1
        
        # 长度适中的句子（信息密度高）
        if 20 <= len(text) <= 100:
            score += 1
        
        # 包含结论性词汇
        conclusion_words = ['所以', '因此', '结果是', '结论是', '证明']
        for word in conclusion_words:
            if word in text_lower:
                score += 1
                break
        
        return score
    
    def _identify_main_theme(self, full_text: str) -> Dict[str, Any]:
        """识别视频的主要主题"""
        # 基于关键词频率分析主题
        words = re.findall(r'\b[\u4e00-\u9fa5]{2,8}\b', full_text)
        word_freq = defaultdict(int)
        
        # 过滤常见词，统计专业术语
        stop_words = {'这个', '那个', '我们', '你们', '他们', '就是', '一个', '可以', '所以'}
        for word in words:
            if word not in stop_words and len(word) >= 2:
                word_freq[word] += 1
        
        # 取频率最高的词作为主题关键词
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        theme_keywords = [w[0] for w in top_words]
        
        # 根据开头内容生成主题描述
        first_para = full_text[:200]
        
        return {
            'keywords': theme_keywords,
            'description': f"围绕'{', '.join(theme_keywords[:3])}'展开的深度讲解",
            'opening_hint': first_para[:100] + '...' if len(first_para) > 100 else first_para
        }
    
    def _extract_core_arguments(self, segments: List[Dict]) -> List[Dict]:
        """提取核心论点和论据"""
        arguments = []
        
        # 识别论点模式：[观点] + [理由/证据]
        for i in range(len(segments) - 1):
            current = segments[i]['text'].strip()
            next_text = segments[i + 1]['text'].strip()
            
            # 检测是否是论点陈述
            is_argument = any(marker in current for marker in 
                            ['我认为', '其实', '真相', '事实上', '关键是', '核心'])
            
            if is_argument and len(current) > 15:
                # 寻找支持论据（接下来的几句话）
                evidence = []
                for j in range(i + 1, min(i + 4, len(segments))):
                    ev_text = segments[j]['text'].strip()
                    if len(ev_text) > 10:
                        evidence.append({
                            'text': ev_text,
                            'timestamp': segments[j]['timestamp_str']
                        })
                
                arguments.append({
                    'argument': current,
                    'timestamp': segments[i]['timestamp_str'],
                    'evidence': evidence[:2],  # 最多2个证据
                    'strength': len(evidence)  # 论据强度
                })
        
        # 按强度排序，返回最强的5个论点
        arguments.sort(key=lambda x: x['strength'], reverse=True)
        return arguments[:5]
    
    def _extract_practical_value(self, segments: List[Dict]) -> List[Dict]:
        """提取实用价值（方法、步骤、建议）"""
        practical_items = []
        
        method_patterns = [
            r'(第一步|首先|先).*?([，。]|$)',
            r'(第二步|然后|接着).*?([，。]|$)',
            r'(第三步|接下来|再).*?([，。]|$)',
            r'(使用方法|操作步骤|具体做法).*?([，。]|$)',
            r'(建议|推荐|最好|应该).*?([，。]|$)',
            r'(记住|牢记|注意).*?([，。]|$)'
        ]
        
        for seg in segments:
            text = seg['text'].strip()
            
            for pattern in method_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    practical_items.append({
                        'content': text,
                        'timestamp': seg['timestamp_str'],
                        'type': 'method' if '步骤' in text or '第' in text else 'advice'
                    })
                    break
        
        # 去重并按时间排序
        seen = set()
        unique_items = []
        for item in practical_items:
            if item['content'] not in seen:
                seen.add(item['content'])
                unique_items.append(item)
        
        return unique_items[:10]  # 最多返回10个实用要点
    
    def _classify_content_type(self, full_text: str) -> str:
        """分类视频内容类型"""
        # 根据关键词判断内容类型
        indicators = {
            'tutorial': ['教程', '教学', '学习', '怎么', '如何', '方法', '步骤'],
            'lecture': ['讲解', '介绍', '分析', '说明', '阐述', '分享'],
            'review': ['评测', '测评', '对比', '测试', '体验'],
            'story': ['故事', '经历', '案例', '曾经', '当年'],
            'news': ['新闻', '报道', '最新消息', '今天', '近日']
        }
        
        scores = {k: 0 for k in indicators}
        for content_type, words in indicators.items():
            for word in words:
                scores[content_type] += full_text.count(word)
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def generate_executive_summary(self, analysis: Dict) -> str:
        """生成执行摘要（高层总结）"""
        content_type_names = {
            'tutorial': '教学教程',
            'lecture': '知识讲解',
            'review': '评测分析',
            'story': '案例故事',
            'news': '资讯报道'
        }
        
        content_type = content_type_names.get(analysis['content_type'], '内容分享')
        theme = analysis['main_theme']
        
        summary = f"## 内容概述\n\n"
        summary += f"**类型**: {content_type}  "
        summary += f"**主题**: {theme['description']}\n\n"
        summary += f"**关键词**: {', '.join(theme['keywords'])}\n\n"
        
        summary += f"**视频主旨**: "
        
        # 根据核心论点生成主旨
        if analysis['core_arguments']:
            main_arg = analysis['core_arguments'][0]['argument']
            summary += f"视频围绕{theme['keywords'][0] if theme['keywords'] else '核心主题'}展开，"
            summary += f"主要阐述'{main_arg[:50]}...'等观点。\n\n"
        else:
            summary += f"视频系统性地讲解了{theme['keywords'][0] if theme['keywords'] else '相关主题'}的内容。\n\n"
        
        return summary
