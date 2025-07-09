
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hospital Crisis Metrics Dashboard", layout="wide")

st.title("🏥 Hospital Crisis Metrics Dashboard (Post-OBBBA)")

@st.cache_data
def load_data():
    return pd.read_csv("Hospital_Metrics_SORM.csv")

df = load_data()

st.markdown("### 📋 Hospital Overview")
st.dataframe(df)

# Heatmap of UCRI
st.markdown("### 🔥 Uncompensated Care Risk Index (UCRI) Heatmap")
fig = px.treemap(df, path=['County', 'Hospital_Name'], values='UCRI', color='UCRI',
                 color_continuous_scale='Reds', title="Hospital UCRI by County")
st.plotly_chart(fig, use_container_width=True)

# Financial Forecasting (simulated revenue loss)
st.markdown("### 💰 Financial Forecasting")
df['Projected_Revenue_Loss_2026_M'] = df['Medicaid_Revenue_Loss_M'] * 1.05
df['Projected_Revenue_Loss_2027_M'] = df['Medicaid_Revenue_Loss_M'] * 1.10
fig2 = px.bar(df, x='Hospital_Name', y=['Medicaid_Revenue_Loss_M', 'Projected_Revenue_Loss_2026_M', 'Projected_Revenue_Loss_2027_M'],
              title="Projected Revenue Loss Over Time", barmode='group', labels={'value': 'Revenue Loss ($M)', 'variable': 'Year'})
st.plotly_chart(fig2, use_container_width=True)

# Legislative Report Builder
st.markdown("

st.markdown("### 🔎 Browse & Download Scored Data")
st.dataframe(df)

st.download_button(
    label="📥 Download Full Scored Dataset (CSV)",
    data=df.to_csv(index=False),
    file_name="Hospital_Crisis_Metrics_Scored.csv",
    mime="text/csv"
)


### 🏛️ One-Click Legislative Report Builder")
selected_hospital = st.selectbox("Select a hospital for report:", df['Hospital_Name'])
row = df[df['Hospital_Name'] == selected_hospital].iloc[0]

report = f'''
#### Legislative Report for {row["Hospital_Name"]}

**County:** {row["County"]}, {row["State"]}  
**Medicaid Revenue Loss:** ${row["Medicaid_Revenue_Loss_M"]}M  
**Uncompensated Care Risk Index (UCRI):** {row["UCRI"]}  
**Rural Closure Risk (RCVS):** {row["RCVS"]}/10  
**ED Overload Level (EDOI):** {row["EDOI"]}  
**Community Care Gap Score (CCGS):** {row["CCGS"]}/100  
**Stabilization Grant Impact Score (SGIS):** {row["SGIS"]}/100  
**Modernization Readiness:** {row["HMRS"]}

**Summary:**  
{row["Hospital_Name"]} is facing elevated financial and operational pressure due to reduced Medicaid reimbursements and rising uncompensated care. We recommend urgent legislative support, including emergency stabilization funding and targeted rural health investments.
'''

st.markdown(report)
