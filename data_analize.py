import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import streamlit as st

# 제목
st.title("서울시 자치구별 범죄 데이터 분석 (2023)")

# 데이터 불러오기
df_raw = pd.read_csv("seoul_crime_2023.csv", encoding='cp949')

# 필요한 열 추출 및 처리
df = df_raw[['자치구', '합계_발생', '합계_검거']].copy()
df['검거율'] = (df['합계_검거'] / df['합계_발생']) * 100

# 범죄 발생 건수 시각화
st.subheader("자치구별 범죄 발생 건수")
df_sorted = df.sort_values(by='합계_발생', ascending=False)
fig1, ax1 = plt.subplots(figsize=(12, 8))
sns.barplot(data=df_sorted, x='합계_발생', y='자치구', palette='Reds_r', ax=ax1)
ax1.set_title('서울시 자치구별 범죄 발생 건수 (2023)')
st.pyplot(fig1)

# 검거율 시각화
st.subheader("자치구별 범죄 검거율")
df_sorted_by_rate = df.sort_values(by='검거율', ascending=False)
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.barplot(data=df_sorted_by_rate, x='검거율', y='자치구', palette='Greens', ax=ax2)
ax2.set_title('서울시 자치구별 범죄 검거율 (2023)')
ax2.set_xlim(0, 110)
st.pyplot(fig2)
