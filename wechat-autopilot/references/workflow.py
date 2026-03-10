# WeChat AutoPilot - 公众号自动化工作流程
# 本文件展示完整的自动化流程实现

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# ==================== 配置 ====================
CONFIG = {
    "WECHAT_APP_ID": os.getenv("WECHAT_APP_ID", ""),
    "WECHAT_APP_SECRET": os.getenv("WECHAT_APP_SECRET", ""),
    "IMAGE_API_KEY": os.getenv("IMAGE_API_KEY", ""),
    "IMAGE_MODEL": os.getenv("IMAGE_MODEL", "nanobanana"),
    "IMAGE_STYLE": os.getenv("IMAGE_STYLE", "mondo"),
    "NEWS_KEYWORDS": os.getenv("NEWS_KEYWORDS", "AI,人工智能"),
    "WRITING_STYLE": os.getenv("WRITING_STYLE", "standup"),
    "POST_SCHEDULE": os.getenv("POST_SCHEDULE", "10:00,18:00"),
}

# ==================== 1. 收集资讯 ====================

async def fetch_news(keywords: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    从 Google News RSS 获取资讯
    
    Args:
        keywords: 关键词，逗号分隔
        count: 获取数量
    
    Returns:
        新闻列表，每条包含 title, link, pub_date, summary
    """
    import feedparser
    
    # 构建 Google News RSS URL
    keyword_query = keywords.replace(",", " OR ")
    rss_url = f"https://news.google.com/rss/search?q={keyword_query}&hl=zh-CN&gl=CN&ceid=CN:zh"
    
    # 解析 RSS
    feed = feedparser.parse(rss_url)
    
    news_list = []
    for entry in feed.entries[:count]:
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.get("summary", "")
        })
    
    return news_list


# ==================== 2. AI 生成文章 ====================

async def generate_article(news_list: List[Dict[str, Any]], style: str = "standup") -> Dict[str, str]:
    """
    使用 AI 整理新闻并生成文章
    
    Args:
        news_list: 新闻列表
        style: 写作风格
    
    Returns:
        包含 title, content, summary 的字典
    """
    
    # 构建提示词
    style_prompts = {
        "standup": """模仿脱口秀演员的文风撰写文章：
- 语言犀利、通俗易懂
- 带点幽默和反讽
- 观点明确、立场鲜明
- 用口语化表达复杂概念""",
        
        "news": """以新闻评论风格撰写：
- 客观陈述事实
- 加入深度分析
- 引用多方观点
- 给出独到见解""",
        
        "edu": """以科普教育风格撰写：
- 由浅入深讲解
- 多用类比和例子
- 分点列出要点
- 总结核心结论""",
        
        "biz": """以商业分析风格撰写：
- 聚焦商业价值
- 分析市场机会
- 引用数据和案例
- 给出行动建议"""
    }
    
    # 整理新闻要点
    news_summary = "\n".join([
        f"{i+1}. {news['title']} - {news.get('summary', '')[:100]}..."
        for i, news in enumerate(news_list[:5])
    ])
    
    # 构建完整提示词
    prompt = f"""基于以下新闻资讯，撰写一篇公众号文章：

{news_summary}

写作要求：
{style_prompts.get(style, style_prompts["standup"])}

输出格式要求：
1. 标题：吸引人点击的标题（20-30字）
2. 导语：100字以内的引言，概括核心观点
3. 正文：800-1200字，分3-4个小节
4. 结尾：总结+引发讨论的问题
5. 推荐配图描述：2-3句画面描述，用于AI生图

请直接输出文章内容，无需额外说明。"""

    # 这里调用 AI 生成内容
    # 实际使用时替换为具体的 AI API 调用
    
    return {
        "title": "示例标题：AI正在改变我们的工作方式",
        "content": "这是文章内容...",
        "summary": "文章摘要...",
        "image_prompts": [
            "现代科技风格，人工智能机器人与人类协作的场景，蓝色调，mondo海报风格",
            "未来办公室场景，AI助手帮助处理文件，暖色调，科技感"
        ]
    }


# ==================== 3. 生成配图 ====================

async def generate_images(prompts: List[str], api_key: str, style: str = "mondo") -> List[str]:
    """
    使用文生图 API 生成配图
    
    Args:
        prompts: 图片描述列表
        api_key: API 密钥
        style: 图片风格
    
    Returns:
        生成的图片 URL 列表
    """
    import aiohttp
    
    image_urls = []
    
    for prompt in prompts:
        # 添加风格修饰
        styled_prompt = f"{prompt}, {style} style, high quality, detailed"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.tuziapi.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "nanobanana",
                    "prompt": styled_prompt,
                    "size": "1024x1024",
                    "n": 1
                }
            ) as response:
                result = await response.json()
                if "data" in result and len(result["data"]) > 0:
                    image_urls.append(result["data"][0]["url"])
    
    return image_urls


# ==================== 4. 发布到公众号 ====================

async def get_access_token(app_id: str, app_secret: str) -> str:
    """获取微信公众号 access_token"""
    import aiohttp
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result.get("access_token", "")


async def upload_image(access_token: str, image_path: str) -> str:
    """上传图片到微信素材库"""
    import aiohttp
    import aiofiles
    
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(image_path, "rb") as f:
            image_data = await f.read()
            
        data = aiohttp.FormData()
        data.add_field("media", image_data, filename="image.jpg", content_type="image/jpeg")
        
        async with session.post(url, data=data) as response:
            result = await response.json()
            return result.get("url", "")  # 返回图片 URL


async def publish_article(
    access_token: str,
    title: str,
    content: str,
    thumb_media_id: str,
    author: str = "",
    digest: str = "",
    content_source_url: str = "",
    need_open_comment: int = 1,
    only_fans_can_comment: int = 0
) -> Dict[str, Any]:
    """
    发布图文消息到公众号
    
    Args:
        access_token: 微信 API access token
        title: 文章标题
        content: 图文消息具体内容（HTML格式）
        thumb_media_id: 封面图片素材 ID
        author: 作者
        digest: 图文消息的摘要
        content_source_url: 原文链接
        need_open_comment: 是否打开评论（1打开，0不打开）
        only_fans_can_comment: 是否粉丝才可评论（1是，0否）
    
    Returns:
        发布结果
    """
    import aiohttp
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 构建文章内容
    # 需要将普通 HTML 转换为微信支持的格式
    wechat_content = content.replace(
        "<img", '<img style="max-width:100%;"'
    )
    
    payload = {
        "articles": [{
            "title": title,
            "author": author,
            "digest": digest,
            "content": wechat_content,
            "content_source_url": content_source_url,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": need_open_comment,
            "only_fans_can_comment": only_fans_can_comment
        }]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()


# ==================== 5. 主流程 ====================

async def run_autopilot():
    """运行完整的自动化流程"""
    
    print("🚀 WeChat AutoPilot 启动")
    print("=" * 50)
    
    # 1. 收集资讯
    print("\n📰 正在收集资讯...")
    keywords = CONFIG["NEWS_KEYWORDS"]
    news_list = await fetch_news(keywords, count=10)
    print(f"✅ 获取到 {len(news_list)} 条新闻")
    
    # 2. 生成文章
    print("\n✍️ 正在生成文章...")
    article = await generate_article(news_list, style=CONFIG["WRITING_STYLE"])
    print(f"✅ 文章生成完成：{article['title']}")
    
    # 3. 生成配图
    print("\n🎨 正在生成配图...")
    image_prompts = article.get("image_prompts", [])
    if CONFIG.get("IMAGE_API_KEY"):
        image_urls = await generate_images(
            image_prompts,
            CONFIG["IMAGE_API_KEY"],
            CONFIG["IMAGE_STYLE"]
        )
        print(f"✅ 生成 {len(image_urls)} 张配图")
    else:
        print("⚠️ 未配置图片 API，跳过配图生成")
        image_urls = []
    
    # 4. 发布到公众号
    print("\n📤 正在发布到公众号...")
    if CONFIG.get("WECHAT_APP_ID") and CONFIG.get("WECHAT_APP_SECRET"):
        # 获取 access token
        access_token = await get_access_token(
            CONFIG["WECHAT_APP_ID"],
            CONFIG["WECHAT_APP_SECRET"]
        )
        
        # 如果有图片，先上传封面图
        thumb_media_id = ""
        if image_urls:
            # 下载并上传封面图
            # thumb_media_id = await upload_image(access_token, image_path)
            pass
        
        # 发布文章
        result = await publish_article(
            access_token=access_token,
            title=article["title"],
            content=article["content"],
            thumb_media_id=thumb_media_id,
            digest=article.get("summary", "")
        )
        
        if result.get("errcode") == 0:
            print("✅ 文章发布成功！")
        else:
            print(f"❌ 发布失败：{result.get('errmsg', '未知错误')}")
    else:
        print("⚠️ 未配置微信 API，跳过发布")
    
    print("\n" + "=" * 50)
    print("✨ 流程执行完成")
    
    return article


# ==================== 定时任务 ====================

async def schedule_daily():
    """设置每日定时任务"""
    import schedule
    import time
    
    schedule_times = CONFIG["POST_SCHEDULE"].split(",")
    
    for post_time in schedule_times:
        schedule.every().day.at(post_time.strip()).do(lambda: asyncio.create_task(run_autopilot()))
        print(f"⏰ 已设置定时任务：每天 {post_time.strip()}")
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


# ==================== 入口 ====================

if __name__ == "__main__":
    # 运行一次
    asyncio.run(run_autopilot())
    
    # 或者启动定时任务
    # asyncio.run(schedule_daily())
