# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import plotly.express as px


# --- 1. PAGE SETUP & PROFESSIONAL THEME ---
st.set_page_config(page_title="Personal Finance Pro", layout="wide")

st.markdown("""
    <style>
    /* Page တစ်ခုလုံးရဲ့ အပေါ်ပိုင်းကိုပဲ ချိန်ညှိမယ် */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Header (Title) ကိုပဲ သီးသန့် အောက်ရွှေ့ချင်ရင် */
    h1 {
        margin-top: 50px !important;
    }

    /* ကျန်တဲ့ Metric, Subheader, Divider တွေအတွက် */
    [data-testid="stMetric"] { margin-bottom: 0px !important; }
    h3 { margin-top: 5px !important; margin-bottom: 1px !important; }
    hr { margin-top: 1px !important; margin-bottom: 1px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MULTILINGUAL DICTIONARY (Translation Data) ---
LANG_DICT = {
    "English": {
        "page_title": "🔒 Finance Pro Login 🔒",
        "username": "Username",
        "password": "Password",
        "access_btn": "Access Dashboard",
        "access_denied": "Access Denied!",
        "new_entry": "📝 New Entry",
        "date": "Date",
        "type": "Type",
        "inc_opt": "Income",
        "exp_opt": "Expense",
        "cat_input": "Category (e.g. Salary, Food)",
        "amount": "Amount",
        "method": "Payment Method",
        "add_rec_btn": "Add Record",
        "budget_prog": "📊 Budget Progress 📊",
        "main_title": "📊 Personal Financial Dashboard 📊",
        "total_inc": "Total Income",
        "total_exp": "Total Expense",
        "net_bal": "Net Balance",
        "inc_chart": "💵 Income Breakdown Chart",
        "exp_chart": "💰 Expense Breakdown Chart",
        "tx_records": "📑 Transaction Records",
        "save_changes": "Save Table Changes",
        "db_updated": "Database Updated!",
        "tab_titles": ["💰 Budget", "🎯 Savings", "💸 Debt", "📊 Compare", "💳 Payment", "🧾 Receipt", "📅 Calendar", "🧮 Calculator", "📁 Archive"],
        "cat_name": "Budget Name",
        "limit_amt": "Limit Amount",
        "set_budget": "Set Budget",
        "goal": "Goal",
        "target": "Target",
        "current": "Current",
        "save_goal": "Save Goal",
        "name": "Name",
        "to_receive": "To Receive",
        "to_pay": "To Pay",
        "add_debt": "Add Debt",
        "methods_used": "Payment Method",
        "upload_receipt": "Upload Receipt Image",
        "add_rec_btn_tab": "Add Recurring",
        "export_csv": "📥 Export CSV",
        "analysis_title": "💡 Insights & Recommendations",
        "calendar_tab": "📅 Financial Calendar",
        "calc_tab": "🧮 Savings Calculator",
        "cal_title": "Monthly Financial Calendar",
        "calc_title": "Quick Savings Target",
        "target_amount": "Target Amount",
        "daily_save": "Daily Savings Goal",
    },
    "မြန်မာ": {
        "page_title": "🔒အသုံးစာရင်းမှတ်တမ်းသို့ ဝင်ရောက်မည်🔒",
        "username": "အသုံးပြုသူအမည်",
        "password": "စကားဝှက်",
        "access_btn": "ဝင်ရောက်မည်",
        "access_denied": "ဝင်ရောက်ခွင့် ငြင်းပယ်ခံရပါသည်။ တိန်!",
        "new_entry": "📝 စာရင်းအသစ်ထည့်ရန်",
        "date": "ရက်စွဲ",
        "type": "အမျိုးအစား",
        "inc_opt": "ဝင်ငွေ",
        "exp_opt": "ထွက်ငွေ",
        "cat_input": "အကြောင်းအရာ(ဥပမာ - လစာ၊ စားစရိတ်)",
        "amount": "ပမာဏ",
        "method": "ငွေပေးချေမှုစနစ်",
        "add_rec_btn": "မှတ်တမ်းထည့်မည်",
        "budget_prog": "📊 ဘတ်ဂျက်အခြေအနေ 📊",
        "main_title": "📊 ဝင်ငွေ/ထွက်ငွေ စာရင်းရှင်းတမ်း 📊",
        "total_inc": "စုစုပေါင်း ဝင်ငွေ",
        "total_exp": "စုစုပေါင်း ထွက်ငွေ",
        "net_bal": "လက်ကျန်ငွေ",
        "inc_chart": "💵 ဝင်ငွေ အသေးစိတ် ခွဲခြမ်းစိတ်ဖြာမှု",
        "exp_chart": "💰 ထွက်ငွေ အသေးစိတ် ခွဲခြမ်းစိတ်ဖြာမှု",
        "tx_records": "📑 ငွေ ပေးချေ/လက်ခံ မှုမှတ်တမ်းများ",
        "save_changes": " ပြင်ဆင်ချက် သိမ်းဆည်းမည်",
        "db_updated": " အချက်အလက်များအောင်မြင်စွာ ပြုပြင်သိမ်းဆည်း ပြီးပါပြီ!",
        "tab_titles": ["💰 ဘတ်ဂျက်", "🎯 စုငွေ", "💸 အကြွေး", "📊 နှိုင်းယှဉ်ချက်", "💳 ငွေပေးချေမှု", "🧾 ပြေစာ", "📅 ငွေကြေးပြက္ခဒိန်", "🧮 စုငွေတွက်ချက်စက်", "📁 သိမ်းဆည်းရန်"],
        "cat_name": "ဘတ်ဂျက် အမည်",
        "limit_amt": "အသုံးပြုမည့် ငွေပမာဏ",
        "set_budget": "ငွေပမာဏ သတ်မှတ်မည်",
        "goal": "စုဆောင်းရသည့် ရည်ရွယ်ချက်",
        "target": "စုဆောင်းမည့်ငွေ ပမာဏ",
        "current": "လက်ရှိစုငွေ",
        "save_goal": "ရည်မှန်းချက်အား သိမ်းဆည်းမည်",
        "name": "အမည်",
        "to_receive": "ရရန်",
        "to_pay": "ပေးရန်",
        "add_debt": "အကြွေးစာရင်း ထည့်မည်",
        "methods_used": "အသုံးပြုခဲ့သော ငွေပေးချေမှုစနစ်များ",
        "upload_receipt": "ပြေစာမှတ်တမ်းများ တင်ရန်",
        "add_rec_btn_tab": "ပုံမှန်စာရင်း ထည့်မည်",
        "export_csv": "📥 CSV ဖိုင်အဖြစ် ထုတ်ယူမည်",
        "analysis_title": "💡 သုံးသပ်ချက်နှင့် အကြံပြုချက်များ",
        "calendar_tab": "📅 ငွေကြေးပြက္ခဒိန်",
        "calc_tab": "🧮 စုငွေတွက်ချက်စက်",
        "cal_title": "လစဉ် ငွေကြေးပြက္ခဒိန်",
        "calc_title": "စုငွေ ပန်းတိုင်တွက်ချက်မှု",
        "target_amount": "ပန်းတိုင် ပမာဏ",
        "daily_save": "နေ့စဉ် စုရန်ပမာဏ",
    }
}

# --- LANGUAGE SELECTOR PLACE AT THE TOP RIGHT ---
# --- 1.2 MAIN TITLE (CENTERED) & LANGUAGE SELECTOR (WIDER PATTERN) ---
# 💡 language selector box ကော်လံအချိုးအစားကို [9.2, 0.8] ဟု ပြောင်းလဲပြီး ဘောက်စ်ကို အလိုအလျောက် တိုသွားအောင် လုပ်လိုက်ပါသည်
title_col, lang_col = st.columns([9.2, 1.4])

with lang_col:
    # label_visibility="collapsed" ကို ပြန်သုံးပြီး ဘောက်စ်ကို ပိုသေးကျစ်စေပါသည်
    lang = st.selectbox("ဘာသာစကား", ["English", "မြန်မာ"], index=0)
    text = LANG_DICT[lang]

with title_col:
    st.markdown(f"""
        <div style='display: grid; place-items: center; text-align: center; height: 100%; min-height: 25px;'>
            <h1 style='margin: 0; padding: 0; color:#FFFFFF; text-align: right; font-size: 50px;'>
                {text['main_title']}
            </h1>
        </div>
    """, unsafe_allow_html=True)
# --- CUSTOM CSS FOR FORCE DARK MODE & OVERRIDE THEME SELECTION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght=400;600;700&display=swap');
    /* Language Box ကို သေးသေးလေး ဖြစ်အောင် လုပ်ပြီး ခေါင်းစဉ်နဲ့ တစ်ဆင့်တည်း ညှိခြင်း */
    .small-lang-box div[data-baseweb="select"] {
        min-height: 30px !important;
        height: 30px !important;
        font-size: 0.5rem !important;
        border-radius: 10px !important;
    }
    .small-lang-box div[data-baseweb="select"] div {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    /* 1. Force the Main Background and Sidebar to Dark Navy Blue */
    /* 🌙 စက်အားလုံးတွင် Light/Dark ရွေးခွင့်မပေးဘဲ Dark Navy Blue စတိုင်တစ်ခုတည်း ပုံသေချုပ်ခြင်း */
    .stApp, html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A192F !important;
        font-family: 'Poppins', 'Pyidaungsu', sans-serif;
        color: #FFFFFF !important;
    }

    /* စာသားများနှင့် ခေါင်းစဉ်အားလုံးကို အမြဲတမ်း အဖြူရောင်/လင်းရောင် ပုံသေထားခြင်း */
    h1, h2, h3, h4, h5, h6, label, p, span, .stMarkdown p {
        color: #FFFFFF !important;
    }

    /* ဇယားကွက်များနှင့် Input Box များကိုပါ အမှောင်ရောင် နောက်ခံဖြင့် တစ်သားတည်းဖြစ်စေခြင်း */
    div[data-testid="stDataFrameDataframe"], 
    div[data-testid="stDataFrameDataframe"] div,
    .stDataFrame, .glideDataEditor-container, .glideDataEditor-canvas {
        background-color: #0A192F !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #0A192F !important;
        border: 1px solid #233554 !important;
        color: #FFFFFF !important;
    }

    /* Insights Box Style */
    .ai-box {
        background-color: #0A192F;
        border-left: 4px solid #64FFDA; border-radius: 8px;
        padding: 15px; margin-top: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .ai-title { color: #64FFDA; font-weight: 600; font-size: 1.05rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    .ai-text { color: #CDD6F4; font-size: 0.95rem; line-height: 1.6; }

    /* Tables, Data Editors and Containers background configurations */
    div[data-testid="element-container"] iframe,
    .stDataFrame, div[data-testid="stDataFrameDataframe"], div[data-testid="stDataFrameDataframe"] div {
        background-color: #0A192F !important;
        border: none !important;
        box-shadow: none !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stDataFrameDataframe"] table, div[role="grid"] {
        background-color: #0A192F !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown(f"<h1 style='text-align: center; font-size: 22px; color: #64FFDA;'>{text['page_title']}</h1>", unsafe_allow_html=True)
    
    # Form အသုံးပြုခြင်း
    with st.form("login_form"):
        u = st.text_input(text['username'])
        p = st.text_input(text['password'], type="password")
        
        # Enter ခေါက်ရင် အလုပ်လုပ်မည့် submit button
        submit_btn = st.form_submit_button(text['access_btn'])
        
        if submit_btn:
            if u == "admin" and p == "Smart_housekeeper":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error(text['access_denied'])
    
    # Login မဝင်ရသေးရင် page ရဲ့ ကျန်တဲ့အပိုင်းတွေကို မပြအောင် ဒီနေရာမှာ stop ပါ
    st.stop()

# --- 3. DATABASE FILES ---
FILES = {
    'db': "database.csv", 'budget': "budget.csv", 'savings': "savings.csv",
    'debt': "debt.csv", 'rec': "recurring.csv",'debt_cats': 'debt_categories.csv'
}
if not os.path.exists("receipts"): os.makedirs("receipts")


def load_data(f, cols):
    if not os.path.exists(f): pd.DataFrame(columns=cols).to_csv(f, index=False)
    return pd.read_csv(f)


data = load_data(FILES['db'], ["Date", "Type", "Category", "Amount", "Payment Method", "Receipt"])
b_df = load_data(FILES['budget'], ["Category", "Limit"])
s_df = load_data(FILES['savings'], ["Goal", "Target", "Saved"])
d_df = load_data(FILES['debt'], ["Name", "Type", "Amount"])
rec_df = load_data(FILES['rec'], ["Type", "Category", "Amount", "Payment Method"])


# --- Helper Function for AI Render ---
def render_ai_box(title, message_en, message_mm):
    msg = message_en if lang == "English" else message_mm
    st.markdown(f"""
        <div class="ai-box">
            <div class="ai-title">✨ {title}</div>
            <div class="ai-text">{msg}</div>
        </div>
    """, unsafe_allow_html=True)


# --- 4. SIDEBAR INPUTS ---
# --- မြန်မာရက်စွဲ အယ်လ်ဂိုရီသမ် (Today Auto-Highlight ပြက္ခဒိန်ပုံစံ) ---
t_date = date.today()
my_year = t_date.year - 638  # မြန်မာသက္ကရာဇ် တွက်ချက်ခြင်း

# ရက်စွဲအလိုက် မြန်မာလနှင့် ရက်ကောက်ချက်ကို တိကျအောင် ဖော်ပြခြင်း
mlist = ["ပြာသို", "တပို့တွဲ", "တပေါင်း", "တန်ခူး", "ကဆုန်", "နယုန်", "ဝါဆို", "ဝါခေါင်", "တော်သလင်း", "သီတင်းကျွတ်",
         "တန်ဆောင်မုန်း", "နတ်တော်"]
m_month = mlist[(t_date.month - 1) % 12]

# လဆန်း/လပြည့်/လဆုတ် ရက်တွက်ချက်မှုကို နမူနာအချိုးချခြင်း
m_day_num = (t_date.day % 15) if (t_date.day % 15) != 0 else 15
m_phase = "လဆန်း" if t_date.day <= 15 else "လဆုတ်"
if t_date.day == 15:
    m_phase = "လပြည့်"
elif t_date.day == 30:
    m_phase = "လကွယ်"

# ပြက္ခဒိန် Box ပုံစံဖြင့် Sidebar ထိပ်ဆုံးတွင် အလှပြခြင်း
st.sidebar.markdown(f"""
    <div style='background-color:#112240; border:1px solid #233554; border-radius:12px; padding:12px; text-align:center; margin-bottom:15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
        <p style='margin:0; color:#8892B0; font-size:0.8rem; font-weight:600;'>📅 MYANMAR CALENDAR (TODAY)</p>
        <h3 style='margin:5px 0; color:#64FFDA; font-family:Pyidaungsu;'>မြန်မာသက္ကရာဇ် {my_year} ခု</h3>
        <p style='margin:0; color:#E2E8F0; font-size:1rem; font-weight:bold;'>{m_month} {m_phase} {m_day_num} ရက်</p>
        <p style='margin:4px 0 0 0; color:#8892B0; font-size:0.8rem;'>အင်္ဂလိပ်ရက်စွဲ: {t_date.strftime('%d-%b-%Y')}</p>
    </div>
""", unsafe_allow_html=True)

# 📝 New Entry ခေါင်းစဉ်ကို ပြက္ခဒိန်အောက်သို့ ပို့ခြင်း
st.sidebar.markdown(f"<h2 style='color:#64FFDA; margin-top:5px;'>{text['new_entry']}</h2>", unsafe_allow_html=True)

# 1. Inputs
d_in = st.sidebar.date_input(text['date'], date.today())
t_in = st.sidebar.selectbox(text['type'], [text['inc_opt'], text['exp_opt']])

# Debt Category တွေကို ဖိုင်ကနေ ဖတ်မယ်
if os.path.exists(FILES['debt_cats']):
    debt_cats_list = pd.read_csv(FILES['debt_cats'])['Category'].tolist()
else:
    debt_cats_list = []

# ရှိပြီးသား Budget Category တွေ + Debt Category တွေ + "အခြား" ကို ပေါင်းလိုက်မယ်
budget_categories = b_df['Category'].tolist() + debt_cats_list + ["အခြား"] 
c_select = st.sidebar.selectbox(text['cat_input'], budget_categories)

c_in = c_select
if c_select == "အခြား":
    c_in = st.sidebar.text_input("အခြား ခေါင်းစဉ်ရိုက်ပါ")

a_in = st.sidebar.number_input(text['amount'], min_value=0.0)
p_in = st.sidebar.selectbox(text['method'], ["Cash", "KBZ Pay", "Wave", "Bank"])

# 2. Submit Button
if st.sidebar.button(text['add_rec_btn']):
    if c_in and a_in > 0:
        type_clean = t_in
        
        # ၁။ CSV ထဲကို အချက်အလက်သစ်သွင်းမယ်
        new_row = pd.DataFrame({
            'Date': [d_in], 
            'Type': [type_clean], 
            'Category': [c_in], 
            'Amount': [a_in], 
            'Payment Method': [p_in], 
            'Receipt': [""]
        })
        # (သတိထားရန် - ကိုကို့ CSV ထဲက Header နာမည်တွေနဲ့ ဒီ key တွေ တူရပါမယ်)
        
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(FILES['db'], index=False)
        
        # ၂။ အခုအသစ်ထည့်လိုက်တာက Savings Goal နဲ့ တူရင် 'Saved' ထဲကို အလိုအလျောက် ပေါင်းထည့်မယ်
        if c_in in s_df['Goal'].values:
            # Savings ဇယားထဲက အဲ့ဒီ Goal ရဲ့ Saved တန်ဖိုးကို ရှာပြီး ပေါင်းမယ်
            s_df.loc[s_df['Goal'] == c_in, 'Saved'] += a_in
            # ပြင်ပြီးသား Savings ဇယားကို သိမ်းမယ်
            s_df.to_csv(FILES['savings'], index=False)
            
        st.success("အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader(text['budget_prog'])
# အသုံးစရိတ် Data ထဲမှာ "Expense (ထွက်ငွေ)" ဆိုတဲ့ စာသား အတိအကျပါမှ တွက်အောင်လုပ်ပါ
for _, r in b_df.iterrows():
    category_name = r['Category']
    limit_val = r['Limit']
    
    # တွက်ချက်မှု: စာရင်းထဲမှာ Expense (ထွက်ငွေ) အမျိုးအစားထဲက သက်ဆိုင်ရာ Category ကို ရှာပြီး ပေါင်းမယ်
    used = data[(data["Type"] == text['exp_opt']) & (data["Category"] == category_name)]["Amount"].sum()
    
    # Progress Bar နဲ့ အချက်အလက် ပြသခြင်း
    st.sidebar.write(f"**{category_name}**: {used:,.0f} / {limit_val:,.0f}")
    
    # ရာခိုင်နှုန်းတွက်ပြီး Progress Bar ပြခြင်း
    progress_pct = min(used / limit_val, 1.0) if limit_val > 0 else 0
    
    # ရာခိုင်နှုန်းပေါ်မူတည်ပြီး အရောင်သတ်မှတ်ခြင်း
    if progress_pct < 0.5:
        bar_color = "#2ECC71"  # အစိမ်း (၅၀% အောက်)
    elif progress_pct < 0.75:
        bar_color = "#F1C40F"  # အဝါ (၅၀% - ၇၅%)
    else:
        bar_color = "#E74C3C"  # အနီ (၇၅% အထက်)

    # HTML/CSS သုံးပြီး Progress Bar ဖန်တီးခြင်း
    st.sidebar.markdown(f"""
        <div style="background-color: #233554; border-radius: 5px; height: 10px; width: 100%;">
            <div style="background-color: {bar_color}; height: 10px; width: {progress_pct * 100}%; border-radius: 5px;"></div>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.write("") # အောက်ကဟာနဲ့ ကပ်မသွားအောင် နေရာချန်ပေးခြင်း
    
    # ဘတ်ဂျက်ကျော်ရင် သတိပေးချက်
    if used > limit_val:
        st.sidebar.error("⚠️ ဘတ်ဂျက်ကျော်လွန်နေပါပြီ")

# 🎨 USER CUSTOM COLORS SETUP FOR PIE CHARTS (SIDEBAR BOTTOM)
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#64FFDA;'>🎨 Pie Chart Colors</h3>", unsafe_allow_html=True)
user_color_1 = st.sidebar.color_picker("Chart Color - Theme A", "#64FFDA")
user_color_2 = st.sidebar.color_picker("Chart Color - Theme B", "#FF6B6B")
custom_colors = [user_color_1, user_color_2]

# --- 5. MAIN DASHBOARD ---
ti = data[data["Type"].str.contains("Income", na=False)]["Amount"].sum() if not data.empty else 0
te = data[data["Type"].str.contains("Expense", na=False)]["Amount"].sum() if not data.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric(text['total_inc'], f"{ti:,.0f} K")
col2.metric(text['total_exp'], f"{te:,.0f} K")
col3.metric(text['net_bal'], f"{(ti - te):,.0f} K")
st.divider() 

# 6. EXCEL STYLE TABLE - ဇယားကို ပြန်ပြင်ခြင်း
st.subheader(text['tx_records']) # ဒီလိုင်းကို ဘယ်ဘက်အစွန်ဆုံးထိ ကပ်လိုက်ပါ
if not data.empty:
    df_v = data.copy()
    df_v["Income"] = df_v.apply(lambda x: x["Amount"] if "Income" in str(x["Type"]) else 0, axis=1)
    df_v["Expense"] = df_v.apply(lambda x: x["Amount"] if "Expense" in str(x["Type"]) else 0, axis=1)

    total_row = pd.DataFrame([{"Date": "TOTAL", "Type": "", "Category": "", "Income": df_v["Income"].sum(),
                               "Expense": df_v["Expense"].sum(), "Payment Method": "", "Receipt": ""}])
    
    final_table = pd.concat([df_v[["Date", "Type", "Category", "Income", "Expense", "Payment Method", "Receipt"]], total_row])

    edited = st.data_editor(final_table, use_container_width=True, num_rows="dynamic")

    if st.button(text['save_changes']):
        clean_df = edited[edited["Date"] != "TOTAL"].copy()
        clean_df["Amount"] = clean_df["Income"] + clean_df["Expense"]
        
        # ၁။ Type ကို Language သဘောတရားနဲ့ အညီ ပြန်သတ်မှတ်မယ်
        clean_df["Type"] = clean_df.apply(lambda x: text['inc_opt'] if x["Income"] > 0 else text['exp_opt'], axis=1)
        
        final_save = clean_df[["Date", "Type", "Category", "Amount", "Payment Method", "Receipt"]]
        final_save.to_csv(FILES['db'], index=False)
        
        # ၂။ Savings တွေကို အရင်အတိုင်း ပြန်တွက်မယ်
        if os.path.exists(FILES['savings']):
            s_df = pd.read_csv(FILES['savings'])
            s_df['Saved'] = 0 
            for index, row in s_df.iterrows():
                goal = row['Goal']
                total = final_save[
                    (final_save["Type"] == text['exp_opt']) & 
                    (final_save['Category'] == goal)
                ]['Amount'].sum()
                s_df.at[index, 'Saved'] = total
            s_df.to_csv(FILES['savings'], index=False)
        
        # ၃။ ပြီးရင် st.rerun() လုပ်လိုက်တာနဲ့ 
        # t3 (Debt Tab) က Database အသစ်ကို ပြန်ဖတ်ပြီး Progress Bar တွေကို အလိုအလျောက် ပြင်ပေးသွားပါလိမ့်မယ်။
        st.success("ဒေတာများနှင့် Savings စုဆောင်းငွေများ အသစ်ပြန်တွက်ပြီးပါပြီ!")
        st.rerun()
# PIE CHARTS & INSIGHTS/RECOMMENDATIONS
if not data.empty:
    st.divider()
    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        inc_data = data[data["Type"].str.contains("Income", na=False)]
        if not inc_data.empty:
            fig_i = px.pie(inc_data, values="Amount", names="Category", title=text['inc_chart'], hole=0.4,
                           template="plotly_dark", color_discrete_sequence=custom_colors)
            fig_i.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_i, use_container_width=True)

            top_inc = inc_data.groupby("Category")["Amount"].sum().idxmax()
            if ti < 500000:
                ai_inc_en = f"**Analysis:**\n* Total monthly inflow is currently low ({ti:,.0f} K).\n* High concentration dependency detected on a single category: '{top_inc}'.\n\n**Recommendations:**\n* Actively seek secondary revenue channels or freelance tasks to distribute risk.\n* Build a basic micro-business model to increase operational capital."
                ai_inc_mm = f"**သုံးသပ်ချက်:**\n* လက်ရှိ စုစုပေါင်း လစဉ်ဝင်ငွေပမာဏသည် နည်းပါးနေပါသေးသည် ({ti:,.0f} K)။\n* ဝင်ငွေစီးဆင်းမှုသည် '{top_inc}' အပေါ်တွင်သာ အဓိက မှီခိုနေရကြောင်း တွေ့ရှိရပါသည်။\n\n**အကြံပြုချက်များ:**\n* Ngweကြေးဆိုင်ရာ စိုးရိမ်ရမှုကို လျှော့ချရန် ဆိုက်ဒ်လိုင်းအလုပ်များနှင့် အခြားဝင်ငွေလမ်းကြောင်းသစ်များကို ရှာဖွေပါ။\n* လည်ပတ်ငွေ ပိုမိုတိုးပွားလာစေရန် အခြေခံ စီးပွားရေးမော်ဒယ်အသေးစားများ ဖော်ထုတ်လုပ်ကိုင်သင့်ပါသည်။"
            else:
                ai_inc_en = f"**Analysis:**\n* Core income generation is operating with great stability.\n* The primary engine driving this capital growth vector is '{top_inc}'.\n\n**Recommendations:**\n* Reallocate a fixed percentage of this cash flow into mid-term investment structures.\n* Scale automated configurations to seamlessly cultivate passive interest layers."
                ai_inc_mm = f"**သုံးသပ်ချက်:**\n* အဓိက ဝင်ငွေစီးဆင်းမှု စနစ်သည် အလွန်တည်ငြိမ် ကောင်းမွန်သော အခြေအနေတွင် ရှိနေပါသည်။\n* ဝင်ငွေတိုးပွားမှုကို မောင်းနှင်ပေးနေသည့် ပင်မရင်းမြစ်မှာ '{top_inc}' ဖြစ်ကြောင်း တွေ့ရှိရပါသည်။\n\n**အကြံပြုချက်များ:**\n* ရရှိလာသော ပိုလျှံငွေများထဲမှ သတ်မှတ်ရာခိုင်နှုန်းတစ်ခုကို ကာလလတ် ရင်းနှီးမြှုပ်နှံမှုများထဲသို့ ပြောင်းရွှေ့ခွဲဝေပါ။\n* ပက်ဆိဗ်ဝင်ငွေ (Passive Income) ရရှိစေမည့် အလိုအလျောက် စနစ်များကို စတင်တည်ဆောက်ပါ။"
            render_ai_box(text['analysis_title'], ai_inc_en, ai_inc_mm)

    with c_chart2:
        exp_data = data[data["Type"].str.contains("Expense", na=False)]
        if not exp_data.empty:
            fig_e = px.pie(exp_data, values="Amount", names="Category", title=text['exp_chart'], hole=0.4,
                           template="plotly_dark", color_discrete_sequence=custom_colors)
            fig_e.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_e, use_container_width=True)

            top_exp = exp_data.groupby("Category")["Amount"].sum().idxmax()
            top_exp_amt = exp_data.groupby("Category")["Amount"].sum().max()
            pct = (top_exp_amt / te) * 100 if te > 0 else 0
            if pct > 40:
                ai_exp_en = f"**Analysis:**\n* Critical spending outflow detected! **'{top_exp}'** consumes a massive {pct:.1f}% of total usage.\n* Structural capital is leaving the loop via a single dominant channel.\n\n**Recommendations:**\n* Immediately enforce strict sub-budget ceilings on **'{top_exp}'** to contain leaks.\n* Postpone non-essential operations inside this specific field for the next 30 days."
                ai_exp_mm = f"**သုံးသပ်ချက်:**\n* အသုံးစရိတ် ယိုစိမ့်မှု ကြီးမားစွာ တွေ့ရပြီး **'{top_exp}'** သည် စုစုပေါင်းထွက်ငွေ၏ {pct:.1f}% အထိ ရှိနေပါသည်။\n* Ngweကြေးအမြောက်အမြားသည် ကဏ္ဍတစ်ခုတည်းမှ တဆင့် အဓိက ထွက်ခွာနေကြောင်း တွေ့ရှိရပါသည်။\n\n**အကြံပြုချက်များ:**\n* ယိုစိမ့်မှုများကို ထိန်းချုပ်ရန် **'{top_exp}'** ကဏ္ဍတွင် တင်းကျပ်သော ဘတ်ဂျက်ကန့်သတ်ချက်ကို ချက်ချင်း သတ်မှတ်ပါ။\n* လာမည့် ရက် ၃၀ အတွင်း အဆိုပါကဏ္ဍရှိ မဖြစ်မနေ မဟုတ်သော အသုံးစရိတ်များကို အတတ်နိုင်ဆုံး ဆိုင်းငံ့ထားပါ။"
            else:
                ai_exp_en = f"**Analysis:**\n* Outflow patterns are beautifully balanced and evenly distributed across targets.\n* Total operations are protected because no individual sector is capturing excessive weight.\n\n**Recommendations:**\n* Maintain this identical structural allocation format through the next financial tracking phase.\n* Routinely audit minor elements to ensure unexpected cost spikes do not distort this layout."
                ai_exp_mm = f"**သုံးသပ်ချက်:**\n* အသုံးစရိတ် ထွက်ရှိမှုပုံစံသည် မျှတမှုရှိပြီး သတ်မှတ်ထားသော ကဏ္ဍများအလိုက် ညီတူညီမျှ ရှိနေပါသည်။\n* ကဏ္ဍတစ်ခုတည်းတွင် ကုန်ကျစရိတ် ပုံမနေသည့်အတွက် အထွေထွေ လည်ပတ်မှုကို မထိခိုက်စေဘဲ ဘေးကင်းပါသည်။\n\n**အကြံပြုချက်များ:**\n* လာမည့် ဘဏ္ဍာရေးကာလများတွင်လည်း ယခုကဲ့သို့ စနစ်တကျ ခွဲဝေသုံးစွဲမှု ပုံစံအတိုင်း ဆက်လက် ထိန်းသိမ်းပါ။\n* မမျှော်လင့်ဘဲ ကုန်ကျစရိတ်များ ရုတ်တရက် မြင့်တက်မလာစေရန် အသေးစား စရိတ်စကများကို ပုံမှန် စစ်ဆေးပါ။"
            render_ai_box(text['analysis_title'], ai_exp_en, ai_exp_mm)

