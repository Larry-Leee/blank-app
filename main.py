import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import openai
import json

# 设置OpenAI API密钥（可选）
openai.api_key = "your-openai-api-key"

def load_excel(file):
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        return None

def generate_chart(df, x_col, y_col1, y_col2, chart_type="bar"):
    # 将NaN替换为null
    df = df.where(pd.notnull(df), None)
    
    # 将数据转换为JSON格式
    option = {
        "tooltip": {},
        "xAxis": {"type": "category", "data": df[x_col].astype(str).tolist()},
        "yAxis": {"type": "value"},
        "series": [
            {"name": y_col1, "data": df[y_col1].tolist(), "type": chart_type},
            {"name": y_col2, "data": df[y_col2].tolist(), "type": chart_type}
        ],
        "legend": {"data": [y_col1, y_col2]}
    }

    # 使用json.dumps将生成的配置转换为有效的JSON字符串
    option_json = json.dumps(option, default=str)
    st_echarts(option_json, height="400px")

def query_data(df, query):
    try:
        result = eval(query)
        return result
    except Exception as e:
        st.error(f"查询失败: {e}")
        return None

def chat_query_to_pandas(query, df):
    try:
        prompt = f"将以下自然语言查询转化为Pandas代码：\n{query}\n\nPandas 代码:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        pandas_code = response.choices[0].text.strip()
        st.write("生成的 Pandas 代码:", pandas_code)
        result = eval(pandas_code)
        return result
    except Exception as e:
        st.error(f"自然语言查询解析失败: {e}")
        return None

# Streamlit 页面配置
st.title("ChatExcel - 智能 Excel 数据分析")

# 上传文件
uploaded_file = st.file_uploader("上传你的 Excel 文件", type=["xlsx", "xls"])

if uploaded_file:
    df = load_excel(uploaded_file)
    if df is not None:
        st.write("### 数据预览", df.head())

        # 选择列进行图表对比
        x_col = st.selectbox("选择 X 轴数据列", df.columns)
        y_col1 = st.selectbox("选择第一个 Y 轴数据列", df.columns)
        y_col2 = st.selectbox("选择第二个 Y 轴数据列", df.columns)
        chart_type = st.selectbox("选择图表类型", ["bar", "line", "scatter"])

        if st.button("生成图表"):
            generate_chart(df, x_col, y_col1, y_col2, chart_type)

        # 让用户输入 Pandas 查询语句
        query = st.text_area("输入查询语句 (如 df[df['列名'] > 10])", "df")
        if st.button("执行查询"):
            result = query_data(df, query)
            if result is not None:
                st.write("### 查询结果", result)

        # 自然语言查询
        user_query = st.text_input("输入自然语言查询 (如：'显示所有大于100的销售数据')")
        if st.button("执行自然语言查询"):
            if user_query:
                result = chat_query_to_pandas(user_query, df)
                if result is not None:
                    st.write("### 查询结果", result)