import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. GLOBAL SYSTEM CONFIGURATION & CONSTANTS
# ==============================================================================
DATABASE_FILE_PATH = "users_db.json"
APP_THEME_COLOR_PRIMARY = "#1e3a8a"
APP_THEME_COLOR_SECONDARY = "#0284c7"

# Active pricing engine initialization
if "laundry_service_catalog" not in st.session_state:
    st.session_state.laundry_service_catalog = [
        {"id": "srv_wash_fold", "name": "Laundry Washing", "price": 200.0, "unit": "7KG", "type": "Wash & Fold", "img": "https://images.unsplash.com/photo-1545173168-9f1947eebd01?w=500&auto=format&fit=crop&q=60", "desc": "Premium automated wash, crisp structural tumble fold, packed by batch."},
        {"id": "srv_carpet", "name": "Carpet Cleaning", "price": 150.0, "unit": "sqm", "type": "Specialty Clean", "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500&auto=format&fit=crop&q=60", "desc": "Deep fiber extraction therapy, sanitizing wash, high-heat air dry."},
        {"id": "srv_duvet", "name": "Duvet Cleaning", "price": 500.0, "unit": "Piece", "type": "Dry Clean", "img": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=500&auto=format&fit=crop&q=60", "desc": "Anti-allergen processing cycle optimized for heavy premium bedding comfort."}
    ]

st.set_page_config(
    page_title="BIGZ CLEANERS AI",
    page_icon="🧺",
    layout="wide"
)

# ==============================================================================
# 2. PERSISTENT STORAGE LAYER ENGINE (WITH SECURITY LAYERS)
# ==============================================================================
def load_user_database() -> dict:
    default_records = {
        "admin@bigz.com": {"name": "Theophilus mose", "phone": "0116993710", "password": "admin123", "role": "admin", "verified": True},
        "sarachen@gmail.com": {
            "name": "Sarah Chen", "phone": "(03) 234-6600", "password": "password123", "role": "customer",
            "address": "123 Saved Address From Street, West, Buil, 4003", "verified": True,
            "wallet_points": 250, "saved_cards": ["•••• •••• •••• 4321"],
            "subscription": "Standard Core Monthly Plan", "subscription_status": "Active",
            "preferences": {"Detergent": "Scented Organic Premium", "Water Temp": "Cold Wash Mode", "Folding Style": "Classic Shelf Fold", "Starch Level": "Medium Crispy Stiffness"}
        }
    }
    if not os.path.exists(DATABASE_FILE_PATH):
        with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as file_handle:
            json.dump(default_records, file_handle, indent=4)
        return default_records
    try:
        with open(DATABASE_FILE_PATH, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (json.JSONDecodeError, IOError):
        return default_records

def save_user_profile(email_key: str, profile_data: dict) -> None:
    current_database = load_user_database()
    current_database[email_key.lower().strip()] = profile_data
    with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as file_handle:
        json.dump(current_database, file_handle, indent=4)

st.session_state.users = load_user_database()

# ==============================================================================
# 3. INITIALIZE STATE RUNTIME MEMORY
# ==============================================================================
state_defaults = {
    "logged_in": False, "current_user": "", "current_email": "", "current_role": "",
    "selected_service_id": "srv_wash_fold", "admin_filter_metric": "Dashboard View",
    "messages": [{"sender": "admin@bigz.com", "recipient": "sarachen@gmail.com", "sender_name": "Theophilus (Admin)", "message": "Hello Sarah, welcome to your secure AI support desk channel thread!", "time": "12:00:00"}],
    "price_alerts": [{"text": "Welcome to BIGZ Cleaners AI Operations Command Panel.", "timestamp": "System Initialization"}],
    "pending_verification": None, "security_mfa_passed": False,
    "delivery_riders": [
        {"name": "David", "location": "Nakuru Town", "orders": 4, "status": "On Delivery"},
        {"name": "Kelvin", "location": "Njoro", "orders": 2, "status": "Pickup"}
    ],
    "notifications": [
        "Order #1023 delayed by 15 mins",
        "New pickup request received",
        "Payment confirmed via encrypted handshake"
    ],
    "recent_orders": [
        {"id": "#1023", "customer": "Brian Mwangi", "service": "Laundry Washing", "status": "Washing"},
        {"id": "#1024", "customer": "Mercy Achieng", "service": "Duvet Cleaning", "status": "Ready"},
        {"id": "#1025", "customer": "Kevin Otieno", "service": "Carpet Cleaning", "status": "Out for Delivery"}
    ],
    "staff_activity": [
        {"name": "John", "role": "Pickup Rider", "active": True},
        {"name": "Mercy", "role": "Ironing", "active": True},
        {"name": "Alex", "role": "Washing", "active": False}
    ],
    "orders": [
        {"tracking": "BIGZ-1023", "customer": "Brian Mwangi", "email": "brian@mwangi.com", "service": "Laundry Washing", "quantity": "1 Batch", "bag_size": "Medium", "detergent": "Standard Clean Formula", "cost": 200.0, "pickup_logistics": "Immediate", "address": "Nakuru Town", "payment_gateway": "M-Pesa (Submitted)", "status": "Washing", "assigned_staff": "John", "created_at": "2026-05-27"},
        {"tracking": "BIGZ-1024", "customer": "Mercy Achieng", "email": "mercy@achieng.com", "service": "Duvet Cleaning", "quantity": "1 Batch", "bag_size": "Large", "detergent": "Hypoallergenic Pure-Soft", "cost": 500.0, "pickup_logistics": "Scheduled", "address": "Njoro", "payment_gateway": "M-Pesa (Submitted)", "status": "Received", "assigned_staff": "Kelvin", "created_at": "2026-05-28"},
        {"tracking": "BIGZ-1025", "customer": "Kevin Otieno", "email": "kevin@otieno.com", "service": "Carpet Cleaning", "quantity": "4 sqm", "bag_size": "Custom Selection", "detergent": "Max-Stain Professional Armor", "cost": 600.0, "pickup_logistics": "Immediate", "address": "Nakuru Town", "payment_gateway": "Secure Card (Confirmed)", "status": "Out for Delivery", "assigned_staff": "David", "created_at": "2026-05-28"}
    ]
}
for state_key, default_value in state_defaults.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value

# ==============================================================================
# 4. GRAPHICAL UI ELEMENT CUSTOMIZATION (CSS) WITH STYLED SERVICE CARDS
# ==============================================================================
st.markdown(f"""
<style>
    @keyframes logoReveal {{
        0% {{ transform: scale(0.3) rotate(-5deg); opacity: 0; filter: blur(10px); }}
        50% {{ transform: scale(1.05) rotate(2deg); filter: blur(0px); }}
        70% {{ transform: scale(0.98) rotate(-1deg); }}
        100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
    }}
    @keyframes bubblePulse {{
        0%, 100% {{ transform: translateY(0px); box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }}
        50% {{ transform: translateY(-8px); box-shadow: 0 10px 30px rgba(2, 132, 199, 0.6); }}
    }}
    .animated-logo-container {{
        text-align: center;
        padding: 30px 10px;
        animation: logoReveal 1.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }}
    .animated-logo-icon {{
        font-size: 64px;
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        width: 110px;
        height: 110px;
        line-height: 110px;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.25);
        animation: bubblePulse 3s ease-in-out infinite;
    }}
    .animated-logo-text {{
        color: white;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-top: 15px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5), 0 0 20px rgba(37, 99, 235, 0.5);
    }}
    .animated-logo-tagline {{
        color: #93c5fd;
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 5px;
        font-weight: 600;
        opacity: 0.85;
    }}
    .stApp {{
        background: linear-gradient(135deg, #020617, #0f172a, #1e3a8a, #0284c7);
        background-attachment: fixed;
    }}
    .mobile-frame {{
        background-color: #f8fafc;
        border-radius: 32px;
        padding: 0px;
        color: #1e293b;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        max-width: 450px;
        margin: 0 auto;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }}
    .mobile-header {{
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        padding: 24px;
        border-bottom-left-radius: 24px;
        border-bottom-right-radius: 24px;
        box-shadow: 0 10px 15px -3px rgba(37,99,235,0.3);
    }}
    .admin-avatar {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background-color: rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 20px;
    }}
    .revenue-box {{
        background-color: rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 16px;
        margin-top: 20px;
        backdrop-filter: blur(4px);
    }}
    .stat-card {{
        background-color: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .data-card {{
        background-color: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #f1f5f9;
        margin-bottom: 12px;
    }}
    .status-badge-blue {{
        background-color: #dbeafe;
        color: #1d4ed8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }}
    .status-badge-green {{
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }}
    .notification-orange {{
        background-color: #fff7ed;
        border: 1px solid #ffedd5;
        color: #c2410c;
        border-radius: 16px;
        padding: 16px;
        font-size: 14px;
        margin-bottom: 12px;
    }}
    .analytics-gradient {{
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        color: white;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(37,99,235,0.2);
    }}
    .bottom-nav {{
        background-color: white;
        border-top: 1px solid #e2e8f0;
        padding: 16px;
        display: flex;
        justify-content: space-around;
        border-bottom-left-radius: 32px;
        border-bottom-right-radius: 32px;
    }}
    .sticky-booking-banner {{
        background: linear-gradient(90deg, #10b981, #06b6d4); color: white; padding: 12px;
        text-align: center; font-weight: bold; font-size: 16px;
        border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(6,182,212,0.3);
    }}
    .dashboard-container {{
        background-color: #f1f5f9; border-radius: 12px; padding: 20px; color: #1e293b; margin-bottom: 25px;
    }}
    .dashboard-header {{
        color: #1e3a8a; font-weight: 700; margin: 0 0 15px 0; font-size: 1.25rem; border-bottom: 2px solid #cbd5e1; padding-bottom: 5px;
    }}
    .calc-box {{
        background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #0284c7;
    }}
    .tracker-card {{
        background: white; padding: 15px; border-radius: 10px; border: 1px solid #cbd5e1; margin-bottom: 15px;
    }}
    .status-node-active {{ color: #10b981; font-weight: bold; }}
    .status-node-pending {{ color: #94a3b8; }}
    .footer {{ text-align: center; color: #94a3b8; padding: 40px 0; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); }}
    
    /* Tap Service Card Design Structure */
    .service-tap-box {
        background-color: white;
        border-radius: 14px;
        overflow: hidden;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        margin-bottom: 15px;
    }
    .service-tap-box:hover {
        border-color: #0284c7;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(2,132,199,0.2);
    }
    .service-tap-box-selected {
        background-color: #f0f9ff;
        border-color: #0284c7;
        box-shadow: 0 0 0 3px rgba(2,132,199,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. PERSISTENT SYSTEM SIDEBAR INTERFACE
# ==============================================================================
st.sidebar.title("🧺 BIGZ CLEANERS")

if st.session_state.logged_in:
    active_email = st.session_state.current_email
    user_record = st.session_state.users.get(active_email)
    if not user_record:
        st.session_state.logged_in = False
        st.rerun()
        
    active_role = st.session_state.current_role
    initial_letter = user_record['name'][0] if user_record.get('name') else 'U'
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 15px 0; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 20px;">
        <div style="width: 70px; height: 70px; background: #3b82f6; border-radius: 50%; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white;">
            {initial_letter}
        </div>
        <h4 style="color: white; margin: 0;">{user_record['name']}</h4>
        <p style="color: #cbd5e1; font-size: 12px; margin: 2px 0 0 0;">{active_role.upper()} CORE ACCESS</p>
    </div>
    """, unsafe_allow_html=True)

    if active_role == "customer":
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Client Dashboard Hub", "💬 Messages Support Desk"])
    else:
        menu_selection = st.sidebar.radio("Administrative Sub-Views", ["Dashboard View", "Live Ledger Matrix Database"])

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Log Out of Session", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_email = ""
        st.session_state.current_role = ""
        st.session_state.security_mfa_passed = False
        st.rerun()

# ==============================================================================
# 6. PUBLIC LANDING ARCHITECTURE WITH LOGO ANIMATION & MFA CHALLENGE
# ==============================================================================
if not st.session_state.logged_in:
    hero_column, authorization_portal_column = st.columns([1.1, 0.9], gap="large")
    
    with hero_column:
        st.markdown("""
        <div class="animated-logo-container">
            <div class="animated-logo-icon">🧺</div>
            <div class="animated-logo-text">BIGZ CLEANERS</div>
            <div class="animated-logo-tagline">AI-Optimized Laundromat Core</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="padding: 10px 0; text-align: center;">
            <h2 style="color: white; font-size: 32px; font-weight: 800; line-height: 1.2; margin-bottom: 15px;">
                INTELLIGENT FABRIC CARE,<br>PROTECTED BY AI.
            </h2>
            <p style="color: #cbd5e1; font-size: 16px; margin-bottom: 35px;">
                One-tap scheduling matching advanced image verification models and chemical tailoring rules.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with authorization_portal_column:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h3 style='color: white; font-weight: 700;'>SECURE IDENTITY PORTAL</h3></div>", unsafe_allow_html=True)
        
        if st.session_state.pending_verification:
            st.markdown(f"""
            <div style="background: #fffbeb; border-left: 5px solid #d97706; padding: 20px; border-radius: 12px; color: #92400e; margin-bottom: 20px;">
                <h4 style="margin: 0 0 6px 0; font-weight: 700;">🔐 Cryptographic Verification Required</h4>
                <p style="font-size: 14px; margin: 0;">An access token pass was generated for: <b>{st.session_state.pending_verification}</b></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Simulate Multi-Factor Verification Confirm", use_container_width=True):
                target_email = st.session_state.pending_verification.lower().strip()
                if target_email in st.session_state.users:
                    st.session_state.users[target_email]["verified"] = True
                    save_user_profile(target_email, st.session_state.users[target_email])
                st.session_state.pending_verification = None
                st.rerun()
        else:
            login_tab, signup_tab = st.tabs(["[ SECURE LOGIN ]", "[ CREATE ACCOUNT ]"])
            with login_tab:
                input_email = st.text_input("Email Account Address", key="login_email_raw", placeholder="name@domain.com")
                input_password = st.text_input("Secure Account Password", type="password", key="login_pass_raw", placeholder="••••••••")
                
                if st.button("AUTHENTICATE ACCOUNT", use_container_width=True, type="primary"):
                    clean_login_email = input_email.lower().strip()
                    if clean_login_email in st.session_state.users and st.session_state.users[clean_login_email]["password"] == input_password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = st.session_state.users[clean_login_email]["name"]
                        st.session_state.current_email = clean_login_email
                        st.session_state.current_role = st.session_state.users[clean_login_email]["role"]
                        st.rerun()
                    else:
                        st.error("Invalid secure matching credentials.")
                            
            with signup_tab:
                with st.form("signup_panel_form"):
                    signup_name = st.text_input("Full Signature Name")
                    signup_phone = st.text_input("Phone Communication Line")
                    signup_email_raw = st.text_input("Email Account Address")
                    signup_address = st.text_input("Primary Physical Delivery Location")
                    signup_password = st.text_input("Set Custom Access Password", type="password")
                    if st.form_submit_button("GENERATE PLATFORM KEY"):
                        clean_email = signup_email_raw.lower().strip()
                        new_profile = {
                            "name": signup_name, "phone": signup_phone, "address": signup_address,
                            "password": signup_password, "role": "customer", "verified": False,
                            "wallet_points": 0, "saved_cards": ["•••• •••• •••• 1111"],
                            "subscription": "None", "subscription_status": "Inactive",
                            "preferences": {"Detergent": "Scented Organic Premium", "Water Temp": "Cold Wash Mode", "Folding Style": "Classic Shelf Fold", "Starch Level": "No Starch Treatment"}
                        }
                        save_user_profile(clean_email, new_profile)
                        st.session_state.pending_verification = clean_email
                        st.rerun()

# ==============================================================================
# 7. CLIENT DASHBOARD (TAP SELECTION, IMAGES, DET_SUITE, & RECOMMENDATION SYSTEM)
# ==============================================================================
elif st.session_state.logged_in and active_role == "customer":
    st.markdown("""<div class="sticky-booking-banner">🤖 AI Core Connected: Machine Learning predictive dispatch configurations are active.</div>""", unsafe_allow_html=True)

    if menu_selection == "Client Dashboard Hub":
        head_col, wall_col = st.columns([2, 1])
        with head_col:
            st.markdown(f"<h1 style='color: white; margin-bottom: 0;'>Welcome back, {user_record['name']}! 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #cbd5e1; margin-top: 5px;'>Tap to pick an active service layer, alter washing mixtures, and commit changes.</p>", unsafe_allow_html=True)
        with wall_col:
            user_points = user_record.get("wallet_points", 0)
            cash_credit = (user_points / 250) * 10
            st.markdown(f"""<div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px; border-radius: 10px;"><small style="text-transform: uppercase; font-weight: bold; opacity: 0.85;">⭐ LOYALTY INTEGRITY</small><h3 style="margin: 4px 0; font-weight: 800;">{user_points} Points</h3><small>Value: <b>${cash_credit:,.2f} Account Credit</b></small></div>""", unsafe_allow_html=True)

        layout_left_column, layout_right_column = st.columns([1.8, 1.2], gap="medium")

        with layout_left_column:
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🧺 Tap-To-Select Service Catalog</h3></div>', unsafe_allow_html=True)
            
            # Interactive visual service list mapping
            tap_cols = st.columns(3)
            for idx, srv in enumerate(st.session_state.laundry_service_catalog):
                with tap_cols[idx]:
                    is_selected = st.session_state.selected_service_id == srv["id"]
                    selected_css = "service-tap-box-selected" if is_selected else ""
                    
                    st.markdown(f"""
                    <div class="service-tap-box {selected_css}">
                        <img src="{srv['img']}" style="width:100%; height:140px; object-fit:cover; border-bottom:1px solid #e2e8f0;" />
                        <div style="padding:12px;">
                            <h4 style="margin:0; color:#1e3a8a; font-weight:bold;">{srv['name']}</h4>
                            <p style="margin:4px 0; font-size:12px; color:#64748b; height:40px; overflow:hidden;">{srv['desc']}</p>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                                <span style="font-weight:bold; color:#0284c7; font-size:14px;">KES {srv['price']}</span>
                                <span style="font-size:11px; background:#e2e8f0; padding:2px 6px; border-radius:4px; color:#475569;">{srv['unit']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Select {srv['name']}", key=f"btn_tap_{srv['id']}", use_container_width=True):
                        st.session_state.selected_service_id = srv["id"]
                        st.rerun()

            # Active target context configuration tracker
            active_tapped_service = next((s for s in st.session_state.laundry_service_catalog if s["id"] == st.session_state.selected_service_id), st.session_state.laundry_service_catalog[0])
            st.info(f"👉 Selected Active Tier: **{active_tapped_service['name']}** at **KES {active_tapped_service['price']} per {active_tapped_service['unit']}**")

            # --- ADVANCED INTEL ENGINE SUB-PANEL ---
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🤖 Predictive Cycle Analyzer</h3></div>', unsafe_allow_html=True)
            ai_c1, ai_c2 = st.columns(2)
            with ai_c1:
                fabric_profile = st.selectbox("Primary Fabric Structural Profile", ["Mixed Daily Wear Cotton", "Heavy Wool & Weighted Linens", "Delicate Silks / High-End Synthetics", "Soiled Athletic Technical Wear"])
                stain_density = st.slider("Stain Concentration Ratio Index", 0, 100, 25)
            with ai_c2:
                weather_forecast = st.selectbox("Current Meteorological Environment", ["Sunny (High Solar UV Index)", "Overcast / Cold Humidity", "Heavy Rain (Requires Full Mechanical Heat Extraction)"])
            
            # Automated calculation run
            recommended_temp = "Cold Wash Optimization" if fabric_profile.startswith("Delicate") else ("Warm Bio-Enzyme" if stain_density < 60 else "Sanitizing Extreme Heat")
            recommended_extraction = "High Velocity Turbo Spin" if weather_forecast.startswith("Heavy Rain") else "Balanced Eco-Spin"
            st.success(f"💡 **AI Recommendation Matrix Result:** Set to **{recommended_temp}** matched with a **{recommended_extraction}** track layout.")

            # --- DISPATCH FORM ---
            with st.form("one_click_scheduling_form"):
                st.markdown("##### 📅 Finalize Dispatch Options")
                
                # Multi-tier chemical select options
                detergent_selection = st.selectbox("Select Target Detergent Formula Matrix", [
                    "Standard Clean Formula (Pro-Care Surfactants)",
                    "Hypoallergenic Pure-Soft (Zero Scent, Sensitive Skin Verified)",
                    "Organic Eco-Enzyme Blend (Botanical Oils & Natural Cleaners)",
                    "Max-Stain Professional Armor (Heavy Solvent Boosters for Deep Grime)"
                ])
                
                bag_toggle = st.radio("Bag Size Selector Profile", ["Small Bag Bundle", "Medium Bag Bundle", "Large Bag Bundle"], index=1, horizontal=True)
                input_address = st.text_input("Enter Delivery Address (Google Maps Verified)", value=user_record.get("address", ""))
                
                l_col1, l_col2 = st.columns(2)
                pickup_date = l_col1.date_input("Target Route Pickup Date")
                pickup_time = l_col2.time_input("Preferred Time Window Picker", datetime.now().time())
                payment_route = st.selectbox("Select Secure Financial Gateway", ["M-Pesa Mobile Billing Interface", "Secure Tokenized Credit Card Engine"])
                
                if st.form_submit_button("⚡ Finalize Order Dispatch Schedule"):
                    generated_id = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    resolved_gateway = "M-Pesa (Submitted)" if "M-Pesa" in payment_route else "Secure Card (Confirmed)"
                    
                    new_booking_item = {
                        "tracking": generated_id, "customer": user_record["name"], "email": active_email,
                        "service": active_tapped_service["name"], "quantity": "1 Unit Batch", "bag_size": bag_toggle,
                        "detergent": detergent_selection, "cost": float(active_tapped_service["price"]),
                        "pickup_logistics": f"{pickup_date} at {pickup_time}", "address": input_address,
                        "payment_gateway": resolved_gateway, "status": "Received",
                        "assigned_staff": "Pending Allocation Hub", "created_at": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.orders.append(new_booking_item)
                    user_record["wallet_points"] = user_record.get("wallet_points", 0) + 30
                    save_user_profile(active_email, user_record)
                    st.success(f"Order processed! Tracking Number: {generated_id}")
                    st.rerun()

        with layout_right_column:
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">📍 Live Order Tracking</h3></div>', unsafe_allow_html=True)
            client_orders = [o for o in st.session_state.orders if o["email"] == active_email]
            active_tracking_pool = [o for o in client_orders if o["status"] != "Delivered & Complete"]
            
            if not active_tracking_pool:
                st.caption("No running operations tracked inside the tracking arrays.")
            else:
                for active_order in active_tracking_pool:
                    st.markdown(f"**Order Token Context: #{active_order['tracking']}**")
                    stages = ["Received", "Washing", "Drying", "Ironing", "Out for Delivery"]
                    current_status = active_order["status"]
                    status_idx = stages.index(current_status) if current_status in stages else 0
                    
                    nodes_output = [f"<span class='status-node-active'>[{stage_label}]</span>" if index == status_idx else f"<span class='status-node-pending'>{stage_label}</span>" for index, stage_label in enumerate(stages)]
                    st.markdown(f"<div class='tracker-card'>{' ➔ '.join(nodes_output)}</div>", unsafe_allow_html=True)
                    st.markdown("---")

            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🛠️ Premium Personalization Panel</h3></div>', unsafe_allow_html=True)
            with st.form("preferences_saving_form"):
                perf_temp = st.selectbox("Water Temperature Settings", ["Cold Wash Mode", "Warm Eco Treatment", "Sanitizing Hot Cycle"])
                perf_fold = st.selectbox("Folding Structural Style", ["Classic Shelf Fold", "Rolled Compact Packing", "Hanger Deployment Request"])
                perf_starch = st.selectbox("Starch Levels Treatment", ["No Starch Treatment", "Medium Crispy Stiffness", "Maximum Crisp Armor"])
                if st.form_submit_button("Save Permanent Wash Preferences"):
                    user_record["preferences"] = {"Detergent": "Saved Matrix Profile", "Water Temp": perf_temp, "Folding Style": perf_fold, "Starch Level": perf_starch}
                    save_user_profile(active_email, user_record)
                    st.success("Preferences updated.")
                    st.rerun()

    elif menu_selection == "💬 Messages Support Desk":
        st.title("💬 Helpdesk Communications")
        chat_input_column, chat_history_column = st.columns([1, 2], gap="medium")
        with chat_input_column:
            composed_text = st.text_area("Write your message to Admin:", placeholder="Type here...")
            if st.button("✉️ Transmit Message", use_container_width=True):
                if composed_text:
                    st.session_state.messages.append({"sender": active_email, "recipient": "admin@bigz.com", "sender_name": f"{user_record['name']} (Client)", "message": composed_text, "time": datetime.now().strftime("%H:%M:%S")})
                    st.success("Message dispatched securely.")
                    st.rerun()
        with chat_history_column:
            customer_thread = [m for m in st.session_state.messages if m["sender"] == active_email or m["recipient"] == active_email]
            for msg in reversed(customer_thread):
                st.info(f"👤 **{msg['sender_name']}** [{msg['time']}]: {msg['message']}")

# ==============================================================================
# 8. MASTER ADMINISTRATIVE HUB VIEW (WITH LIVE REVENUE & PIPELINE GRAPHS)
# ==============================================================================
elif st.session_state.logged_in and active_role == "admin":
    
    if menu_selection == "Dashboard View":
        
        # Upper Split Layout: Mobile Mock-up Frame vs Live High-Fidelity Graphs
        mobile_panel_col, statistics_analyzer_col = st.columns([1.1, 1.9], gap="large")
        
        with mobile_panel_col:
            st.markdown('<div class="mobile-frame">', unsafe_allow_html=True)
            
            # --- HEADER BLOCK ---
            st.markdown(f"""
            <div class="mobile-header">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h1 style="color: white; font-size: 24px; font-weight: bold; margin: 0; line-height: 1.2;">Bigz Cleaners</h1>
                        <p style="color: rgba(255,255,255,0.9); font-size: 14px; margin: 4px 0 0 0;">Admin Dashboard</p>
                    </div>
                    <div class="admin-avatar">A</div>
                </div>
                <div class="revenue-box">
                    <p style="margin: 0; font-size: 14px; opacity: 0.9; color: white;">Today's Revenue</p>
                    <h2 style="margin: 4px 0 0 0; color: white; font-size: 28px; font-weight: 800;">KES 17,500</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- STATS GRID ---
            st.markdown("<div style='padding: 16px;'>", unsafe_allow_html=True)
            st_col1, st_col2 = st.columns(2)
            with st_col1:
                st.markdown("""<div class="stat-card"><p style="font-size: 12px; color: #64748b; margin:0;">Orders Today</p><h3 style="font-size: 20px; font-weight: bold; margin: 4px 0 0 0;">48</h3></div>""", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""<div class="stat-card"><p style="font-size: 12px; color: #64748b; margin:0;">Pending</p><h3 style="font-size: 20px; font-weight: bold; margin: 4px 0 0 0;">12</h3></div>""", unsafe_allow_html=True)
            with st_col2:
                st.markdown("""<div class="stat-card"><p style="font-size: 12px; color: #64748b; margin:0;">Revenue</p><h3 style="font-size: 20px; font-weight: bold; margin: 4px 0 0 0;">KES 17,500</h3></div>""", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""<div class="stat-card"><p style="font-size: 12px; color: #64748b; margin:0;">Deliveries</p><h3 style="font-size: 20px; font-weight: bold; margin: 4px 0 0 0;">9</h3></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # --- QUICK ACTIONS GRID ---
            st.markdown("<div style='padding: 0 16px;'><h2 style='font-size: 18px; font-weight: bold; margin: 10px 0;'>Quick Actions</h2></div>", unsafe_allow_html=True)
            act_col1, act_col2, act_col3 = st.columns(3)
            with act_col1:
                if st.button("Orders", key="act_orders", use_container_width=True): st.info("Displaying running order sequences.")
                if st.button("Payments", key="act_pay", use_container_width=True): st.info("Payment gateways verified.")
            with act_col2:
                if st.button("Pickup", key="act_pick", use_container_width=True): st.info("Pickup schedules mapped.")
                if st.button("Staff", key="act_staff", use_container_width=True): st.info("Staff activity logs active.")
            with act_col3:
                if st.button("Delivery", key="act_deliv", use_container_width=True): st.info("Delivery dispatch routes live.")
                if st.button("Reports", key="act_rep", use_container_width=True): st.info("Generating system data analytics.")
                
            # --- RECENT ORDERS ---
            st.markdown("<div style='padding: 16px;'><div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'><h2 style='font-size: 18px; font-weight: bold; margin:0;'>Recent Orders</h2></div>", unsafe_allow_html=True)
            for r_order in st.session_state.recent_orders:
                st.markdown(f"""
                <div class="data-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; font-weight: bold; font-size: 16px;">{r_order['id']}</h3>
                            <p style="margin: 2px 0 0 0; size: 14px; color: #64748b;">{r_order['customer']}</p>
                        </div>
                        <span class="status-badge-blue">{r_order['status']}</span>
                    </div>
                    <p style="margin: 8px 0 0 0; font-size: 14px; color: #475569;">{r_order['service']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- STAFF ACTIVITY ---
            st.markdown("<div style='padding: 0 16px;'><h2 style='font-size: 18px; font-weight: bold; margin-bottom:10px;'>Staff Activity</h2></div>", unsafe_allow_html=True)
            for person in st.session_state.staff_activity:
                status_indicator_dot = "🟢 Active" if person["active"] else "🔴 Offline"
                st.markdown(f"""
                <div class="data-card" style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; font-weight: bold; font-size: 15px;">{person['name']}</h3>
                        <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">{person['role']}</p>
                    </div>
                    <span style="font-size: 13px; font-weight: 500;">{status_indicator_dot}</span>
                </div>
                """, unsafe_allow_html=True)

            # --- RIDER TRACKING ---
            st.markdown("<div style='padding: 16px;'><h2 style='font-size: 18px; font-weight: bold; margin-bottom:10px;'>Delivery Riders</h2></div>", unsafe_allow_html=True)
            for rider in st.session_state.delivery_riders:
                st.markdown(f"""
                <div class="data-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; font-weight: bold; font-size: 15px;">{rider['name']}</h3>
                            <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">📍 {rider['location']}</p>
                        </div>
                        <span class="status-badge-green">{rider['status']}</span>
                    </div>
                    <p style="margin: 6px 0 0 0; font-size: 13px; color: #475569;">Active Orders Assigned: <b>{rider['orders']}</b></p>
                </div>
                """, unsafe_allow_html=True)

            # --- NOTIFICATIONS ---
            st.markdown("<div style='padding: 0 16px;'><h2 style='font-size: 18px; font-weight: bold; margin-bottom:10px;'>Notifications</h2></div>", unsafe_allow_html=True)
            for note in st.session_state.notifications:
                st.markdown(f'<div class="notification-orange">🔔 {note}</div>', unsafe_allow_html=True)

            # --- CURRENT BASE PRICE REFERENCE MATRIX ---
            st.markdown("<div style='padding: 16px;'><h2 style='font-size: 18px; font-weight: bold; margin-bottom:10px;'>Active Service Pricing</h2></div>", unsafe_allow_html=True)
            for srv in st.session_state.laundry_service_catalog:
                st.markdown(f"""
                <div class="data-card" style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; font-weight: bold; font-size: 15px;">{srv['name']}</h3>
                        <p style="margin: 2px 0 0 0; font-size: 12px; color: #64748b;">Active Value Mapping</p>
                    </div>
                    <span style="font-weight: 700; color: #1d4ed8; font-size: 15px;">KES {srv['price']} / {srv['unit']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="bottom-nav">
                <span style="color: #2563eb; font-weight: bold; font-size: 14px;">🏠 Home</span>
                <span style="color: #64748b; font-size: 14px;">📦 Orders</span>
                <span style="color: #64748b; font-size: 14px;">📍 Tracking</span>
                <span style="color: #64748b; font-size: 14px;">👤 Profile</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with statistics_analyzer_col:
            st.markdown("""<div style="background-color:rgba(255,255,255,0.08); padding:24px; border-radius:24px; border:1px solid rgba(255,255,255,0.1);">
                <h2 style="color:white; margin:0 0 5px 0;">📈 High-Fidelity Statistical Analyser</h2>
                <p style="color:#94a3b8; font-size:14px; margin-bottom:20px;">Real-time execution analytics drawn from the core operations ledger database matrix.</p>
            </div>""", unsafe_allow_html=True)
            
            # Parsing current order arrays into DataFrame structures for visualization
            df_orders = pd.DataFrame(st.session_state.orders)
            
            # --- CHART REGION 1: PIPELINE LOAD FLOW GRAPH ---
            st.markdown("<h4 style='color:white; margin-top:20px;'>📊 Pipeline Load Level Distribution</h4>", unsafe_allow_html=True)
            status_distribution = df_orders['status'].value_counts().reset_index()
            status_distribution.columns = ['Status Node', 'Active Batch Count']
            st.bar_chart(status_distribution, x='Status Node', y='Active Batch Count', use_container_width=True)
            
            # --- CHART REGION 2: COMPOSITE FINANCIAL BREAKDOWN REVENUE PIE ---
            an_col1, an_col2 = st.columns(2)
            
            with an_col1:
                st.markdown("<h4 style='color:white; text-align:center;'>🥧 Revenue Stream Share</h4>", unsafe_allow_html=True)
                revenue_share = df_orders.groupby('service')['cost'].sum().reset_index()
                revenue_share.columns = ['Service Catalog Model', 'Accrued Revenue Gross (KES)']
                st.pie_chart(revenue_share, values='Accrued Revenue Gross (KES)', names='Service Catalog Model', use_container_width=True)
                
            with an_col2:
                st.markdown("<h4 style='color:white; text-align:center;'>🏍️ Rider Dispatch Allocation</h4>", unsafe_allow_html=True)
                rider_workload = df_orders['assigned_staff'].value_counts().reset_index()
                rider_workload.columns = ['Rider Identity Tag', 'Assigned Deliveries']
                st.pie_chart(rider_workload, values='Assigned Deliveries', names='Rider Identity Tag', use_container_width=True)
                
            # --- CHART REGION 3: DETEGERENT DEMAND DISTRIBUTION MATRIX ---
            st.markdown("<h4 style='color:white; margin-top:10px;'>🧪 Detergent Selection Volume Trends</h4>", unsafe_allow_html=True)
            detergent_trends = df_orders['detergent'].value_counts().reset_index()
            detergent_trends.columns = ['Detergent Matrix Variant', 'Selections Count']
            st.bar_chart(detergent_trends, x='Detergent Matrix Variant', y='Selections Count', use_container_width=True)

    elif menu_selection == "Live Ledger Matrix Database":
        st.markdown("## 📊 Operational Pipeline Database Engine")
        
        # --- DYNAMIC PRICING CONTROL PANELS ---
        st.markdown("### 💰 Corporate Revenue & Pricing Matrix Adjustment Panel")
        st.caption("Alter values below to adjust client catalog costs in real time across all storefront interfaces.")
        
        with st.form("admin_pricing_control_form"):
            p_cols = st.columns(3)
            temp_prices = {}
            for idx, srv in enumerate(st.session_state.laundry_service_catalog):
                with p_cols[idx]:
                    temp_prices[srv["id"]] = st.slider(f"Base Fee: {srv['name']} (per {srv['unit']})", min_value=10, max_value=2000, value=int(srv["price"]), step=5)
            
            if st.form_submit_button("🔒 Save & Deploy New Rates"):
                for srv in st.session_state.laundry_service_catalog:
                    srv["price"] = float(temp_prices[srv["id"]])
                st.success("New pricing catalog rates synchronized successfully across databases.")
                st.rerun()

        st.markdown("---")
        
        # --- EXCLUSIVE ADMIN PROMOTION PANEL ---
        st.markdown("### 🔑 Administrator Role Delegation Panel")
        st.caption("Elevate user privileges directly to internal operations administrative access tiers.")
        
        customer_accounts = [email for email, profile in st.session_state.users.items() if profile["role"] == "customer"]
        
        if not customer_accounts:
            st.info("No registered customer profiles are currently available for role elevation workflows.")
        else:
            col_target, col_action = st.columns([2, 1])
            with col_target:
                selected_user_email = st.selectbox("Select Account for Escalation", options=customer_accounts, format_func=lambda e: f"{st.session_state.users[e]['name']} ({e})")
            with col_action:
                st.markdown("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
                if st.button("🚀 Grant Administrative Clearance", use_container_width=True):
                    st.session_state.users[selected_user_email]["role"] = "admin"
                    st.session_state.users[selected_user_email]["verified"] = True
                    save_user_profile(selected_user_email, st.session_state.users[selected_user_email])
                    st.success(f"Security clearance confirmed: {selected_user_email} is now an Admin.")
                    st.rerun()
                    
        st.markdown("---")
        
        # --- ORDER WORKFLOW CONTROL LEDGER ---
        if st.session_state.orders:
            matrix_ledger = [
                {"Order Unique Token": entry["tracking"], "Client": entry["customer"], "Service Model": entry["service"], "Billing Status": entry["payment_gateway"], "Workflow Stage": entry["status"], "Rider Assigned": entry["assigned_staff"], "Index": index}
                for index, entry in enumerate(st.session_state.orders)
            ]
            st.dataframe(pd.DataFrame(matrix_ledger).drop(columns=["Index"]), use_container_width=True, hide_index=True)
            
            st.markdown("### ⚙️ Live Stage Modification Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                target_idx = st.selectbox("Select Target Order Matrix Index", options=range(len(st.session_state.orders)), format_func=lambda x: f"Order #{st.session_state.orders[x]['tracking']}")
            with col2:
                next_stage = st.selectbox("Update Pipeline Status Node", ["Received", "Washing", "Drying", "Ironing", "Out for Delivery", "Delivered & Complete"])
            with col3:
                next_rider = st.selectbox("Re-assign Field Delivery Rider", ["David", "Kelvin", "John", "Unassigned Pool"])
                
            if st.button("Commit Overrides to Persistent Storage Engine", use_container_width=True):
                st.session_state.orders[target_idx]["status"] = next_stage
                st.session_state.orders[target_idx]["assigned_staff"] = next_rider
                st.success("Database records synchronized perfectly.")
                st.rerun()

# ==============================================================================
# 9. FOOTER BASE
# ==============================================================================
st.markdown("""
<div class="footer">
    🧺 BIGZ CLEANERS AI <br>
    System Compliant Blueprint Core — Secure Operational Layer Terminal Platform <br><br>
    © 2026 BIGZ CLEANERS
</div>
""", unsafe_allow_html=True)
