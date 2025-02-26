import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import re
from collections import defaultdict



# 加载spaCy中文模型
nlp = spacy.load("zh_core_web_sm")


# 定义一个简单的模糊匹配方法，用于从用户的请求中推断图表类型
def guess_chart_type(request):
    chart_keywords = {
        "柱状图": "bar",
        "折线图": "line",
        "散点图": "scatter",
        "热力图": "heatmap",
        "饼图": "pie",
        "对比": "bar"  # 默认对比为柱状图
    }

    # 搜索请求文本中是否有对应的图表类型关键词
    for keyword, chart_type in chart_keywords.items():
        if keyword in request:
            return chart_type

    # 如果没有明确的图表类型，返回默认类型
    return "bar"


# 基于用户输入生成图表
def generate_chart(df, analysis_request):
    # 使用spaCy进行文本分析，提取列名等信息
    doc = nlp(analysis_request)

    # 提取文本中的名词（可能是列名）
    columns = [token.text for token in doc if token.pos_ == "NOUN"]

    # 如果用户输入中包含至少两列数据，生成柱状图
    if len(columns) >= 2:
        col1, col2 = columns[:2]

        # 如果这些列存在于数据框中
        if col1 in df.columns and col2 in df.columns:
            chart_type = guess_chart_type(analysis_request)

            if chart_type == "bar":
                return generate_bar_chart(df, col1, col2)
            elif chart_type == "line":
                return generate_line_chart(df, col1, col2)
            elif chart_type == "scatter":
                return generate_scatter_chart(df, col1, col2)
            elif chart_type == "heatmap":
                return generate_heatmap(df)
            elif chart_type == "pie":
                return generate_pie_chart(df, col1)
    return None


# 生成柱状图
def generate_bar_chart(df, col1, col2):
    fig, ax = plt.subplots(figsize=(10, 6))
    df[[col1, col2]].plot(kind='bar', ax=ax)
    ax.set_title(f"{col1} 与 {col2} 对比柱状图")
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    return fig


# 生成折线图
def generate_line_chart(df, col1, col2):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='line', x=col1, y=col2, ax=ax)
    ax.set_title(f"{col1} 与 {col2} 的折线图")
    return fig


# 生成散点图
def generate_scatter_chart(df, col1, col2):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df[col1], df[col2])
    ax.set_title(f"{col1} 与 {col2} 的散点图")
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    return fig


# 生成热力图
def generate_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title("相关性热力图")
    return fig


# 生成饼图
def generate_pie_chart(df, col):
    fig, ax = plt.subplots(figsize=(8, 8))
    df[col].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title(f"{col} 的饼图")
    ax.set_ylabel('')
    return fig


# 主函数
def main():
    st.title("基于自然语言的 Excel 数据分析")

    # 上传文件
    uploaded_file = st.file_uploader("上传您的 Excel 文件", type=["xlsx"])

    if uploaded_file is not None:
        # 读取文件
        df = pd.read_excel(uploaded_file)
        st.write("数据预览：")
        st.write(df.head())

        # 输入分析需求
        analysis_request = st.text_input("请输入分析需求（例如：'基于这个Excel文档帮我生成一个计划与时间完成的对比柱状图'）")

        # 持续监控分析请求
        if analysis_request:
            with st.spinner('正在处理中...'):
                fig = generate_chart(df, analysis_request)
                if fig:
                    st.pyplot(fig)
                else:
                    st.error("无法解析该请求，请检查输入的内容。")
        else:
            st.warning("请输入分析需求。")


if __name__ == "__main__":
    main()