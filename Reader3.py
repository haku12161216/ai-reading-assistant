from openai import OpenAI
import streamlit as st
import requests
from bs4 import BeautifulSoup
import trafilatura

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# 页面标题
st.title("🚀 AI Reading Assistant")

#st.write("帮助你快速理解 AI 文章")

# 输入框
url = st.text_input("Enter article URL")

mode = st.selectbox(
    "Select mode",
    [
        "AI 创业",
        "金融投资",
        "科技新闻",
        "学术研究", 
        "美容行业"
    ]
)

# 按钮
# 按钮
if st.button("开始分析"):

    with st.spinner("AI 正在阅读文章..."):

        try:
            # 获取网页
            response = requests.get(url)

            # 提取正文
            downloaded = trafilatura.fetch_url(url)
            article = trafilatura.extract(downloaded)

            # 如果失败，fallback
            if article is None:
                soup = BeautifulSoup(response.text, "html.parser")
                article = soup.get_text()

            # 限制长度
            article = article[:5000]

            # Prompt
            # 根据 mode 选择不同分析师
            if mode == "AI 创业":

                system_prompt = """
你是一位顶级 AI 创业分析师。

请重点分析：

- AI 趋势
- 创业机会
- 商业模式
- 行业变化
- Agent 方向
"""

            elif mode == "金融投资":

                system_prompt = """
你是一位顶级金融投资分析师。

请重点分析：

- 市场影响
- 投资价值
- 商业逻辑
- 风险
- 长期趋势
"""

            elif mode == "科技新闻":

                system_prompt = """
你是一位科技趋势分析师。

请重点分析：

- 技术趋势
- 科技影响
- 产品方向
- 行业变化
- 创新点
"""

            elif mode == "学术研究":

                system_prompt = """
你是一位科研助手。

请重点分析：

- 核心研究内容
- 创新点
- 方法论
- 学术价值
- 未来研究方向
"""

            elif mode == "美容行业":

                system_prompt = """
你是一位顶级美容行业分析师。

请重点分析：

- 美容行业趋势
- 消费者需求
- 产品机会
- 品牌策略
- 社交媒体趋势
- AI 对美容行业的影响
"""

            else:

                system_prompt = """
你是一位专业阅读助手。
"""

            # 最终 Prompt

            prompt = f"""
{system_prompt}

请阅读下面文章。

请使用中文输出。

并严格按照以下格式输出：

# 📰 三句话总结

# 🧠 核心观点

# 📈 行业意义

# 🚀 潜在机会

# ⚠️ 风险与挑战

# ⭐ 阅读价值评分（1-10）

文章：

{article}
"""

            # 调用 OpenAI
            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = completion.choices[0].message.content

            # 输出结果
            st.markdown(result)
        except Exception as e:
            st.error(f"发生错误：{e}")
