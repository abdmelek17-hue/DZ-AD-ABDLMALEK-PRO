import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# 1. إعدادات الأمان والمدير
ADMIN_PASSWORD = "ENS_MEDEA_2026"  # كلمة السر الخاصة بك للدخول كمدير

# تهيئة مخزن البيانات في المتصفح (Session State)
if 'blocked_users' not in st.session_state:
    st.session_state.blocked_users = ["spam@test.com"] # أمثلة فقط
if 'user_list' not in st.session_state:
    st.session_state.user_list = []

# 2. تنسيق الواجهة لتكون احترافية وباللغة العربية
st.set_page_config(page_title="DZ-Ad Pro AI", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #004aad; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 DZ-Ad Pro AI")
st.write("المساعد الذكي لكتابة إعلانات البيع في الجزائر")

# 3. نظام تسجيل الدخول بالإيميل
email = st.text_input("أدخل بريدك الإلكتروني للبدء:")

if email:
    if email in st.session_state.blocked_users:
        st.error("❌ هذا الحساب محظور. يرجى التواصل مع الإدارة.")
    else:
        if email not in st.session_state.user_list:
            st.session_state.user_list.append(email)
        
        st.success(f"مرحباً بك {email}")
        
        # إدخال مفتاح API (يمكنك وضعه برمجياً لاحقاً لزيادة الأمان)
        api_key = st.sidebar.text_input("مفتاح Gemini API:", type="password")
        
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # مدخلات التطبيق
            uploaded_file = st.file_uploader("ارفع صورة المنتج (اختياري)", type=["jpg", "png", "jpeg"])
            extra_info = st.text_input("تفاصيل إضافية (السعر، الولاية...):")
            phone = st.text_input("رقم الهاتف:")

            if st.button("توليد الإعلان ✨"):
                with st.spinner('جاري التحليل والكتابة...'):
                    try:
                        prompt = f"اكتب 3 إعلانات بالدارجة الجزائرية لمنتج. 1- رسمي لواد كنيس، 2- جذاب لفيسبوك، 3- أفار مستعجل. الإضافات: {extra_info}. الهاتف: {phone}"
                        if uploaded_file:
                            img = Image.open(uploaded_file)
                            response = model.generate_content([prompt, img])
                        else:
                            response = model.generate_content(prompt)
                        
                        st.markdown("### الإعلانات المقترحة:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"حدث خطأ في الاتصال: {e}")
        else:
            st.warning("👈 يرجى إدخال مفتاح API في القائمة الجانبية لتفعيل الذكاء الاصطناعي.")

# 4. لوحة تحكم المدير (مخفية)
st.write("---")
with st.expander("🔐 لوحة تحكم المدير"):
    pass_input = st.text_input("كلمة سر الإدارة:", type="password")
    if pass_input == ADMIN_PASSWORD:
        st.subheader("إدارة المستخدمين")
        col1, col2 = st.columns(2)
        
        with col1:
            target_block = st.selectbox("حظر مستخدم:", st.session_state.user_list)
            if st.button("تأكيد الحظر 🚫"):
                st.session_state.blocked_users.append(target_block)
                st.rerun()
        
        with col2:
            target_unblock = st.selectbox("إلغاء حظر:", st.session_state.blocked_users)
            if st.button("إزالة الحظر ✅"):
                st.session_state.blocked_users.remove(target_unblock)
                st.rerun()

