import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================
# PAGE CONFIGURATION
# =========================================
st.set_page_config(
    page_title="BIGZ CLEANERS",
    page_icon="🧺",
    layout="wide"
)

# =========================================
# CENTRAL MEMORY & PERSISTENT SESSION STATES
# =========================================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin@bigz.com": {
            "name": "Theophilus mose",
            "phone": "0116993710",
            "password": "admin123",
            "role": "admin",
            "verified": True
        },
        "sarachen@gmail.com": {
            "name": "Sarah Chen",
            "phone": "(03) 234-6600",
            "password": "password123",
            "role": "customer",
            "address": "123 Saved Address From Street, West, Buil, 4003",
            "verified": True,
            "saved_cards": ["•••• •••• •••• 4321"],
            "preferences": {"Detergent type": "Scented Organic", "Starched Shirts": "Medium Crispy Stiffness"}
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "current_email" not in st.session_state:
    st.session_state.current_email = ""
if "current_role" not in st.session_state:
    st.session_state.current_role = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_verification" not in st.session_state:
    st.session_state.pending_verification = None

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Detergent (L)": 180, 
        "Fabric Softener (L)": 95, 
        "Tags & Bags (Pcs)": 450
    }
if "staff" not in st.session_state:
    st.session_state.staff = ["Alex Chen", "Marix Mason", "John Doe", "Theophilus mose"]

if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "tracking": "BIGZ-12341", "customer": "Sarah Chen", "email": "sarachen@gmail.com",
            "service": "Wash & Fold (General Wear)", "quantity": "5 KG", "cost": 500,
            "pickup_logistics": "05/28/26 at 10:00 AM", "address": "123 Saved Address From Street",
            "payment_gateway": "M-Pesa Express", "status": "Pickup", "assigned_staff": "Alex Chen",
            "created_at": "05/26/26"
        },
        {
            "tracking": "BIGZ-12342", "customer": "Sarah Chen", "email": "sarachen@gmail.com",
            "service": "Wash, Dry, Iron & Fold", "quantity": "3 KG", "cost": 420,
            "pickup_logistics": "05/28/26 at 12:00 PM", "address": "123 Saved Address From Street",
            "payment_gateway": "Secure Card Payment Gateway", "status": "Washing", "assigned_staff": "Alex Staff",
            "created_at": "05/26/26"
        },
        {
            "tracking": "BIGZ-12344", "customer": "Sarah Chen", "email": "sarachen@gmail.com",
            "service": "Heavy Blanket / Duvet", "quantity": "1 Piece", "cost": 400,
            "pickup_logistics": "05/29/26 at 02:00 PM", "address": "123 Saved Address From Street",
            "payment_gateway": "M-Pesa Express", "status": "Drying", "assigned_staff": "Theophilus mose",
            "created_at": "05/26/26"
        }
    ]

# =========================================
# ADVANCED CUSTOM GRAPHICS INTERFACE CSS
# =========================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e3a8a, #0284c7);
    background-attachment: fixed;
}
.service-card { 
    background: white; 
    padding: 22px; 
    border-radius: 16px; 
    margin-bottom: 20px; 
    color: #0f172a; 
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); 
    border-top: 5px solid #2563eb;
}
.track-box { 
    background: #f8fafc; 
    color: #0f172a; 
    padding: 25px; 
    border-radius: 18px; 
    margin-top: 20px; 
    border-left: 6px solid #3b82f6; 
}
.footer { 
    text-align: center; 
    color: #94a3b8; 
    padding: 40px 0; 
    margin-top: 60px; 
    border-top: 1px solid rgba(255,255,255,0.1); 
}
div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# STANDARD BASE DATA DEFINITIONS
# =========================================
services = [
    {"name": "Wash & Fold (General Wear)", "price": 100, "unit": "KG", "type": "Wash & Fold"},
    {"name": "Wash, Dry, Iron & Fold", "price": 140, "unit": "KG", "type": "Wash & Fold"},
    {"name": "Heavy Blanket / Duvet", "price": 400, "unit": "Piece", "type": "Dry Clean"},
    {"name": "Official Suits (Jacket & Trousers)", "price": 500, "unit": "Suit", "type": "Dry Clean"},
    {"name": "Sneaker / Canvas Shoe Cleaning", "price": 200, "unit": "Pair", "type": "Wash & Fold"}
]