# --- 7. TABS 9 ခု ---
st.divider()
# အရင်က ၈ ခုနေရာမှာ အခု ၉ ခုဖြစ်သွားပါပြီ
t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs(text['tab_titles'])

with t1:
    with st.form("tab_b"):
        bc = st.text_input(text['cat_name'])
        bl = st.number_input(text['limit_amt'], min_value=0.0)
        
        if st.form_submit_button(text['set_budget']):
            # ဘတ်ဂျက်အသစ် ထည့်သွင်းခြင်း
            new_budget = pd.DataFrame([[bc, bl]], columns=b_df.columns)
            pd.concat([b_df, new_budget], ignore_index=True).to_csv(FILES['budget'], index=False)
            st.success("ဘတ်ဂျက်အသစ် ထည့်သွင်းပြီးပါပြီ!")
            st.rerun() # အဆင့် (၃) - Page ကို Refresh လုပ်ပေးခြင်း

    # ဘတ်ဂျက်ဇယား ပြင်ဆင်ခြင်း
    edited_b = st.data_editor(b_df, use_container_width=True, num_rows="dynamic", key="editor_b")
    
    if st.button(text['save_changes'], key="btn_save_b"):
        edited_b.to_csv(FILES['budget'], index=False)
        st.success(text['db_updated'])
        st.rerun() # အဆင့် (၃) - ပြင်ဆင်ပြီးတာနဲ့ Page ကို Refresh လုပ်ပေးခြင်း

    # AI Analysis အပိုင်း
    if not b_df.empty:
        ai_b_en = "**Analysis:**\n* Sub-budgets have been initialized and loaded inside active storage.\n* Real-time monitoring vectors are fully functional across the configured parameters.\n\n**Recommendations:**\n* Ensure the total combined budget threshold never breaches 70% of total expected incoming revenue.\n* Adjust allocation weights monthly based on the real expenditure feedback loop."
        ai_b_mm = "**သုံးသပ်ချက်:**\n* ကဏ္ဍအလိုက် ဘတ်ဂျက်ကန့်သတ်ချက်များကို လက်ရှိစနစ်ထဲတွင် အောင်မြင်စွာ ထည့်သွင်းထားပြီး ဖြစ်ပါသည်။\n* သတ်မှတ်ထားသော ဘောင်များအတွင်း ကုန်ကျစရိတ်များကို အချိန်နဲ့တပြေးညီ ကောင်းမွန်စွာ စောင့်ကြည့်နိုင်ပြီ ဖြစ်ပါသည်။\n\n**အကြံပြုချက်များ:**\n* ဘတ်ဂျက်စုစုပေါင်း ပမာဏသည် ခန့်မှန်းလစဉ်ဝင်ငွေ၏ ၇၀% ထက် မကျော်လွန်စေရန် ဂရုပြုပါ။\n* လက်တွေ့သုံးစွဲမှု မှတ်တမ်းများအပေါ် အခြေခံ၍ လစဉ် ဘတ်ဂျက်ပမာဏများကို လိုအပ်သလို အနည်းငယ် ညှိနှိုင်းပြင်ဆင်ပါ။"
    else:
        ai_b_en = "**Analysis:**\n* The budget matrix is currently empty with zero protective thresholds found.\n* Financial parameters are currently exposed to sudden impulsive spending vectors.\n\n**Recommendations:**\n* Set definite ceilings for your top three historical operational costs immediately.\n* Review past expenditure layers to find the optimal baseline numbers for each key category."
        ai_b_mm = "**သုံးသပ်ချက်:**\n* စနစ်ထဲတွင် ဘတ်ဂျက်သတ်မှတ်ချက်များ မရှိသေးဘဲ အကာအကွယ်မဲ့သော အခြေအနေ ဖြစ်နေပါသည်။\n* မမျှော်လင့်ဘဲ စိတ်အလိုလိုက် သုံးစွဲမိမည့် အန္တရာယ်နှင့် Ngweကြေးယိုစိမ့်မှုများ ဖြစ်ပေါ်နိုင်ပါသည်။\n\n**အကြံပြုချက်များ:**\n* အသုံးစရိတ် အများဆုံးဖြစ်လေ့ရှိသည့် အဓိက ကဏ္ဍ ၃ ခုအတွက် ကန့်သတ်ချက်များကို ချက်ချင်း သတ်မှတ်ပါ။\n* သင့်တင့်မျှတသော ဘတ်ဂျက်ပမာဏများ ရရှိစေရန် ယခင်လများက ကုန်ကျစရိတ်များကို ပြန်လည် ဆန်းစစ်ပါ။"
    
    render_ai_box(text['analysis_title'], ai_b_en, ai_b_mm)

