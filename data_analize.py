# app.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib  # 한글 폰트 자동 적용

st.set_page_config(layout="wide")
st.title("📊 서울시 자치구별 범죄 발생 및 검거율 분석 (2023)")

# ✅ GitHub에서 직접 CSV 불러오기
csv_url = "https://raw.githubusercontent.com/gardensecond/data_analyzing/main/5%EB%8C%80%2B%EB%B2%94%EC%A3%84%2B%EB%B0%9C%EC%83%9D%ED%98%84%ED%99%A9_20250609121517.csv"

# CSV 파일 읽기 (실제 헤더는 3번째 줄부터 시작)
df_raw = pd.read_csv(csv_url, encoding='utf-8-sig', header=2, skiprows=[3])

# 열 이름 정리
df_raw.columns = [
    '자치구1', '자치구', '합계_발생', '합계_검거', '살인_발생', '살인_검거',
    '강도_발생', '강도_검거', '성범죄_발생', '성범죄_검거',
    '절도_발생', '절도_검거', '폭력_발생', '폭력_검거'
]

# 불필요한 행 및 열 제거
df = df_raw[df_raw['자치구'] != '소계'].copy()
df = df.drop(columns=['자치구1'])

# 숫자형 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 검거율 계산
df['검거율'] = (df['합계_검거'] / df['합계_발생']) * 100
df_sorted = df.sort_values(by='검거율', ascending=False)

# 📊 검거율 시각화
st.subheader("✅ 자치구별 검거율")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(data=df_sorted, x='검거율', y='자치구', palette='Greens', ax=ax)
ax.set_title('서울시 자치구별 범죄 검거율 (2023)')
ax.set_xlabel('검거율 (%)')
ax.set_ylabel('자치구')
st.pyplot(fig)

# 📊 범죄 유형별 합계 시각화
st.subheader("✅ 범죄 유형별 총합 (발생 기준)")
crime_totals = df[['살인_발생', '강도_발생', '성범죄_발생', '절도_발생', '폭력_발생']].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x=crime_totals.values, y=crime_totals.index, palette='Reds_r', ax=ax2)
ax2.set_title("범죄 유형별 총합 (2023)")
ax2.set_xlabel("발생 건수")
ax2.set_ylabel("범죄 유형")
st.pyplot(fig2)

# 📋 데이터프레임 출력
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df.reset_index(drop=True))
