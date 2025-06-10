import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(layout="wide", page_title="서울시 범죄 대시보드")

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("5대 범죄 발생현황_20250609121517.csv")
    df["검거율"] = df["검거건수"] / df["발생건수"] * 100
    return df

df = load_data()

# 자치구 및 범죄유형 목록
districts = sorted(df["자치구"].unique())
crime_types = sorted(df["범죄유형"].unique())

# --- 사이드바 필터 ---
with st.sidebar:
    st.title("🔍 필터")

    selected_districts = st.multiselect("자치구 선택", options=districts, default=districts)
    if st.button("자치구 전체 해제"):
        selected_districts = []

    selected_crimes = st.multiselect("범죄 유형 선택", options=crime_types, default=crime_types)
    if st.button("범죄 유형 전체 해제"):
        selected_crimes = []

# --- 필터 적용 ---
filtered = df[
    df["자치구"].isin(selected_districts) & 
    df["범죄유형"].isin(selected_crimes)
]

# --- 메인 대시보드 영역 ---
st.title("📊 자치구별 범죄 발생 및 검거율 추이")
st.markdown("자치구와 범죄 유형을 선택하면, 연도별 발생건수와 검거율을 꺾은선 그래프로 확인할 수 있습니다.")

if filtered.empty:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
else:
    for crime in selected_crimes:
        st.subheader(f"📈 {crime} - 발생건수 및 검거율")

        crime_data = filtered[filtered["범죄유형"] == crime]

        # 발생건수 그래프
        fig1, ax1 = plt.subplots(figsize=(9, 4))
        for gu in selected_districts:
            line = crime_data[crime_data["자치구"] == gu]
            ax1.plot(line["년도"], line["발생건수"], label=gu)
        ax1.set_title(f"{crime} - 연도별 발생건수")
        ax1.set_xlabel("년도")
        ax1.set_ylabel("발생건수")
        ax1.legend(fontsize="small", ncol=4)
        st.pyplot(fig1)

        # 검거율 그래프
        fig2, ax2 = plt.subplots(figsize=(9, 4))
        for gu in selected_districts:
            line = crime_data[crime_data["자치구"] == gu]
            ax2.plot(line["년도"], line["검거율"], label=gu)
        ax2.set_title(f"{crime} - 연도별 검거율 (%)")
        ax2.set_xlabel("년도")
        ax2.set_ylabel("검거율 (%)")
        ax2.legend(fontsize="small", ncol=4)
        st.pyplot(fig2)