with t2:
    st.subheader(text['tab_titles'][1]) 
    
    # 1. Goal အသစ်ထည့်ရန် Form (အရင်အတိုင်း)
    with st.form("tab_s"):
        sg, stg, sc = st.text_input(text['goal']), st.number_input(text['target']), st.number_input(text['current'])
        if st.form_submit_button(text['save_goal']):
            pd.concat([s_df, pd.DataFrame([[sg, stg, sc]], columns=s_df.columns)], ignore_index=True).to_csv(FILES['savings'], index=False)
            st.rerun()
            
    # 2. Savings ဇယားကို Editor နဲ့ ပြမယ်
    edited_s = st.data_editor(s_df, use_container_width=True, num_rows="dynamic", key="editor_s")
    if st.button(text['save_changes'], key="btn_save_s"):
        edited_s.to_csv(FILES['savings'], index=False)
        st.success(text['db_updated'])
        st.rerun()

    st.markdown("---")
    
   # 3. ဤနေရာမှာ New Entry နဲ့ ချိတ်ဆက်ပေးမည့် Logic
    for _, r in edited_s.iterrows():
        goal_name = r['Goal']
        target_val = r['Target']
        
        # [အရေးကြီး] "Expense (ထွက်ငွေ)" ဆိုတဲ့ စာသားအစား text['exp_opt'] ကို သုံးပါမယ်
        total_current = data[(data['Type'] == text['exp_opt']) & 
                             (data['Category'] == goal_name)]['Amount'].sum()
        
        st.write(f"### {goal_name}")
        st.write(f"စုဆောင်းပြီးပမာဏ: {total_current:,.0f} K / {target_val:,.0f} K")
        
        # Progress Bar အတွက်
        progress_val = float(total_current) / float(target_val) if target_val > 0 else 0
        st.progress(min(max(progress_val, 0.0), 1.0))
        st.markdown("---")

    # 3. AI Analysis (အရင်ကအတိုင်းပဲ)
    if not s_df.empty:
        low_savings = s_df[s_df["Saved"] / s_df["Target"] < 0.3]
        if not low_savings.empty:
            ai_s_en = f"**Analysis:**\n* Savings blueprints are correctly structured...\n* Critical velocity lag observed: **'{low_savings.iloc[0]['Goal']}'** is scaling slowly..."
            ai_s_mm = f"**သုံးသပ်ချက်:**\n* စုဆောင်းငွေ ရည်မှန်းချက်များအား စနစ်တကျ ထည့်သွင်း တည်ဆောက်ထားပြီး ဖြစ်ပါသည်။\n* တိုးတက်မှု နှေးကွေးခြင်း သတိပြုမိသည်- **'{low_savings.iloc[0]['Goal']}'** သည် သတ်မှတ်ချက်၏ ၃၀% အောက်တွင်သာ ရှိနေသေးပါသည်။"
        else:
            ai_s_en = "**Analysis:**\n* Outstanding savings metrics detected..."
            ai_s_mm = "**သုံးသပ်ချက်:**\n* စုဆောင်းငွေ တိုးတက်မှု အရှိန်အဟုန်သည် အလွန်ကောင်းမွန်ပြီး..."
    else:
        ai_s_en = "**Analysis:**\n* No active financial saving targets are registered..."
        ai_s_mm = "**သုံးသပ်ချက်:**\n* စနစ်ထဲတွင် စုဆောင်းငွေ ရည်မှန်းချက် ပန်းတိုင်များ တစ်ခုမှ မှတ်တမ်းတင်ထားခြင်း မရှိသေးပါ။"
        
    render_ai_box(text['analysis_title'], ai_s_en, ai_s_mm)

