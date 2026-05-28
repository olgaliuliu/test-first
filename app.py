import streamlit as st
import pandas as pd
import os

# 設定資料儲存的檔案名稱
DATA_FILE = "my_data.csv"

# 設定網頁標題與排版
st.set_page_config(page_title="專屬數據收集與分析系統", layout="wide")

# 建立側邊欄選單（可以作為前後台切換）
st.sidebar.title("系統選單")
menu = ["📝 前台：填寫問卷", "📊 後台：數據下載與圖表"]
choice = st.sidebar.radio("請選擇頁面：", menu)

# ==========================================
# 1. 前台：給指定人員填寫的頁面
# ==========================================
if choice == "📝 前台：填寫問卷":
    st.title("數據回填表單")
    st.write("請填寫以下資訊，完成後點擊提交。")
    
    # 建立表單
    with st.form("data_form"):
        # 您可以在這裡自訂任何想要收集的問題
        user_name = st.text_input("填寫人姓名")
        project_name = st.selectbox("負責專案", ["專案 A", "專案 B", "專案 C", "其他"])
        sales_amount = st.number_input("本週業績數據 (單位：萬)", min_value=0)
        satisfaction = st.slider("專案推進順暢度評分 (1-10)", 1, 10, 5)
        
        submitted = st.form_submit_button("一鍵提交")
        
        # 處理提交後的動作
        if submitted:
            # 將新資料整理成表格格式
            new_data = pd.DataFrame({
                "姓名": [user_name],
                "負責專案": [project_name],
                "業績數據(萬)": [sales_amount],
                "順暢度評分": [satisfaction]
            })
            
            # 將資料存入 CSV 檔案（簡單的內建資料庫）
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
            else:
                df = new_data
                
            df.to_csv(DATA_FILE, index=False)
            st.success(f"感謝 {user_name}，您的資料已成功提交！")

# ==========================================
# 2. 後台：給您一鍵下載與分析的頁面
# ==========================================
elif choice == "📊 後台：數據下載與圖表":
    st.title("後台管理中心")
    
    # 檢查是否有資料
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        
        # 區塊 1：原始資料檢視與下載
        st.subheader("📁 收集到的原始資料")
        st.dataframe(df, use_container_width=True) # 顯示資料表
        
        # 一鍵下載功能
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 一鍵下載 Excel/CSV 檔案",
            data=csv_data,
            file_name="collected_data.csv",
            mime="text/csv"
        )
        
        st.divider() # 分隔線
        
        # 區塊 2：自動化彩色圖表分析
        st.subheader("📈 自動化數據分析圖表")
        
        # 將畫面分為左右兩排顯示圖表
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**各專案業績總和 (長條圖)**")
            # 自動計算各專案業績並畫圖
            project_sales = df.groupby("負責專案")["業績數據(萬)"].sum()
            st.bar_chart(project_sales)
            
        with col2:
            st.write("**各專案平均順暢度評分 (折線圖)**")
            # 自動計算各專案平均評分並畫圖
            project_score = df.groupby("負責專案")["順暢度評分"].mean()
            st.line_chart(project_score)
            
    else:
        st.info("目前還沒有人填寫資料喔！")
