import streamlit as st
import pandas as pd
import altair as alt

# 📁 CSV 파일 불러오기
file_path = "5대+범죄+발생현황_20250609121517.csv"
df_raw = pd.read_csv(file_path, header=[0, 1, 2])

# 📌 '자치구' 컬럼명 정리
df_raw = df_raw.rename(columns={
    ('자치구별(2)', '자치구별(2)', '자치구별(2)'): '자치구'
})

# ✅ 데이터 본문만 추출 (앞부분 2행은 메타 정보)
df = df_raw.iloc[2:].copy()

# 🏙 자치구 리스트
gu_list = df['자치구'].unique().tolist()

# 🔍 범죄 유형 목록 정의
crime_types = ['살인', '강도', '성범죄', '절도', '폭력']
category_map = {
    '성범죄': '강간·강제추행',
}

# 📊 Streamlit UI
st.title("📈 범죄율 및 검거율 시각화 대시보드")

selected_gu = st.multiselect("자치구를 선택하세요", gu_list, default=gu_list[:5])
selected_crimes = st.multiselect("범죄 유형을 선택하세요", crime_types, default=['살인', '강도'])

# 🔧 전처리 함수
def preprocess_data(df, selected_gu, selected_crimes):
    plot_data = []
    for crime in selected_crimes:
        display_name = category_map.get(crime, crime)
        for stat in ['발생', '검거']:
            col = ('2023', '합계', display_name if stat == '발생' else display_name + '.1')
            if col not in df.columns:
                continue
            for _, row in df[df['자치구'].isin(selected_gu)].iterrows():
                try:
                    value = int(row[col])
                except:
                    value = 0
                plot_data.append({
                    '자치구': row['자치구'],
                    '범죄유형': crime,
                    '통계': stat,
                    '건수': value
                })
    return pd.DataFrame(plot_data)

# 📈 데이터 전처리 후 시각화
plot_df = preprocess_data(df, selected_gu, selected_crimes)

st.markdown("## 📊 자치구별 범죄 발생 및 검거 추이")

if not plot_df.empty:
    chart = alt.Chart(plot_df).mark_line(point=True).encode(
        x='자치구:N',
        y='건수:Q',
        color='범죄유형:N',
        strokeDash='통계:N',
        tooltip=['자치구', '범죄유형', '통계', '건수']
    ).properties(
        width=800,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("선택한 자치구나 범죄 유형에 해당하는 데이터가 없습니다.")