with t3:
    st.subheader("အကြွေးစာရင်းနှင့် Progress Bar များ")
    
    # ၁။ Category အသစ်ဖန်တီးရန်
    with st.form("new_debt_cat_form"):
        new_cat = st.text_input("အကြွေးစာရင်း အမည်သစ် (ဥပမာ- မေမေ, ကိုကြီး)")
        if st.form_submit_button("Create Debt Category"):
            if new_cat:
                if os.path.exists(FILES['debt_cats']):
                    cats_df = pd.read_csv(FILES['debt_cats'])
                else:
                    cats_df = pd.DataFrame(columns=['Category'])
                
                if new_cat not in cats_df['Category'].values:
                    cats_df = pd.concat([cats_df, pd.DataFrame([new_cat], columns=['Category'])], ignore_index=True)
                    cats_df.to_csv(FILES['debt_cats'], index=False)
                    st.success(f"'{new_cat}' ကို အကြွေးစာရင်းထဲ ထည့်လိုက်ပါပြီ။")
                    st.rerun()
                else:
                    st.warning("ဒီနာမည် ရှိပြီးသားပါ။")

    # ၂။ Transaction Data မှ အကြွေးတွက်ချက်ခြင်း
    if os.path.exists(FILES['debt_cats']) and os.path.exists(FILES['db']):
        debt_list = pd.read_csv(FILES['debt_cats'])['Category'].tolist()
        
        total_net_debt = 0
        
        for cat in debt_list:
            if cat in data['Category'].values:
                cat_data = data[data['Category'] == cat]
                
                # Language ပေါ်မူတည်ပြီး မှန်ကန်သော Type ကို စစ်ပါမယ်
                income = cat_data[cat_data['Type'] == text['inc_opt']]['Amount'].sum()
                expense = cat_data[cat_data['Type'] == text['exp_opt']]['Amount'].sum()
                
                net_debt = income - expense
                total_net_debt += net_debt
                
                st.write(f"### {cat}")
                st.write(f"လက်ကျန်အကြွေး: {net_debt:,.0f} K")
                # Progress bar (max 100000 K ကို အခြေခံထားသည်)
                progress = min(max(net_debt / 100000, 0), 1.0)
                st.progress(progress)
                st.divider()

        # ၃။ AI Analysis
        if total_net_debt > 0:
            ai_d_en = f"**Analysis:**\n* Total Outstanding Debt tracked: {total_net_debt:,.0f} K."
            ai_d_mm = f"**သုံးသပ်ချက်:**\n* လက်ရှိ စုစုပေါင်း အကြွေးကျန်မှာ {total_net_debt:,.0f} K ရှိပါသည်။"
        elif total_net_debt < 0:
            ai_d_en = "**Analysis:**\n* Credit balance positive."
            ai_d_mm = "**သုံးသပ်ချက်:**\n* အကြွေးစာရင်းမှာ ပိုနေပါသည်။"
        else:
            ai_d_en = "**Analysis:**\n* Clean debt ledger."
            ai_d_mm = "**သုံးသပ်ချက်:**\n* အကြွေးစာရင်း မျှတပါသည်။"
        
        render_ai_box(text['analysis_title'], ai_d_en, ai_d_mm)
    else:
        st.info("အကြွေးစာရင်း သို့မဟုတ် Transaction Data မရှိသေးပါ။")

