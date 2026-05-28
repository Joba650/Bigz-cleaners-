import streamlit as st
import datetime
import pandas as pd
import requests

# --- PAGE CONFIGURATION & THEME ANCHORS ---
st.set_page_config(
    page_title="BOSS.CO | Premium Laundry Ecosystem", 
    page_icon="🧺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ARCHITECTURAL STYLING ENGINE (CSS) ---
st.markdown("""
    <style>
        /* Global Typography & Background Elements */
        @import url('https://googleapis.com');
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Metric Cards Visual Upgrades */
        [data-testid="stMetricValue"] {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: #1E1B4B;
        }
        [data-testid="stMetricLabel"] {
            font-size: 13px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #6B7280;
        }
        
        /* Button Enhancements */
        div.stButton > button:first-child {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        
        /* Clean Subheaders */
        .section-header {
            font-size: 18px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 12px;
            border-left: 4px solid #4F46E5;
            padding-left: 10px;
        }
    </style>
""", unsafe_html=True)

# --- BACKEND WEBHOOK CONFIGURATION ---
# Configure your production webhooks here
EMAIL_WEBHOOK_URL = "https://formsubmit.co"
GSHEET_FORM_URL = "https://google.com"

# --- SYSTEM STATE INITIALIZATION ---
if "services" not in st.session_state:
    st.session_state["services"] = {
        "Wash & Fold": 500,
        "Dry Cleaning": 1200,
        "Ironing Only": 300,
        "Comforter / Blanket": 800
    }

if "orders" not in st.session_state:
    st.session_state["orders"] = [
        {"Order ID": "B-1001", "Date": "2026-05-25", "Client": "Alex Mwangi", "Total (KES)": 1300, "Status": "Delivered"},
        {"Order ID": "B-1002", "Date": "2026-05-26", "Client": "Beatrice Amina", "Total (KES)": 500, "Status": "Delivered"},
        {"Order ID": "B-1003", "Date": "2026-05-27", "Client": "Charles Ochieng", "Total (KES)": 2300, "Status": "Pending Delivery"},
        {"Order ID": "B-1004", "Date": "2026-05-28", "Client": "David Kiprop", "Total (KES)": 800, "Status": "Pending Delivery"},
    ]

# --- SIDEBAR NAVIGATOR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #4F46E5; font-size: 28px; font-weight: 800; letter-spacing: -1px; margin-bottom: 0;'>BOSS.CO</h1>", unsafe_html=True)
    st.markdown("<p style='text-align: center; font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; margin-top: 0;'>Laundry Management Hub</p>", unsafe_html=True)
    st.markdown("<br>", unsafe_html=True)
    
    role = st.selectbox("Navigate Module", ["Client Terminal", "Executive Control Room"])
    st.markdown("---")
    
    is_admin = False
    if role == "Executive Control Room":
        st.markdown("### Secure Gateway")
        password = st.sidebar.text_input("Access Token Key", type="password", placeholder="••••••••")
        if password == "boss123":
            is_admin = True
            st.sidebar.success("✓ Identity Confirmed")
        elif password != "":
            st.sidebar.error("✗ System Rejected Token")

# ==========================================
#        EXECUTIVE CONTROL ROOM (ADMIN)
# ==========================================
if role == "Executive Control Room" and is_admin:
    st.markdown("<h2 style='color: #1E1B4B; font-weight: 700; margin-bottom: 5px;'>📊 BOSS.CO Executive Control Tower</h2>", unsafe_html=True)
    st.markdown("<p style='color: #6B7280; font-size: 14px;'>Real-time metrics, system tariffs overview, and volumetric yield monitoring.</p>", unsafe_html=True)
    st.markdown("<br>", unsafe_html=True)
    
    # 1. Operational Key Metrics Row
    df_orders = pd.DataFrame(st.session_state["orders"])
    total_rev = df_orders["Total (KES)"].sum()
    total_count = len(df_orders)
    pending_count = len(df_orders[df_orders["Status"] == "Pending Delivery"])
    
    m1, m2, m3 = st.columns(3)
    with m1:
        with st.container(border=True):
            st.metric(label="Gross Accumulated Revenue", value=f"KES {total_rev:,}", delta="+12.4% vs Last Week")
    with m2:
        with st.container(border=True):
            st.metric(label="Volumetric Pipeline Orders", value=total_count, delta="+2 New Inbound")
    with m3:
        with st.container(border=True):
            st.metric(label="Outstanding COD Receivables", value=f"KES {df_orders[df_orders['Status']=='Pending Delivery']['Total (KES)'].sum():,}", delta="Unpaid", delta_color="inverse")
        
    st.markdown("<br>", unsafe_html=True)
    
    # 2. Main Analytics Workstation Split
    c1, c2 = st.columns([3, 2])
    
    with c1:
        st.markdown("<div class='section-header'>Chronological Yield Performance</div>", unsafe_html=True)
        df_daily = df_orders.groupby("Date")["Total (KES)"].sum().reset_index()
        st.line_chart(data=df_daily, x="Date", y="Total (KES)", height=260)
        
        st.markdown("<div class='section-header'>Live Central Operations Register</div>", unsafe_html=True)
        st.dataframe(df_orders, use_container_width=True, hide_index=True)
        
    with c2:
        st.markdown("<div class='section-header'>Global Tariff Modifier</div>", unsafe_html=True)
        st.caption("Editing indices below will instantaneously shift catalog pricing globally across all user portals.")
        
        updated_services = {}
        with st.container(border=True):
            for service, price in st.session_state["services"].items():
                new_price = st.number_input(
                    f"{service} Price (KES)", 
                    min_value=0, 
                    value=price, 
                    step=50, 
                    key=f"adm_cfg_{service}"
                )
                updated_services[service] = new_price
            
            st.markdown("<br>", unsafe_html=True)
            if st.button("Publish Updates to Cloud Catalog", use_container_width=True, type="primary"):
                st.session_state["services"] = updated_services
                st.toast("Global dynamic prices deployed!", icon="✅")
                st.rerun()

# --- SECURITY SYSTEM WALL ---
elif role == "Executive Control Room" and not is_admin:
    st.markdown("<br><br>", unsafe_html=True)
    with st.container(border=True):
        st.markdown("<h3 style='color: #DC2626; margin-top:0;'>🔒 Firewall Access Exception</h3>", unsafe_html=True)
        st.markdown("This control center strictly requires authentication tokens. Provide your valid administrator passkey in the sidebar panel to build data tables.")

# ==========================================
#             CLIENT TERMINAL VIEW
# ==========================================
else:
    st.markdown("<h1 style='color: #4F46E5; font-weight: 800; margin-bottom: 0;'>🧺 BOSS.CO</h1>", unsafe_html=True)
    st.markdown("<h3 style='color: #1F2937; margin-top: 5px; font-weight: 500;'>Premium Garment Care Concierge</h3>", unsafe_html=True)
    st.markdown("<p style='color: #6B7280; font-size: 15px;'>Select high-fidelity cleaning services. Deliveries are completely free. <b>Pay only after your items return spotless!</b></p>", unsafe_html=True)
    st.markdown("<br>", unsafe_html=True)
    
    # 1. Menu Grid Display
    st.markdown("<div class='section-header'>1. Interactive Service Catalog</div>", unsafe_html=True)
    
    col_menu = st.columns(len(st.session_state["services"]))
    selected_services = []
    
    for idx, (service, price) in enumerate(st.session_state["services"].items()):
        with col_menu[idx]:
            with st.container(border=True):
                st.markdown(f"<p style='font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 4px;'>{service}</p>", unsafe_html=True)
                st.markdown(f"<h3 style='color: #10B981; margin-top: 0; font-weight: 700;'>KES {price:,}</h3>", unsafe_html=True)
                st.markdown("<p style='font-size: 11px; color: #9CA3AF; margin-top: -10px;'>Per standard consignment unit</p>", unsafe_html=True)
                
                if st.checkbox("Select Service", key=f"user_select_{service}"):
                    selected_services.append({"name": service, "price": price})

    st.markdown("<br><br>", unsafe_html=True)

    # 2. Logistic Dispatch Interface Block
    st.markdown("<div class='section-header'>2. Logistics Coordination & Timelines</div>", unsafe_html=True)
    
    with st.form("client_logistics_form", clear_on_submit=False):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            pickup_date = st.date_input("Requested Pick-up Date", min_value=datetime.date.today())
            pickup_time = st.time_input("Preferred Pick-up Time Window")
        with f_col2:
            delivery_date = st.date_input("Target Delivery Date", min_value=datetime.date.today() + datetime.timedelta(days=1))
            delivery_time = st.time_input("Preferred Delivery Time Window")
            
        st.markdown("<hr style='border: 0.5px solid #E5E7EB;'>", unsafe_html=True)
        
        c_name = st.text_input("Full Name Identifier", placeholder="John Doe")
        c_phone = st.text_input("Mobile Contact Number (For M-PESA/Call Alerts)", placeholder="e.g., 0712345678")
        c_address = st.text_area("Physical Residential / Office Address Coordinates", placeholder="Apartment, Street Name, Estate/Area name")
        
