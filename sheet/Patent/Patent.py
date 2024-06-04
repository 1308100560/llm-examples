#导入相关包
import pandas as pd
import plotly.express as px
import streamlit as st

# 设置页面配置
st.set_page_config(page_title="数据大屏", page_icon=":bar_chart:", layout="wide")
st.balloons()

# 读取数据
def get_data_from_excel():
    df = pd.read_excel(io="./Batteries/Patent.xlsx", engine="openpyxl", sheet_name="Sheet1")
    return df

df = get_data_from_excel()

# 主页面标题
st.title(":bar_chart: 模型评分")
st.markdown("##")

# df["model_prompt"] = df["model"] + df["prompt"]

# 横向条形图
fig_model = px.bar(
    data_frame=df,
    x="总分",
    y="model",
    orientation="h",
    title="<b>模型评分</b>"
)

fig_model.update_layout(
    plot_bgcolor="rgba(0, 0, 0, 0)",
    xaxis=dict(showgrid=False)
)

# 显示图表
st.plotly_chart(fig_model)
