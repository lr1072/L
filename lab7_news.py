import requests
from datetime import datetime

# ===================== 配置信息 =====================
API_KEY = "2226ef36be6c42d483e0124b85bb396c"  
BASE_URL = "https://newsapi.org/v2/everything"
QUERY = "technology"  
# ===================================================

def get_news():
    """获取新闻数据"""
    params = {
        "q": QUERY,
        "apiKey": API_KEY,
        "language": "en",
        "pageSize": 8,
        "sortBy": "publishedAt"
    }
    
    try:
        print("🌐 正在连接NewsAPI...")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"❌ API错误: {data.get('message', '未知错误')}")
            return None
        return data
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def show_news(data):
    """显示新闻"""
    if not data or "articles" not in data:
        print("没有获取到新闻")
        return
    
    articles = data["articles"]
    total = data.get("totalResults", 0)
    
    print("\n" + "=" * 70)
    print(f"🔍 关键词: {QUERY}")
    print(f"📊 共找到 {total} 条新闻（显示前{len(articles)}条）")
    print("=" * 70)
    
    for i, news in enumerate(articles, 1):
        print(f"\n📰 【新闻 {i}】")
        print("-" * 50)
        
        # 1. 标题
        print(f"标 题: {news.get('title', '无')}")
        
        # 2. 来源
        source = news.get('source', {})
        print(f"来 源: {source.get('name', '未知')}")
        
        # 3. 作者
        if news.get('author'):
            print(f"作 者: {news.get('author')}")
        
        # 4. 时间
        time_str = news.get('publishedAt', '')
        if time_str:
            time_str = time_str.replace('T', ' ').replace('Z', '')[:16]
            print(f"时 间: {time_str}")
        
        # 5. 简介
        desc = news.get('description', '')
        if desc:
            if len(desc) > 60:
                desc = desc[:60] + '...'
            print(f"简 介: {desc}")
        
        # 6. 内容
        content = news.get('content', '')
        if content:
            if len(content) > 50:
                content = content[:50] + '...'
            print(f"内 容: {content}")
        
        # 7. 链接
        print(f"链 接: {news.get('url', '无')}")

def main():
    print("=" * 70)
    print("  实验室工作 №7 — NewsAPI 新闻查询")
    print("=" * 70)
    
    news_data = get_news()
    show_news(news_data)
    
    print("\n" + "=" * 70)
    print("✅ 程序运行完毕")

if __name__ == "__main__":
    main()