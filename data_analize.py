import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(layout="wide", page_title="서울시 자치구별 범죄 분석 대시보드")

# 예시용 데이터 로딩 (실제 데이터로 대체하세요)
@st.cache_data
def load_data():
    # 예시 데이터 형식: ['년도', '자치구', '범죄유형', '발생건수', '검거건수']
    return pd.read_csv("seoul_crime_by_year.csv")

data = load_data()

# 자치구와 범죄유형 목록
districts = sorted(data["자치구"].unique())
crime_types = sorted(data["범죄유형"].unique())

# --- 사이드바 필터 영역 ---
with st.sidebar:
    st.title("🔍 필터")

    selected_districts = st.multiselect(
        "자치구를 선택하세요",
        options=districts,
        default=districts,
        key="districts"
    )
    if st.button("자치구 전체 선택 해제"):
        selected_districts = []

    selected_crimes = st.multiselect(
        "범죄 유형을 선택하세요",
        options=crime_types,
        default=crime_types,
        key="crimes"
    )
    if st.button("범죄 유형 전체 선택 해제"):
        selected_crimes = []

# --- 메인 페이지 ---
st.title("📊 서울시 자치구별 범죄 발생 및 검거율 분석")
st.markdown("**선택된 자치구와 범죄 유형에 따라 연도별 추이를 꺾은선 그래프로 시각화합니다.**")

# 필터링
filtered = data[
    data["자치구"].isin(selected_districts) & 
    data["범죄유형"].isin(selected_crimes)
]

# --- 시각화 영역 ---
if filtered.empty:
    st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
else:
    for crime in selected_crimes:
        st.subheader(f"📈 {crime} 발생건수 및 검거율 추이")

        crime_data = filtered[filtered["범죄유형"] == crime]
        crime_data["검거율"] = crime_data["검거건수"] / crime_data["발생건수"] * 100

        fig, ax1 = plt.subplots(figsize=(10, 5))
        
        for district in selected_districts:
            subset = crime_data[crime_data["자치구"] == district]
            ax1.plot(subset["년도"], subset["발생건수"], label=f"{district} 발생건수")

        ax1.set_ylabel("발생건수")
        ax1.set_xlabel("년도")
        ax1.legend()
        ax1.set_title(f"{crime} 발생 추이")
        st.pyplot(fig)

        # 검거율 그래프
        fig, ax2 = plt.subplots(figsize=(10, 5))
        for district in selected_districts:
            subset = crime_data[crime_data["자치구"] == district]
            ax2.plot(subset["년도"], subset["검거율"], label=f"{district} 검거율")

        ax2.set_ylabel("검거율 (%)")
        ax2.set_xlabel("년도")
        ax2.legend()
        ax2.set_title(f"{crime} 검거율 추이")
        st.pyplot(fig)
