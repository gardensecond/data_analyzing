import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm

font_path = os.path.join(os.getcwd(), "NanumGothic.otf")
fm.fontManager.addfont(font_path)
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(layout="centered")
st.title("📊 서울시 자치구별 범죄 분석 대시보드")
st.markdown("2023년 서울시의 자치구별 범죄 발생 현황과 검거율을 시각적으로 분석한 결과입니다.")

# GitHub의 CSV 파일 경로
csv_url = "https://raw.githubusercontent.com/gardensecond/data_analyzing/main/5%EB%8C%80%2B%EB%B2%94%EC%A3%84%2B%EB%B0%9C%EC%83%9D%ED%98%84%ED%99%A9_20250609121517.csv"
df_raw = pd.read_csv(csv_url, encoding='utf-8-sig', header=2, skiprows=[3])

# 컬럼 이름 정리
df_raw.columns = [
    '자치구1', '자치구', '합계_발생', '합계_검거', '살인_발생', '살인_검거',
    '강도_발생', '강도_검거', '성범죄_발생', '성범죄_검거',
    '절도_발생', '절도_검거', '폭력_발생', '폭력_검거'
]

# 불필요한 행 제거 및 숫자 변환
df = df_raw[df_raw['자치구'] != '소계'].drop(columns=['자치구1']).copy()
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 검거율 계산 및 클리핑 처리
df['검거율'] = (df['합계_검거'] / df['합계_발생']) * 100
df['검거율'] = df['검거율'].clip(upper=100)

# 사이드바 필터
st.sidebar.markdown("## 🧭 대시보드 필터")
st.sidebar.markdown("원하는 자치구와 범죄 유형을 선택해보세요!")
selected_gu = st.sidebar.multiselect("자치구를 선택하세요", df['자치구'].unique(), default=df['자치구'].unique())
crime_types = ['살인', '강도', '성범죄', '절도', '폭력']
selected_crimes = st.sidebar.multiselect("범죄 유형을 선택하세요", crime_types, default=crime_types)

# 필터링 된 데이터
filtered_df = df[df['자치구'].isin(selected_gu)]

# 시각화 스타일 설정
sns.set_style("whitegrid")

st.markdown("---")
st.subheader("✅ 선택된 범죄 유형 검거율 비교")
for crime in selected_crimes:
    fig, ax = plt.subplots(figsize=(10, 5))
    crime_data = filtered_df[[f'{crime}_발생', f'{crime}_검거', '자치구']].copy()
    crime_data['검거율'] = (crime_data[f'{crime}_검거'] / crime_data[f'{crime}_발생']) * 100
    crime_data['검거율'] = crime_data['검거율'].clip(upper=100)

    sns.barplot(data=crime_data, x='자치구', y='검거율', palette='flare', ax=ax)

    # 바 위에 검거율 숫자 표시
    for i, val in enumerate(crime_data['검거율']):
        ax.text(i, val + 1, f"{val:.1f}%", ha='center', va='bottom', fontsize=9)

    ax.set_title(f'🔍 {crime} 검거율', fontsize=14, weight='bold')
    ax.set_ylabel('검거율 (%)')
    ax.set_ylim(0, 110)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

# 데이터 보기
with st.expander("📄 원본 데이터 보기"):
    st.markdown("다음은 선택된 자치구의 원본 데이터를 요약한 표입니다.")
    st.dataframe(filtered_df.reset_index(drop=True))
