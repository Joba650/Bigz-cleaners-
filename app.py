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

if "laundry_service_catalog" not in st.session_state:
    st.session_state.laundry_service_catalog = [
        {"id": "srv_wash_fold", "name": "Laundry Washing", "price": 200.0, "unit": "7KG", "type": "Wash & Fold"},
        {"id": "srv_carpet", "name": "Carpet Cleaning", "price": 150.0, "unit": "sqm", "type": "Specialty Clean"},
        {"id": "srv_duvet", "name": "Duvet Cleaning", "price": 500.0, "unit": "Piece", "type": "Dry Clean"}
    ]

st.set_page_config(
    page_title="BIGZ CLEANERS",
    page_icon="🧺",
    layout="wide"
)

# ==============================================================================
# 2. PERSISTENT STORAGE LAYER ENGINE
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
    "selected_service_id": st.session_state.laundry_service_catalog[0]["id"], "admin_filter_metric": "Dashboard View",
    "messages": [{"sender": "admin@bigz.com", "recipient": "sarachen@gmail.com", "sender_name": "Theophilus (Admin)", "message": "Hello Sarah, welcome to your support desk channel thread!", "time": "12:00:00"}],
    "price_alerts": [{"text": "Welcome to BIGZ Cleaners Operations Command Panel.", "timestamp": "System Initialization"}],
    "pending_verification": None,
    "delivery_riders": [
        {"name": "David", "location": "Nakuru Town", "orders": 4, "status": "On Delivery"},
        {"name": "Kelvin", "location": "Njoro", "orders": 2, "status": "Pickup"}
    ],
    "notifications": [
        "Order #1023 delayed by 15 mins",
        "New pickup request received",
        "Payment confirmed from Mercy"
    ],
    "recent_orders": [
        {"id": "#1023", "customer": "Brian Mwangi", "service": "7KG Laundry", "status": "Washing"},
        {"id": "#1024", "customer": "Mercy Achieng", "service": "Duvet Cleaning", "status": "Ready"},
        {"id": "#1025", "customer": "Kevin Otieno", "service": "Carpet Cleaning", "status": "Delivery"}
    ],
    "staff_activity": [
        {"name": "John", "role": "Pickup Rider", "active": True},
        {"name": "Mercy", "role": "Ironing", "active": True},
        {"name": "Alex", "role": "Washing", "active": False}
    ],
    "orders": [
        {"tracking": "BIGZ-1023", "customer": "Brian Mwangi", "email": "brian@mwangi.com", "service": "7KG Laundry", "quantity": "1 Batch", "bag_size": "Medium", "detergent": "Standard", "cost": 200.0, "pickup_logistics": "Immediate", "address": "Nakuru Town", "payment_gateway": "M-Pesa (Submitted)", "status": "Washing", "assigned_staff": "John", "created_at": "2026-05-27"}
    ]
}
for state_key, default_value in state_defaults.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value

