import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

# ==========================================
# 基础关卡：数据加载
# ==========================================
@st.cache_data
def load_data():
    """
    从 CSV 文件加载 5G 信号数据
    
    Returns:
        pd.DataFrame: 包含信号数据的 DataFrame
    """
    return pd.read_csv('data/signal_samples.csv')

df = load_data()

# ==========================================
# 进阶关卡：侧边栏筛选器
# ==========================================
st.sidebar.title("🔧 数据筛选")

# 频段筛选
bands = sorted(df['Band'].unique().tolist())
selected_bands = st.sidebar.multiselect(
    "选择频段 (Band)",
    bands,
    default=bands
)

# RSRP范围滑动条
rsrp_min, rsrp_max = float(df['RSRP_dBm'].min()), float(df['RSRP_dBm'].max())
rsrp_range = st.sidebar.slider(
    "RSRP 信号强度范围 (dBm)",
    min_value=rsrp_min,
    max_value=rsrp_max,
    value=(rsrp_min, rsrp_max),
    step=0.5
)

# 终端类型筛选
terminal_types = sorted(df['TerminalType'].unique().tolist())
selected_terminals = st.sidebar.multiselect(
    "选择终端类型",
    terminal_types,
    default=terminal_types
)

# 应用筛选逻辑
filtered_df = df[
    (df['Band'].isin(selected_bands)) &
    (df['RSRP_dBm'] >= rsrp_range[0]) &
    (df['RSRP_dBm'] <= rsrp_range[1]) &
    (df['TerminalType'].isin(selected_terminals))
]

st.sidebar.info(f"📊 已加载 {len(filtered_df)} / {len(df)} 条记录")

# ==========================================
# 基础关卡：信号热力/散点地图
# ==========================================
st.subheader("🗺️ 信号强度分布地图")

# 定义信号强度到颜色的映射逻辑
def get_color(rsrp):
    """
    根据 RSRP 值返回对应的 RGB 颜色
    
    Args:
        rsrp (float): 信号强度值，单位 dBm
        
    Returns:
        list: [R, G, B] 颜色值
    """
    if rsrp > -90:
        return [0, 255, 0]  # 绿色 - 信号强
    elif rsrp > -100:
        return [255, 255, 0]  # 黄色 - 信号中等
    elif rsrp > -110:
        return [255, 165, 0]  # 橙色 - 信号较弱
    else:
        return [255, 0, 0]  # 红色 - 信号弱

# 添加颜色列
filtered_df_map = filtered_df.copy()
filtered_df_map['color'] = filtered_df_map['RSRP_dBm'].apply(get_color)

# 创建 Pydeck 地图
layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_df_map,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=30,
    radius_min_pixels=5,
    radius_max_pixels=60,
    line_width_min_pixels=1,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_line_color=[0, 0, 0],
    tooltip=True
)

# 计算地图中心
view_state = pdk.ViewState(
    longitude=filtered_df_map['Longitude'].mean(),
    latitude=filtered_df_map['Latitude'].mean(),
    zoom=13,
    pitch=0,
)

# 渲染地图
st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "小区ID: {CellID}\n频段: {Band}\nRSRP: {RSRP_dBm} dBm\nSINR: {SINR_dB} dB\n下载速率: {Download_Mbps} Mbps"
        }
    )
)

# ==========================================
# 基础关卡：数据概览图表
# ==========================================
st.subheader("📊 数据统计分析")

col1, col2 = st.columns(2)

# 频段基站数量统计
with col1:
    st.write("**各频段基站数量分布**")
    band_counts = filtered_df['Band'].value_counts()
    fig1 = px.bar(
        band_counts,
        x=band_counts.index,
        y=band_counts.values,
        labels={'x': '频段', 'y': '数量'},
        color=band_counts.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig1, use_container_width=True)

# 终端类型占比统计
with col2:
    st.write("**终端类型占比**")
    terminal_counts = filtered_df['TerminalType'].value_counts()
    fig2 = px.pie(
        values=terminal_counts.values,
        names=terminal_counts.index,
        title="终端类型分布"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 进阶关卡：3D 信号强度可视化
# ==========================================
st.subheader("🎯 3D 下载速率柱状分布")

# 创建 3D 柱状图
fig3d = go.Figure(data=[go.Scatter3d(
    x=filtered_df['Longitude'],
    y=filtered_df['Latitude'],
    z=filtered_df['Download_Mbps'],
    mode='markers',
    marker=dict(
        size=5,
        color=filtered_df['RSRP_dBm'],  # 按 RSRP 着色
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="RSRP (dBm)")
    ),
    text=[f"CellID: {cid}<br>Band: {band}<br>RSRP: {rsrp:.2f} dBm<br>下载: {dl:.2f} Mbps<br>终端: {tt}" 
          for cid, band, rsrp, dl, tt in zip(
              filtered_df['CellID'],
              filtered_df['Band'],
              filtered_df['RSRP_dBm'],
              filtered_df['Download_Mbps'],
              filtered_df['TerminalType']
          )],
    hovertemplate='%{text}<extra></extra>'
)])

fig3d.update_layout(
    title='3D 信号强度与下载速率分布',
    scene=dict(
        xaxis_title='经度',
        yaxis_title='纬度',
        zaxis_title='下载速率 (Mbps)'
    ),
    height=600
)

st.plotly_chart(fig3d, use_container_width=True)

# ==========================================
# 数据统计摘要
# ==========================================
st.subheader("📈 数据统计摘要")

col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric(
        "平均RSRP",
        f"{filtered_df['RSRP_dBm'].mean():.2f} dBm"
    )

with col4:
    st.metric(
        "平均SINR",
        f"{filtered_df['SINR_dB'].mean():.2f} dB"
    )

with col5:
    st.metric(
        "平均下载速率",
        f"{filtered_df['Download_Mbps'].mean():.2f} Mbps"
    )

with col6:
    st.metric(
        "数据记录总数",
        len(filtered_df)
    )

# ==========================================
# 展示原始数据
# ==========================================
with st.expander("查看原始数据"):
    st.dataframe(filtered_df, use_container_width=True)

st.success("✅ 实时数据仪表板加载完成！")