with t4:
    st.subheader("📊 ဝင်ငွေ/ထွက်ငွေ နှိုင်းယှဉ်ချက် (Area Chart)")
    
    if not data.empty:
        # Data ပြင်ဆင်ခြင်း
        df_plot = data.copy()
        df_plot['Date'] = pd.to_datetime(df_plot['Date'])
        daily_flow = df_plot.groupby(['Date', 'Type'])['Amount'].sum().reset_index()
        
        # Area Chart ဆွဲခြင်း
        fig_area = px.area(daily_flow, x="Date", y="Amount", color="Type",
                           color_discrete_map={text['inc_opt']: '#2ECC71', text['exp_opt']: '#E74C3C'},
                           template="plotly_dark")
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                               hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_area, use_container_width=True)
        
        # AI သုံးသပ်ချက် (render_ai_box ကို သုံးပါမယ်)
        total_inc = daily_flow[daily_flow['Type'] == text['inc_opt']]['Amount'].sum()
        total_exp = daily_flow[daily_flow['Type'] == text['exp_opt']]['Amount'].sum()
        net = total_inc - total_exp
        
        # AI Text များ
        if total_inc > total_exp:
            ai_en = f"**Analysis:** Financial performance is strong. Income exceeds expenses by {net:,.0f} K."
            ai_mm = f"**သုံးသပ်ချက်:** ငွေကြေးအခြေအနေ တောင့်တင်းပါသည်။ ဝင်ငွေသည် ထွက်ငွေထက် {net:,.0f} K ပိုများနေပါသည်။"
        elif total_inc < total_exp:
            ai_en = f"**Analysis:** Warning! Expenses exceed income by {abs(net):,.0f} K. Please monitor spending."
            ai_mm = f"**သုံးသပ်ချက်:** သတိပြုပါ! ထွက်ငွေသည် ဝင်ငွေထက် {abs(net):,.0f} K ပိုများနေပါသည်။ အသုံးစရိတ်များကို ပြန်လည်စစ်ဆေးပါ။"
        else:
            ai_en = "**Analysis:** Income and expenses are balanced."
            ai_mm = "**သုံးသပ်ချက်:** ဝင်ငွေနှင့် ထွက်ငွေ ပမာဏ တူညီနေပါသည်။"
            
        # render_ai_box ကို ခေါ်သုံးခြင်း (t1, t2 တွေလိုပဲ)
        render_ai_box(text['analysis_title'], ai_en, ai_mm)
        
    else:
        st.warning("ပြသရန် Data မရှိသေးပါ။")

