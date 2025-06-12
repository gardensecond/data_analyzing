import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm

font_path = os.path.join(os.getcwd(),"data","NanumGothic.otf")
fm.fontManager.addfont(font_path)
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family']=font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(layout="centered")
st.title("📊 서울시 자치구별 범죄 발생 및 검거율 분석 (2023)")

# GitHub의 CSV 파일 경로
csv_url = "https://raw.githubusercontent.com/gardensecond/data_analyzing/main/5%EB%8C%80%2B%EB%B2%94%EC%A3%84%2B%EB%B0%9C%EC%83%9D%ED%98%84%ED%99%A9_20250609121517.csv"
df_raw = pd.read_csv(csv_url, encoding='utf-8-sig', header=2, skiprows=[3])

df_raw.columns = [
    '자치구1', '자치구', '합계_발생', '합계_검거', '살인_발생', '살인_검거',
    '강도_발생', '강도_검거', '성범죄_발생', '성범죄_검거',
    '절도_발생', '절도_검거', '폭력_발생', '폭력_검거'
]

df = df_raw[df_raw['자치구'] != '소계'].drop(columns=['자치구1']).copy()

# 숫자 변환
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 검거율 계산
df['검거율'] = (df['합계_검거'] / df['합계_발생']) * 100

# 🎯 사용자 필터
st.sidebar.header("🔍 필터")
selected_gu = st.sidebar.multiselect("자치구를 선택하세요", df['자치구'].unique(), default=df['자치구'].unique())
crime_types = ['살인', '강도', '성범죄', '절도', '폭력']
selected_crimes = st.sidebar.multiselect("범죄 유형을 선택하세요", crime_types, default=crime_types)

# 🔎 필터링된 데이터
filtered_df = df[df['자치구'].isin(selected_gu)]

# 📊 시각화
st.subheader("✅ 선택된 범죄 유형 발생 및 검거율 비교")
for crime in selected_crimes:
    fig, ax = plt.subplots(figsize=(10, 5))
    crime_data = filtered_df[[f'{crime}_발생', f'{crime}_검거', '자치구']]
    crime_data['검거율'] = (crime_data[f'{crime}_검거'] / crime_data[f'{crime}_발생']) * 100

    sns.barplot(data=crime_data, x='자치구', y='검거율', palette='coolwarm', ax=ax)
    ax.set_title(f'{crime} 검거율')
    ax.set_ylabel('검거율 (%)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# 📋 데이터 출력
with st.expander("📄 데이터 보기"):
    st.dataframe(filtered_df.reset_index(drop=True))