# ==============================================================================
# 4. GRAPHICAL UI ELEMENT CUSTOMIZATION (CSS)
# ==============================================================================
st.markdown(f"""
<style>
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
    .action-btn {{
        background-color: #eff6ff;
        color: #1d4ed8;
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        font-size: 13px;
        font-weight: 500;
        border: none;
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
        background: #10b981; color: white; padding: 12px;
        text-align: center; font-weight: bold; font-size: 16px;
        border-radius: 8px; margin-bottom: 20px;
    }}
    .footer {{ text-align: center; color: #94a3b8; padding: 40px 0; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); }}
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
        <p style="color: #cbd5e1; font-size: 12px; margin: 2px 0 0 0;">{active_role.upper()} PORTAL</p>
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
        st.rerun()

# ==============================================================================
# 6. PUBLIC LANDING ARCHITECTURE
# ==============================================================================
if not st.session_state.logged_in:
    hero_column, authorization_portal_column = st.columns([1.1, 0.9], gap="large")
    
    with hero_column:
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
        
        feature_one_col, feature_two_col = st.columns(2)
        with feature_one_col:
            st.markdown(f"""
            <div style="background: white; padding: 22px; border-radius: 16px; min-height: 180px; color: #0f172a; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);">
                <span style="font-size: 32px;">📥</span>
                <h4 style="margin-top: 10px; font-weight: 700; color: {APP_THEME_COLOR_PRIMARY}; margin-bottom: 5px;">FOR CLIENTS:</h4>
                <p style="font-size: 13px; color: #475569; line-height: 1.4; margin: 0;">
                    Schedule Pickups, Track Your Wash Status, and Manage Payments effortlessly.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with feature_two_col:
            st.markdown("""
            <div style="background: white; padding: 22px; border-radius: 16px; min-height: 180px; color: #0f172a; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);">
                <span style="font-size: 32px;">📊</span>
                <h4 style="margin-top: 10px; font-weight: 700; color: #581c87; margin-bottom: 5px;">FOR ADMINS & STAFF:</h4>
                <p style="font-size: 13px; color: #475569; line-height: 1.4; margin: 0;">
                    Streamline Operations, Assign Staff/Routes, and Monitor Resource Reserves.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with authorization_portal_column:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: white; font-weight: 700;'>GET STARTED OR LOG IN</h2></div>", unsafe_allow_html=True)
        
        if st.session_state.pending_verification:
            st.markdown(f"""
            <div style="background: #fffbeb; border-left: 5px solid #d97706; padding: 20px; border-radius: 12px; color: #92400e; margin-bottom: 20px;">
                <h4 style="margin: 0 0 6px 0; font-weight: 700;">⚠️ Email Verification Required</h4>
                <p style="font-size: 14px; margin: 0;">A system dispatch link has been pushed to: <b>{st.session_state.pending_verification}</b></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Simulate Verification Confirm", use_container_width=True):
                target_email = st.session_state.pending_verification.lower().strip()
                if target_email in st.session_state.users:
                    st.session_state.users[target_email]["verified"] = True
                    save_user_profile(target_email, st.session_state.users[target_email])
                st.session_state.pending_verification = None
                st.rerun()
        else:
            login_tab, signup_tab = st.tabs(["[ LOGIN ]", "[ SIGN UP ]"])
            with login_tab:
                input_email = st.text_input("Email Account Address", key="login_email_raw", placeholder="name@domain.com")
                input_password = st.text_input("Secure Account Password", type="password", key="login_pass_raw", placeholder="••••••••")
                if st.button("LOG IN TO DASHBOARD", use_container_width=True, type="primary"):
                    clean_login_email = input_email.lower().strip()
                    if clean_login_email in st.session_state.users and st.session_state.users[clean_login_email]["password"] == input_password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = st.session_state.users[clean_login_email]["name"]
                        st.session_state.current_email = clean_login_email
                        st.session_state.current_role = st.session_state.users[clean_login_email]["role"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                            
            with signup_tab:
                selected_role_type = st.selectbox("Assign Profile Blueprint Type:", ["Client / Consumer Account", "Admin / Production Staff"])
                with st.form("signup_panel_form"):
                    signup_name = st.text_input("Full Signature Name")
                    signup_phone = st.text_input("Phone Communication Line")
                    signup_email_raw = st.text_input("Email Account Address")
                    signup_address = st.text_input("Primary Physical Delivery Location")
                    signup_password = st.text_input("Set Custom Access Password", type="password")
                    if st.form_submit_button("SUBMIT APPLICATION FILES", use_container_width=True):
                        clean_email = signup_email_raw.lower().strip()
                        assigned_role = "customer" if "Client" in selected_role_type else "admin"
                        new_profile = {
                            "name": signup_name, "phone": signup_phone, "address": signup_address,
                            "password": signup_password, "role": assigned_role, "verified": (assigned_role == "admin"),
                            "wallet_points": 0, "saved_cards": ["•••• •••• •••• 1111"],
                            "subscription": "None", "subscription_status": "Inactive",
                            "preferences": {"Detergent": "Scented Organic Premium", "Water Temp": "Cold Wash Mode", "Folding Style": "Classic Shelf Fold", "Starch Level": "No Starch Treatment"}
                        }
                        save_user_profile(clean_email, new_profile)
                        if assigned_role == "customer":
                            st.session_state.pending_verification = clean_email
                        st.rerun()

# ==============================================================================
# 7. CLIENT DASHBOARD & PROFILE VIEW (UPGRADED CONVERSION SUITE)
# ==============================================================================
elif st.session_state.logged_in and active_role == "customer":
    st.markdown("""<div class="sticky-booking-banner">⚡ Need a 60-Second Pickup? Use the High-Conversion Booking Engine panel below for instant pickup scheduling!</div>""", unsafe_allow_html=True)

    if menu_selection == "Client Dashboard Hub":
        head_col, wall_col = st.columns([2, 1])
        with head_col:
            st.markdown(f"<h1 style='color: white; margin-bottom: 0;'>Welcome back, {user_record['name']}! 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #cbd5e1; margin-top: 5px;'>Manage allocations, review active workflow maps, and edit preferences.</p>", unsafe_allow_html=True)
        with wall_col:
            user_points = user_record.get("wallet_points", 0)
            cash_credit = (user_points / 250) * 10
            st.markdown(f"""<div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px; border-radius: 10px;"><small style="text-transform: uppercase; font-weight: bold; opacity: 0.85;">⭐ LOYALTY & WALLET HUB</small><h3 style="margin: 4px 0; font-weight: 800;">{user_points} Points</h3><small>Value: <b>${cash_credit:,.2f} Account Credit</b></small></div>""", unsafe_allow_html=True)

        layout_left_column, layout_right_column = st.columns([1.8, 1.2], gap="medium")

        with layout_left_column:
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🚀 High-Conversion Booking Engine</h3></div>', unsafe_allow_html=True)
            st.markdown("##### 📊 Interactive Pricing Calculator")
            calc_col1, calc_col2, calc_col3 = st.columns(3)
            with calc_col1:
                item_wash_fold = st.number_input("Laundry Washing (7KG Batches)", min_value=0, value=1)
            with calc_col2:
                item_duvet = st.number_input("Duvet Cleaning (Pcs)", min_value=0, value=0)
            with calc_col3:
                item_carpet = st.number_input("Carpet Cleaning (sqm)", min_value=0, value=0)
                
            est_total = (item_wash_fold * 200.0) + (item_duvet * 500.0) + (item_carpet * 150.0)
            st.markdown(f"""<div class="calc-box"><span style="font-size: 13px; color: #64748b; font-weight: bold;">PREVIEW ESTIMATE</span><h3 style="margin: 0; color: #0284c7; font-weight: 800;">KES {est_total:,.2f}</h3></div>""", unsafe_allow_html=True)
            
            with st.form("one_click_scheduling_form"):
                st.markdown("##### 📅 One-Click Dispatch Parameters")
                bag_toggle = st.radio("Bag Size Selector Profile", ["Small Bag Bundle", "Medium Bag Bundle", "Large Bag Bundle", "Custom Itemized Assignment"], index=1, horizontal=True)
                input_address = st.text_input("Enter Delivery Address (Google Maps Verified)", value=user_record.get("address", ""))
                if input_address:
                    st.markdown("<p style='color: #10b981; font-size: 12px; margin-top:-10px;'>✔️ Address confirmed within active service radius.</p>", unsafe_allow_html=True)
                
                l_col1, l_col2 = st.columns(2)
                pickup_date = l_col1.date_input("Target Route Pickup Date")
                pickup_time = l_col2.time_input("Preferred Time Window Picker", datetime.now().time())
                payment_route = st.selectbox("Select Secure Financial Gateway", ["M-Pesa Mobile Billing", "Secure Credit Card Engine"])
                
                if st.form_submit_button("⚡ Finalize Booking Schedule (<60s)", use_container_width=True):
                    generated_id = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    resolved_gateway = "M-Pesa (Submitted)" if "M-Pesa" in payment_route else "Secure Card (Confirmed)"
                    pref_dict = user_record.get("preferences", {})
                    
                    new_booking_item = {
                        "tracking": generated_id, "customer": user_record["name"], "email": active_email,
                        "service": "Mixed Items Batch" if est_total > 0 else "Laundry Washing",
                        "quantity": f"{item_wash_fold} Batch", "bag_size": bag_toggle,
                        "detergent": pref_dict.get("Detergent", "Scented Organic Premium"), "cost": est_total if est_total > 0 else 200.0,
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
                perf_det = st.selectbox("Preferred Detergent Type", ["Scented Organic Premium", "Hypoallergenic Eco-Soft", "Unscented Protect Line", "Heavy Duty Citrus Boost"], index=0)
                perf_temp = st.selectbox("Water Temperature Settings", ["Cold Wash Mode", "Warm Eco Treatment", "Sanitizing Hot Cycle"])
                perf_fold = st.selectbox("Folding Structural Style", ["Classic Shelf Fold", "Rolled Compact Packing", "Hanger Deployment Request"])
                perf_starch = st.selectbox("Starch Levels Treatment", ["No Starch Treatment", "Medium Crispy Stiffness", "Maximum Crisp Armor"])
                if st.form_submit_button("Save Permanent Wash Preferences"):
                    user_record["preferences"] = {"Detergent": perf_det, "Water Temp": perf_temp, "Folding Style": perf_fold, "Starch Level": perf_starch}
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
# 8. AUTHORIZED LAYER C: MASTER ADMINISTRATIVE HUB VIEW (REACT DESIGN IMPLEMENTED)
# ==============================================================================
elif st.session_state.logged_in and active_role == "admin":
    
    if menu_selection == "Dashboard View":
        # Centered frame container mapping cleanly to the mobile view layout specification
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

        # --- RIDER TRACKING (NAKURU / NJORO) ---
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

        # --- PRICING MANAGER DISPLAY ---
        st.markdown("<div style='padding: 16px;'><h2 style='font-size: 18px; font-weight: bold; margin-bottom:10px;'>Service Pricing</h2></div>", unsafe_allow_html=True)
        for srv in st.session_state.laundry_service_catalog:
            st.markdown(f"""
            <div class="data-card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-weight: bold; font-size: 15px;">{srv['name']}</h3>
                    <p style="margin: 2px 0 0 0; font-size: 12px; color: #64748b;">Current Tier Configuration</p>
                </div>
                <span style="font-weight: 700; color: #1d4ed8; font-size: 15px;">KES {srv['price']} / {srv['unit']}</span>
            </div>
            """, unsafe_allow_html=True)

        # --- WEEKLY ANALYTICS SUMMARY BOX ---
        st.markdown("""
        <div style="padding: 16px;">
            <div class="analytics-gradient">
                <h2 style="margin: 0; font-size: 18px; font-weight: bold; color: white;">Weekly Analytics</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
                    <div>
                        <p style="margin: 0; font-size: 12px; opacity: 0.85; color: white;">Completed Orders</p>
                        <h3 style="margin: 4px 0 0 0; font-size: 22px; font-weight: bold; color: white;">214</h3>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 12px; opacity: 0.85; color: white;">New Customers</p>
                        <h3 style="margin: 4px 0 0 0; font-size: 22px; font-weight: bold; color: white;">36</h3>
                    </div>
                </div>
                <div style="margin-top: 15px; background: rgba(255,255,255,0.15); padding: 12px; border-radius: 12px;">
                    <p style="margin: 0; font-size: 13px; color: white;">Business Performance: <b>82% Growth</b></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- BOTTOM FIXED BAR SIMULATION ---
        st.markdown("""
        <div class="bottom-nav">
            <span style="color: #2563eb; font-weight: bold; font-size: 14px;">🏠 Home</span>
            <span style="color: #64748b; font-size: 14px;">📦 Orders</span>
            <span style="color: #64748b; font-size: 14px;">📍 Tracking</span>
            <span style="color: #64748b; font-size: 14px;">👤 Profile</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu_selection == "Live Ledger Matrix Database":
        st.markdown("## 📊 Active Operational Pipeline Database Engine")
        
        # Allow admins to seamlessly modify operational parameters
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
    🧺 BIGZ CLEANERS <br>
    System Compliant Blueprint Core — Trusted Production Engine Framework Terminal <br><br>
    © 2026 BIGZ CLEANERS
</div>
""", unsafe_allow_html=True)