with t5:
    st.subheader("💳 " + text['methods_used']) # Header လေးတော့ ထည့်ပေးထားတယ်
    if not data.empty:
        fig_p = px.pie(data, values="Amount", names="Payment Method", 
                       template="plotly_dark", color_discrete_sequence=custom_colors)

        # FLOATING STYLE
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

        # Payment Tab Analysis
        top_method = data.groupby("Payment Method")["Amount"].sum().idxmax()
        ai_p_en = f"**Analysis:**\n* Heavy terminal transaction reliance detected centered inside the **'{top_method}'** system.\n* Channel concentration risk is high if this single system experiences tech server issues.\n\n**Recommendations:**\n* Maintain secondary cash or bank backup buffers to prevent sudden transactional lockouts.\n* Audit digital wallets frequently to ensure transfer limit caps do not stall large urgent items."
        ai_p_mm = f"**သုံးသပ်ချက်:**\n* လက်ရှိတွင် ငွေပေးချေမှု အများစုအတွက် **'{top_method}'** စနစ်တစ်ခုတည်းကိုသာ အဓိက အသုံးပြုနေကြောင်း တွေ့ရပါသည်။\n* ၎င်းစနစ်တစ်ခုတည်း နည်းပညာပိုင်းဆိုင်ရာ ချို့ယွင်းချက်ဖြစ်ပေါ်ပါက လုပ်ငန်းလည်ပတ်မှု ကြန့်ကြာနိုင်သည့် စွန့်စားရမှု ရှိပါသည်။\n\n**အကြံပြုချက်များ:**\n* ငွေပေးချေမှုများ လုံးဝရပ်တန့်မသွားစေရန် အခြားဘဏ်စနစ် သို့မဟုတ် လက်ငင်းငွေသား (Cash) အရန် ထားရှိပါ။\n* အရေးကြီး လုပ်ငန်းကိစ္စများတွင် ငွေလွှဲပမာဏ ကန့်သတ်ချက် (Limits) ကြောင့် မကြန့်ကြာစေရန် ဒစ်ဂျစ်တယ်ပိုက်ဆံအိတ်များကို စစ်ဆေးပါ။"
    else:
        ai_p_en = "**Analysis:**\n* Method routing matrix is completely blank with zero payment tracking vectors recorded."
        ai_p_mm = "**သုံးသပ်ချက်:**\n* ငွေပေးချေမှုစနစ် မှတ်တမ်းများ မရှိသေးသည့်အတွက် သုံးစွဲမှုပုံစံ ခွဲခြမ်းစိတ်ဖြာရန် ဒေတာ မလုံလောက်သေးပါ။"
    
    render_ai_box(text['analysis_title'], ai_p_en, ai_p_mm)

