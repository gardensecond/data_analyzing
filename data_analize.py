import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 스타일 지정
st.set_page_config(layout="wide")
st.markdown("<h1 style='font-size: 28px;'>🔍 서울시 자치구별 범죄 발생 및 검거율 분석 (2023)</h1>", unsafe_allow_html=True)

# 데이터 불러오기 (예시용)
df = pd.read_csv("crime_seoul_2023.csv")  # '자치구', '범죄유형', '발생건수', '검거건수' 포함 필요

# 범죄율, 검거율 계산
df["검거율"] = (df["검거건수"] / df["발생건수"]) * 100
df["범죄율"] = df["발생건수"] / df["발생건수"].sum() * 100  # 전체 대비 비율

# --- 사이드바 필터 ---
st.sidebar.markdown("### 🔍 필터")

# 자치구 선택
gu_list = df["자치구"].unique().tolist()
selected_gu = st.sidebar.multiselect("자치구를 선택하세요", gu_list, default=gu_list)

if st.sidebar.button("자치구 전체 선택 취소"):
    selected_gu = []

# 범죄유형 선택
crime_list = df["범죄유형"].unique().tolist()
selected_crimes = st.sidebar.multiselect("범죄 유형을 선택하세요", crime_list, default=crime_list)

if st.sidebar.button("범죄유형 전체 선택 취소"):
    selected_crimes = []

# 시각화 종류 선택
chart_type = st.sidebar.radio("시각화 유형 선택", ["막대그래프 (검거율)", "꺾은선그래프 (범죄율/검거율 변화)"])

# 필터 적용
filtered_df = df[(df["자치구"].isin(selected_gu)) & (df["범죄유형"].isin(selected_crimes))]

# --- 메인 영역 ---
st.markdown("### ✅ 선택된 범죄 유형 발생 및 검거율 비교")

if chart_type == "막대그래프 (검거율)":
    pivot_df = filtered_df.pivot(index="자치구", columns="범죄유형", values="검거율").fillna(0)
    pivot_df = pivot_df[selected_crimes]  # 범죄유형 순서 고정

    fig, ax = plt.subplots(figsize=(10, 4))
    pivot_df.plot(kind="bar", ax=ax, colormap="coolwarm", width=0.85)
    plt.ylabel("검거율 (%)")
    plt.title("검거율 비교", fontsize=15)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

elif chart_type == "꺾은선그래프 (범죄율/검거율 변화)":
    fig, ax = plt.subplots(figsize=(10, 4))

    for gu in selected_gu:
        gu_df = filtered_df[filtered_df["자치구"] == gu]
        if gu_df.empty:
            continue
        gu_df = gu_df.groupby("범죄유형")[["범죄율", "검거율"]].mean().reset_index()
        gu_df = gu_df.sort_values("범죄유형")

        ax.plot(gu_df["범죄유형"], gu_df["범죄율"], label=f"{gu} - 범죄율", linestyle="--", marker="o")
        ax.plot(gu_df["범죄유형"], gu_df["검거율"], label=f"{gu} - 검거율", linestyle="-", marker="s")

    ax.set_ylabel("비율 (%)")
    ax.set_title("자치구별 범죄율 및 검거율 변화", fontsize=15)
    plt.xticks(rotation=45, ha='right')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)