# =========================================
# PERSISTENT SYSTEM SIDEBAR CONTROL PANEL
# =========================================
st.sidebar.title("🧺 BIGZ CLEANERS")
if st.session_state.logged_in:
    user_email = st.session_state.current_email
    user_record = st.session_state.users[user_email]
    user_role = st.session_state.current_role
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 15px 0; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 20px;">
        <div style="width: 70px; height: 70px; background: #3b82f6; border-radius: 50%; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white;">
            {user_record['name'][0]}
        </div>
        <h4 style="color: white; margin: 0;">{user_record['name']}</h4>
        <p style="color: #cbd5e1; font-size: 12px; margin: 2px 0 0 0;">{user_role.upper()} HUB</p>
        <p style="color: #4ade80; font-size: 11px; margin-top: 6px;">● Secure Layer Connected</p>
    </div>
    """, unsafe_allow_html=True)

    if user_role == "customer":
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Service Dashboard", "My Profile Account", "Support Messaging Desk"])
    else:
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Main Operations Ledger", "User Accounts Profiles", "Inventory & Billings"])

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Log Out of Session", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_email = ""
        st.session_state.current_role = ""
        st.rerun()
else:
    st.sidebar.info("Awaiting verification access signatures.")

# =========================================
# LAYER A: SPLIT LANDING VIEW (UNAUTHENTICATED)
# =========================================
if not st.session_state.logged_in:
    left_hero, right_portal = st.columns([1.1, 0.9], gap="large")
    
    with left_hero:
        st.markdown("""
        <div style="padding: 10px 0;">
            <h1 style="color: white; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 15px;">
                PROFESSIONAL LAUNDRY,<br>MADE EASY FOR YOU &<br>YOUR BUSINESS.
            </h1>
            <p style="color: #cbd5e1; font-size: 18px; margin-bottom: 35px;">
                Track Orders, Manage Accounts, and Experience Convenience - All in One Unified Architecture.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("""
            <div style="background: white; padding: 22px; border-radius: 16px; min-height: 180px; color: #0f172a; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);">
                <span style="font-size: 32px;">📥</span>
                <h4 style="margin-top: 10px; font-weight: 700; color: #1e3a8a; margin-bottom: 5px;">FOR CLIENTS:</h4>
                <p style="font-size: 13px; color: #475569; line-height: 1.4; margin: 0;">
                    Schedule Pickups, Track Your Wash Status, and Manage Payments effortlessly.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_f2:
            st.markdown("""
            <div style="background: white; padding: 22px; border-radius: 16px; min-height: 180px; color: #0f172a; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);">
                <span style="font-size: 32px;">📊</span>
                <h4 style="margin-top: 10px; font-weight: 700; color: #581c87; margin-bottom: 5px;">FOR ADMINS & STAFF:</h4>
                <p style="font-size: 13px; color: #475569; line-height: 1.4; margin: 0;">
                    Streamline Operations, Assign Staff/Routes, and Monitor Resource Reserves.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        <div style="margin-top: 45px; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 25px;">
            <p style="color: #cbd5e1; font-style: italic; font-size: 15px; margin-bottom: 5px;">
                "Managing my laundry has never been simpler! Dynamic updates give complete peace of mind."
            </p>
            <p style="color: #60a5fa; font-weight: 600; font-size: 14px;">– Sarah Chen, Business Partner</p>
        </div>
        """, unsafe_allow_html=True)

    with right_portal:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: white; font-weight: 700;'>GET STARTED OR LOG IN</h2></div>", unsafe_allow_html=True)
        
        if st.session_state.pending_verification:
            st.markdown(f"""
            <div style="background: #fffbeb; border-left: 5px solid #d97706; padding: 20px; border-radius: 12px; color: #92400e; margin-bottom: 20px;">
                <h4 style="margin: 0 0 6px 0; font-weight: 700;">⚠️ Email Verification Security Loop</h4>
                <p style="font-size: 14px; margin: 0;">A system dispatch link has been pushed to: <b>{st.session_state.pending_verification}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Simulate Incoming Verification Email Confirm Link", use_container_width=True):
                email = st.session_state.pending_verification
                st.session_state.users[email]["verified"] = True
                st.session_state.pending_verification = None
                st.success("Account Authorization Verified! Proceed to sign in.")
                st.rerun()
                
            if st.button("❌ Deny Process Verification Framework / Return", use_container_width=True):
                st.session_state.pending_verification = None
                st.rerun()
        else:
            login_tab, signup_tab = st.tabs(["[ LOGIN ]", "[ SIGN UP ]"])
            
            with login_tab:
                st.markdown("<p style='color: #cbd5e1; font-weight: bold; margin-bottom: 15px;'>WELCOME BACK</p>", unsafe_allow_html=True)
                with st.form("login_panel_form"):
                    login_email = st.text_input("Registered Email Address", placeholder="name@domain.com")
                    login_password = st.text_input("Secure Account Password", type="password", placeholder="••••••••")
                    if st.form_submit_button("LOG IN TO DASHBOARD", use_container_width=True):
                        if login_email in st.session_state.users:
                            user = st.session_state.users[login_email]
                            if user["password"] == login_password:
                                if not user.get("verified", False):
                                    st.error("Account registration sequence is unverified. Halt process entry.")
                                else:
                                    st.session_state.logged_in = True
                                    st.session_state.current_user = user["name"]