with t6:
    st.subheader("🧾 " + text['upload_receipt'])
    
    # ၁။ Transaction Record ကို ရွေးချယ်ခိုင်းခြင်း
    # "နေ့စွဲ - ခေါင်းစဉ် (ပမာဏ)" ပုံစံနဲ့ ပြပေးမယ်
    options = [f"{i}: {row['Date']} | {row['Category']} ({row['Amount']} K)" for i, row in data.iterrows()]
    selected_idx = st.selectbox("ပြေစာ ပူးတွဲမည့် စာရင်းကို ရွေးပါ", range(len(options)), format_func=lambda x: options[x])
    
    # ၂။ File Uploader
    uploaded_file = st.file_uploader("ပြေစာ ပုံတင်ရန်", type=["jpg", "png", "pdf"])
    
    # ၃။ သိမ်းဆည်းခြင်း
    if st.button("ပြေစာ သိမ်းဆည်းမည်"):
        if uploaded_file is not None:
            # receipts ဖိုင်ထဲမှာ သိမ်းမယ်
            file_name = f"receipt_{selected_idx}.png"
            file_path = os.path.join("receipts", file_name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Database ရဲ့ Receipt Column ထဲကို File Path သွင်းပေးခြင်း
            data.at[selected_idx, 'Receipt'] = file_path
            data.to_csv(FILES['db'], index=False)
            st.success("ပြေစာအား အောင်မြင်စွာ ပူးတွဲပြီးပါပြီ!")
            st.rerun() # ပြောင်းလဲသွားတာကို ချက်ချင်းမြင်ရအောင်
        else:
            st.warning("ကျေးဇူးပြု၍ ပြေစာဖိုင်ကို ဦးစွာတင်ပေးပါ။")

    # ၄။ ကိုကိုကြိုက်တဲ့ AI Analysis (မပြောင်းထားပါဘူး)
    ai_rc_en = "**Analysis:**\n* Document storage repository is armed and ready to index scanned image assets.\n* Digital validation layer is active to back up database entries with physical receipts.\n\n**Recommendations:**\n* Attach high-definition receipt images for all large business-related corporate costs.\n* Use this structured archive to match tax deductor compliance protocols seamlessly each season."
    ai_rc_mm = "**သုံးသပ်ချက်:**\n* ပြေစာများနှင့် စာရွက်စာတမ်းများ သိမ်းဆည်းမည့်စနစ်သည် အဆင်သင့်ဖြစ်ပြီး စနစ်တကျ အလုပ်လုပ်နေပါသည်။\n* ဒေတာဘေ့စ်ရှိ စာရင်းများကို ခိုင်မာစေရန် ဒစ်ဂျစ်တယ် ပြေစာပုံရိပ်များဖြင့် ပူးတွဲ သိမ်းဆည်းနိုင်ပြီ ဖြစ်ပါသည်။\n\n**အကြံပြုချက်များ:**\n* လုပ်ငန်းနှင့် သက်ဆိုင်သော ကြီးမားသော ကုန်ကျစရိတ်များအတွက် ပြေစာပုံရိပ်များကို မပျက်မကွက် တင်ထားပါ။\n* နှစ်ချုပ် စာရင်းဇယားများနှင့် အခွန်ဆိုင်ရာ စစ်ဆေးမှုများတွင် အဆင်ပြေစေရန် ဤမှတ်တမ်းကို စနစ်တကျ အသုံးချပါ။"
    render_ai_box(text['analysis_title'], ai_rc_en, ai_rc_mm)

with t7:
    st.subheader(text['calendar_tab'])
    
    # ၁။ Data ကို ပြင်ဆင်ခြင်း
    # ကိုကို့ရဲ့ data ထဲက Date column ကို datetime ဖြစ်အောင်လုပ်မယ်
    df_cal = data.copy()
    df_cal['Date'] = pd.to_datetime(df_cal['Date'])
    
    # ၂။ လ/နှစ် ရွေးချယ်ခြင်း
    selected_year = st.selectbox("ခုနှစ် ရွေးပါ", sorted(df_cal['Date'].dt.year.unique(), reverse=True))
    selected_month = st.selectbox("လ ရွေးပါ", range(1, 13))
    
    # ၃။ ရွေးထားတဲ့ လ/နှစ် အတွက် Data ကို စစ်ထုတ်မယ်
    monthly_data = df_cal[(df_cal['Date'].dt.year == selected_year) & (df_cal['Date'].dt.month == selected_month)]
    
    # ၄။ ပြက္ခဒိန်ပုံစံနဲ့ ပြသခြင်း (နေ့အလိုက် ပေါင်းပေးမယ်)
    if not monthly_data.empty:
        daily_summary = monthly_data.groupby('Date')['Amount'].sum().reset_index()
        daily_summary['Date'] = daily_summary['Date'].dt.strftime('%Y-%m-%d')
        
        st.write(f"{selected_year} ခုနှစ်၊ {selected_month} လ အတွက် နေ့စဉ်သုံးစွဲမှု စာရင်း")
        st.bar_chart(daily_summary.set_index('Date'))
    else:
        st.warning("ဒီလအတွက် မှတ်တမ်းမရှိသေးပါ။")

with t8:
    st.subheader(text['calc_tab'])
    target = st.number_input("ပန်းတိုင် ပမာဏ (Target Amount):", min_value=1.0)
    days = st.number_input("ရက်ပေါင်း (Days):", min_value=1)
    
    if target > 0 and days > 0:
        daily_needed = target / days
        st.metric("နေ့စဉ် စုရန်ပမာဏ:", f"{daily_needed:,.0f} K")
        st.write(f"ပန်းတိုင်သို့ရောက်ရန် နေ့စဉ် {daily_needed:,.0f} K စုဆောင်းရန် လိုအပ်ပါသည်။")

with t9:
    st.subheader("📤 Data Backup & Management")
    
    # ၁။ Data Export / Backup Button
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Backup & Download Data (CSV)",
        data=csv,
        file_name='finance_backup.csv',
        mime='text/csv',
    )
    
    st.warning("အောက်ပါ Reset ခလုတ်သည် လက်ရှိ ဝင်ငွေ/ထွက်ငွေ မှတ်တမ်းများကို ဖျက်ပြီး Archive သို့ ပို့ဆောင်ပေးပါမည်။ (စုငွေ/အကြွေး မှတ်တမ်းများသာ ကျန်ရှိပါမည်။)")
    
    # ၂။ Trigger Reset Button
    if st.button("⚠️ Reset Monthly Data (Trigger)"):
        # Archive လုပ်ခြင်း
        if os.path.exists('finance_archive.csv'):
            data.to_csv('finance_archive.csv', mode='a', header=False, index=False)
        else:
            data.to_csv('finance_archive.csv', index=False)
            
        # စုငွေ နဲ့ အကြွေး ကို ချန်ပြီး ကျန်တာဖျက်မယ်
        # Type ထဲတွင် Savings သို့မဟုတ် Debts ပါသော Data များကိုသာ Filter လုပ်သည်
        df_new = data[data['Type'].isin(['Savings', 'Debts'])]
        df_new.to_csv(FILES['db'], index=False)
        
        st.success("လစဉ် စာရင်းရှင်းလင်းခြင်း အောင်မြင်ပါသည်။ စနစ်အား ပြန်လည်စတင်ရန် Refresh လုပ်ပေးပါ။")
        st.rerun()

    # ၃။ AI Analysis
    ai_ex_en = "**Analysis:**\n* Backup and data synchronization protocols are fully operational.\n* Monthly reset trigger is primed for manual maintenance cycles."
    ai_ex_mm = "**သုံးသပ်ချက်:**\n* အချက်အလက်များအား အရန်သိမ်းဆည်းခြင်း (Backup) နှင့် လစဉ်စာရင်းရှင်းလင်းခြင်း လုပ်ဆောင်ချက်များ အဆင်သင့်ရှိပါသည်။\n* လုပ်ငန်းလည်ပတ်မှုအတွက် လိုအပ်ပါက Trigger ခလုတ်ကို အသုံးပြု၍ စာရင်းများအား ရှင်းလင်းနိုင်ပါသည်။"
    render_ai_box(text['analysis_title'], ai_ex_en, ai_ex_mm)
