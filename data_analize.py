import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import seaborn as sns

# 한글 폰트 설정 (Windows/Linux 호환)
plt.rcParams['font.family'] = 'Malgun Gothic' if 'Malgun Gothic' in plt.rcParams['font.family'] else 'AppleGothic'

# 데이터 불러오기
url = "https://github.com/gardensecond/data_analyzing/raw/main/5%EB%8C%80%2B%EB%B2%94%EC%A3%84%2B%EB%B0%9C%EC%83%9D%ED%98%84%ED%99%A9_20250609121517.csv"
df = pd.read_csv(url)

# Streamlit 앱 제목
st.title("📊 서울시 자치구별 범죄 발생 및 검거율 분석 (2023)")

# 사이드바 필터
st.sidebar.header("🔎 필터 설정")

# 자치구 선택 필터
st.sidebar.markdown("### 🧭 자치구 필터")
if st.sidebar.button("자치구 전체 선택 해제"):
    selected_gu = []
else:
    selected_gu = st.sidebar.multiselect("자치구를 선택하세요", df['자치구'].unique(), default=df['자치구'].unique())

# 범죄 유형 선택 필터
st.sidebar.markdown("### 🚨 범죄유형 필터")
crime_types = df['죄종'].unique()
if st.sidebar.button("범죄유형 전체 선택 해제"):
    selected_crimes = []
else:
    selected_crimes = st.sidebar.multiselect("범죄 유형을 선택하세요", crime_types, default=crime_types)

# 데이터 필터링
filtered_df = df[df['자치구'].isin(selected_gu) & df['죄종'].isin(selected_crimes)]

# 필터링된 항목이 있을 때만 그래프 출력
if not filtered_df.empty:
    for crime in selected_crimes:
        crime_df = filtered_df[filtered_df['죄종'] == crime]

        # 그래프 출력
        st.subheader(f"{crime} 검거율")
        fig, ax = plt.subplots(figsize=(12, 6))  # 그래프 크기 조정
        sns.barplot(data=crime_df, x='자치구', y='검거율', hue='자치구', palette='coolwarm', dodge=False, ax=ax)
        plt.xticks(rotation=90)
        plt.ylabel("검거율 (%)")
        plt.xlabel("")
        plt.legend([],[], frameon=False)  # 범례 제거
        st.pyplot(fig)
else:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
