import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("5대+범죄+발생현황_20250609121517.csv")

# 컬럼 정리
df.columns = df.columns.str.strip()  # 공백 제거
if '연도' in df.columns:
    df['연도'] = df['연도'].astype(str)  # 슬라이더용 문자열 처리

# 제목
st.title("📊 5대 범죄 발생현황 대시보드")

st.markdown("""
**데이터 출처:** 5대 범죄 발생현황 CSV 파일  
범죄 유형과 연도별로 필터링하여 발생 추이를 확인할 수 있습니다.
""")

# 연도 필터
years = sorted(df['연도'].unique())
year_min, year_max = int(min(years)), int(max(years))
selected_range = st.slider("📅 연도 범위 선택", year_min, year_max, (year_min, year_max))

# 범죄 필터
crime_types = df['죄종'].unique()
selected_crimes = st.multiselect("🔍 범죄 유형 선택", crime_types, default=list(crime_types))

# 필터링 적용
filtered_df = df[
    (df['연도'].astype(int) >= selected_range[0]) &
    (df['연도'].astype(int) <= selected_range[1]) &
    (df['죄종'].isin(selected_crimes))
]

# 그래프 출력
fig = px.line(
    filtered_df,
    x="연도",
    y="발생",
    color="죄종",
    markers=True,
    title="📈 연도별 범죄 발생 추이"
)
fig.update_layout(xaxis_title="연도", yaxis_title="발생 건수")

st.plotly_chart(fig)

# 2022년 데이터 요약
if '2022' in df['연도'].values:
    st.header("📌 2022년 범죄 발생 건수 요약")
    summary = df[df['연도'] == '2022'][['죄종', '발생']].sort_values(by='발생', ascending=False)
    st.dataframe(summary)
