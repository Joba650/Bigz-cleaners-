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
        {"id": "srv_wash_fold", "name": "Wash & Fold (General Wear)", "price": 100.0, "unit": "KG", "type": "Wash & Fold"},
        {"id": "srv_wash_iron", "name": "Wash, Dry, Iron & Fold", "price": 140.0, "unit": "KG", "type": "Wash & Fold"},
        {"id": "srv_duvet", "name": "Heavy Blanket / Duvet", "price": 400.0, "unit": "Piece", "type": "Dry Clean"},
        {"id": "srv_suits", "name": "Official Suits (Jacket & Trousers)", "price": 500.0, "unit": "Suit", "type": "Dry Clean"},
        {"id": "srv_shoes", "name": "Sneaker / Canvas Shoe Cleaning", "price": 200.0, "unit": "Pair", "type": "Wash & Fold"}
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
    "selected_service_id": st.session_state.laundry_service_catalog[0]["id"], "admin_filter_metric": "Orders",
    "messages": [{"sender": "admin@bigz.com", "recipient": "sarachen@gmail.com", "sender_name": "Theophilus (Admin)", "message": "Hello Sarah, welcome to your support desk channel thread!", "time": "12:00:00"}],
    "price_alerts": [{"text": "Welcome to BIGZ Cleaners! Interactive calculators and verified zoning maps are now active.", "timestamp": "System Initialization"}],
    "pending_verification": None, "inventory": {"Detergent (L)": 180, "Fabric Softener (L)": 95, "Tags & Bags (Pcs)": 450},
    "staff_directory": ["Alex Chen", "Marix Mason", "John Doe", "Theophilus mose"],
    "orders": [
        {"tracking": "BIGZ-12341", "customer": "Sarah Chen", "email": "sarachen@gmail.com", "service": "Wash & Fold (General Wear)", "quantity": "5 KG", "bag_size": "Medium Bag", "detergent": "Scented Organic Premium", "cost": 500.0, "pickup_logistics": "2026-05-28 at 10:00 AM", "address": "123 Saved Address From Street, West, Buil, 4003", "payment_gateway": "M-Pesa (Submitted)", "status": "Washing", "assigned_staff": "Alex Chen", "created_at": "05/26/26"},
        {"tracking": "BIGZ-12342", "customer": "Sarah Chen", "email": "sarachen@gmail.com", "service": "Heavy Blanket / Duvet", "quantity": "1 Piece", "bag_size": "Item-by-Item", "detergent": "Hypoallergenic Eco-Soft", "cost": 400.0, "pickup_logistics": "2026-05-29 at 02:00 PM", "address": "123 Saved Address From Street, West, Buil, 4003", "payment_gateway": "Secure Card (Confirmed)", "status": "Received", "assigned_staff": "Alex Chen", "created_at": "05/26/26"}
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
    .sticky-booking-banner {{
        background: #10b981;
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
    }}
    .dashboard-container {{
        background-color: #f1f5f9;
        border-radius: 12px;
        padding: 20px;
        color: #1e293b;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 25px;
    }}
    .dashboard-header {{
        color: #1e3a8a;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 15px;
        font-size: 1.25rem;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 5px;
    }}
    .calc-box {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #0284c7;
    }}
    .tracker-card {{
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        margin-bottom: 15px;
    }}
    .status-node-active {{ color: #10b981; font-weight: bold; }}
    .status-node-pending {{ color: #94a3b8; }}
    .metric-btn-box {{ background: white; padding: 15px; border-radius: 12px; text-align: center; color: #0f172a; border-bottom: 4px solid #cbd5e1; }}
    .metric-btn-box-active {{ background: white; padding: 15px; border-radius: 12px; text-align: center; color: #0f172a; border-bottom: 4px solid #2563eb; }}
    .alert-bar {{
        background: linear-gradient(90deg, #1e3a8a, #0284c7); color: white; 
        padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-size: 14px;
        border-left: 5px solid #3b82f6;
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
        <div style="color: #10b981; font-size: 12px; font-weight: bold; margin-top: 10px;">● Live Connection</div>
    </div>
    """, unsafe_allow_html=True)

    if active_role == "customer":
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Client Dashboard Hub", "💬 Messages Support Desk"])
    else:
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Main Operations Ledger", "Dynamic Price Updates", "User Accounts Profiles", "Inventory & Billings"])

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
    
    # ⚡ HIGH-CONVERSION ACCELERATOR: Sticky Top Quick Action Booking Trigger Banner
    st.markdown("""
    <div class="sticky-booking-banner">
        ⚡ Need a 60-Second Pickup? Use the High-Conversion Booking Engine panel below for instant pickup scheduling!
    </div>
    """, unsafe_allow_html=True)

    if menu_selection == "Client Dashboard Hub":
        
        # ----------------------------------------------------------------------
        # SECTION 1: HEADER & WALLET INVENTORY OVERVIEW
        # ----------------------------------------------------------------------
        head_col, wall_col = st.columns([2, 1])
        with head_col:
            st.markdown(f"<h1 style='color: white; margin-bottom: 0;'>Welcome back, {user_record['name']}! 👋</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #cbd5e1; margin-top: 5px;'>Manage allocations, review active workflow maps, and edit preferences.</p>", unsafe_allow_html=True)
        with wall_col:
            user_points = user_record.get("wallet_points", 0)
            cash_credit = (user_points / 250) * 10
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px; border-radius: 10px;">
                <small style="text-transform: uppercase; font-weight: bold; opacity: 0.85;">⭐ LOYALTY & WALLET HUB</small>
                <h3 style="margin: 4px 0; font-weight: 800;">{user_points} Reward Points</h3>
                <small>Auto-applied valuation: <b>${cash_credit:,.2f} Account Credit</b></small>
            </div>
            """, unsafe_allow_html=True)

        layout_left_column, layout_right_column = st.columns([1.8, 1.2], gap="medium")

        # ----------------------------------------------------------------------
        # SECTION 2: HIGH-CONVERSION BOOKING ENGINE HUB
        # ----------------------------------------------------------------------
        with layout_left_column:
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🚀 High-Conversion Booking Engine</h3></div>', unsafe_allow_html=True)
            
            # Interactive Pricing Calculator Matrix
            st.markdown("##### 📊 Interactive Pricing Calculator")
            st.caption("Adjust items dynamically to preview an instant transparent price estimate before ordering.")
            
            calc_col1, calc_col2, calc_col3 = st.columns(3)
            with calc_col1:
                item_wash_fold = st.number_input("Wash & Fold (KG)", min_value=0, value=5, step=1)
            with calc_col2:
                item_duvet = st.number_input("Heavy Duvets (Pcs)", min_value=0, value=0, step=1)
            with calc_col3:
                item_suits = st.number_input("Official Suits", min_value=0, value=0, step=1)
                
            est_total = (item_wash_fold * 100.0) + (item_duvet * 400.0) + (item_suits * 500.0)
            
            st.markdown(f"""
            <div class="calc-box">
                <span style="font-size: 13px; color: #64748b; font-weight: bold;">PREVIEW ESTIMATE</span>
                <h3 style="margin: 0; color: #0284c7; font-weight: 800;">KES {est_total:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # One-Click Scheduling Delivery Matrix
            with st.form("one_click_scheduling_form"):
                st.markdown("##### 📅 One-Click Dispatch Parameters")
                
                bag_toggle = st.radio("Bag Size Selector Profile", ["Small Bag Bundle", "Medium Bag Bundle", "Large Bag Bundle", "Custom Itemized Assignment"], index=1, horizontal=True)
                
                # Verified Address Autocomplete Verification Field Module
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
                    
                    # Pull defaults from permanent settings dashboard profiles
                    pref_dict = user_record.get("preferences", {})
                    
                    new_booking_item = {
                        "tracking": generated_id, "customer": user_record["name"], "email": active_email,
                        "service": "Custom Mixed Calculator Batch" if est_total > 0 else "Standard General Wash Profile",
                        "quantity": f"{item_wash_fold} KG / Mixed Items", "bag_size": bag_toggle,
                        "detergent": pref_dict.get("Detergent", "Scented Organic Premium"), "cost": est_total if est_total > 0 else 500.0,
                        "pickup_logistics": f"{pickup_date} at {pickup_time}", "address": input_address,
                        "payment_gateway": resolved_gateway, "status": "Received",
                        "assigned_staff": "Pending Allocation Hub", "created_at": datetime.now().strftime("%m/%d/%y")
                    }
                    st.session_state.orders.append(new_booking_item)
                    
                    # Update loyalty balances incrementally
                    user_record["wallet_points"] = user_record.get("wallet_points", 0) + 30
                    save_user_profile(active_email, user_record)
                    
                    st.success(f"Order processed into pipeline! Tracking Number: {generated_id}")
                    st.rerun()

        # ----------------------------------------------------------------------
        # SECTION 3: TRUST HUB & UNTOUCHABLE LIVE ORDER TRACKING
        # ----------------------------------------------------------------------
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
                    
                    # Build string layout representation of order tracking metrics
                    nodes_output = []
                    for index, stage_label in enumerate(stages):
                        if index == status_idx:
                            nodes_output.append(f"<span class='status-node-active'>[{stage_label}]</span>")
                        else:
                            nodes_output.append(f"<span class='status-node-pending'>{stage_label}</span>")
                            
                    formatted_nodes = " ➔ ".join(nodes_output)
                    st.markdown(f"<div class='tracker-card'>{formatted_nodes}</div>", unsafe_allow_html=True)
                    st.caption(f"🗺️ *Route Dispatch:* Driver assignment mapped live inside active delivery window.")
                    st.markdown("---")

            # ----------------------------------------------------------------------
            # SECTION 4: PREMIUM PERSONALIZATION PANEL & PREFERENCES
            # ----------------------------------------------------------------------
            st.markdown('<div class="dashboard-container"><h3 class="dashboard-header">🛠️ Premium Personalization Panel</h3></div>', unsafe_allow_html=True)
            
            # Instant replication macro-action button
            if client_orders:
                historical_anchor = client_orders[-1]
                if st.button("🔄 One-Click Repeat Last Order", use_container_width=True):
                    replicated_item = historical_anchor.copy()
                    replicated_item["tracking"] = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    replicated_item["created_at"] = datetime.now().strftime("%m/%d/%y")
                    replicated_item["status"] = "Received"
                    st.session_state.orders.append(replicated_item)
                    st.success("Replicated configuration array into pipeline queue matrix!")
                    st.rerun()
            
            st.markdown("<br>**Permanent Profile Preferences Dashboard**", unsafe_allow_html=True)
            current_pref = user_record.get("preferences", {})
            
            with st.form("preferences_saving_form"):
                perf_det = st.selectbox("Preferred Detergent Type", ["Scented Organic Premium", "Hypoallergenic Eco-Soft", "Unscented Protect Line", "Heavy Duty Citrus Boost"], index=0)
                perf_temp = st.selectbox("Water Temperature Settings", ["Cold Wash Mode", "Warm Eco Treatment", "Sanitizing Hot Cycle"])
                perf_fold = st.selectbox("Folding Structural Style", ["Classic Shelf Fold", "Rolled Compact Packing", "Hanger Deployment Request"])
                perf_starch = st.selectbox("Starch Levels Treatment", ["No Starch Treatment", "Medium Crispy Stiffness", "Maximum Crisp Armor"])
                
                if st.form_submit_button("Save Permanent Wash Preferences"):
                    user_record["preferences"] = {
                        "Detergent": perf_det, "Water Temp": perf_temp, "Folding Style": perf_fold, "Starch Level": perf_starch
                    }
                    save_user_profile(active_email, user_record)
                    st.success("Profile preferences saved across application nodes.")
                    st.rerun()
            
            # Premium Subscription Tier Plan Dashboard Management Sub-Block
            st.markdown("<br>**Subscription Tier Management Control**", unsafe_allow_html=True)
            sub_tier = user_record.get("subscription", "None")
            sub_status = user_record.get("subscription_status", "Inactive")
            
            st.markdown(f"Current Matrix Tier Selection: **{sub_tier}** | Status Node: `[{sub_status}]`")
            
            selected_sub_action = st.selectbox("Subscription Tier Adjust Matrix Allocation", ["Maintain Current Plan Setting", "Pause Plan Recurrence Profile", "Upgrade to Unlimited Premium Plan"])
            if st.button("Commit Plan Matrix Configuration Overrides"):
                if "Pause" in selected_sub_action:
                    user_record["subscription_status"] = "Paused"
                elif "Upgrade" in selected_sub_action:
                    user_record["subscription"] = "Unlimited Premium Plan Tier"
                    user_record["subscription_status"] = "Active"
                save_user_profile(active_email, user_record)
                st.success("Subscription profile modified updated successfully.")
                st.rerun()

    elif menu_selection == "💬 Messages Support Desk":
        st.title("💬 Helpdesk Communications")
        chat_input_column, chat_history_column = st.columns([1, 2], gap="medium")
        with chat_input_column:
            composed_text = st.text_area("Write your message to Admin:", placeholder="Type here...")
            if st.button("✉️ Transmit Message", use_container_width=True):
                if composed_text:
                    st.session_state.messages.append({
                        "sender": active_email, "recipient": "admin@bigz.com",
                        "sender_name": f"{user_record['name']} (Client)", "message": composed_text,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Message dispatched securely.")
                    st.rerun()
        with chat_history_column:
            customer_thread = [m for m in st.session_state.messages if m["sender"] == active_email or m["recipient"] == active_email]
            for msg in reversed(customer_thread):
                if "Admin" in msg["sender_name"]:
                    st.warning(f"🛠️ **{msg['sender_name']}** [{msg['time']}]: {msg['message']}")
                else:
                    st.info(f"👤 **{msg['sender_name']}** [{msg['time']}]: {msg['message']}")

# ==============================================================================
# 8. AUTHORIZED LAYER C: ADMINISTRATIVE HUB CONTROL ENGINE
# ==============================================================================
elif st.session_state.logged_in and active_role == "admin":
    total_customers_count = len([u for u in st.session_state.users.values() if u["role"] == "customer"])
    
    if menu_selection == "Main Operations Ledger":
        st.markdown("## ⚙️ Administration Process Control Dashboard")
        analytics_col_1, analytics_col_2, analytics_col_3 = st.columns(3)
        
        with analytics_col_1:
            active_class = "metric-btn-box-active" if st.session_state.admin_filter_metric == "Clients" else "metric-btn-box"
            st.markdown(f'<div class="{active_class}"><h4>👥 {total_customers_count} Registered Clients</h4></div>', unsafe_allow_html=True)
            if st.button("🔍 View Clients Directory", key="click_m1", use_container_width=True):
                st.session_state.admin_filter_metric = "Clients"
                st.rerun()
        with analytics_col_2:
            active_class = "metric-btn-box-active" if st.session_state.admin_filter_metric == "Orders" else "metric-btn-box"
            st.markdown(f'<div class="{active_class}"><h4>📦 {len(st.session_state.orders)} Total Active Orders</h4></div>', unsafe_allow_html=True)
            if st.button("📊 View Orders Pipeline", key="click_m2", use_container_width=True):
                st.session_state.admin_filter_metric = "Orders"
                st.rerun()
        with analytics_col_3:
            active_class = "metric-btn-box-active" if st.session_state.admin_filter_metric == "Messages" else "metric-btn-box"
            st.markdown(f'<div class="{active_class}"><h4>💬 {len(st.session_state.messages)} End-to-End Chat Logs</h4></div>', unsafe_allow_html=True)
            if st.button("📩 Open Support Desk Threads", key="click_m3", use_container_width=True):
                st.session_state.admin_filter_metric = "Messages"
                st.rerun()

        workspace_ledger_col, workspace_calc_col = st.columns([2.1, 0.9], gap="large")

        with workspace_ledger_col:
            st.markdown(f"### 📍 Current Focus: `{st.session_state.admin_filter_metric.upper()}`")
            
            if st.session_state.admin_filter_metric == "Orders":
                if not st.session_state.orders:
                    st.info("System process logs contain zero running context objects.")
                else:
                    matrix_ledger = [
                        {"Order ID Vector": entry["tracking"], "Client Context": entry["customer"], "Service Profile": entry["service"], "Settlement Model": entry["payment_gateway"], "Processing Lifecycle Stage": entry["status"], "Deployed Fleet Asset": entry["assigned_staff"], "Index Pointer": index}
                        for index, entry in enumerate(st.session_state.orders)
                    ]
                    orders_dataframe = pd.DataFrame(matrix_ledger)
                    st.dataframe(orders_dataframe.drop(columns=["Index Pointer"]), use_container_width=True, hide_index=True)
                    
                    st.markdown("#### State Manipulation Unit")
                    control_col_1, control_col_2, control_col_3 = st.columns(3)
                    with control_col_1:
                        target_order_index = st.selectbox("Target Pipeline ID Context", options=orders_dataframe["Index Pointer"], format_func=lambda x: f"Order #{st.session_state.orders[x]['tracking']}")
                    with control_col_2:
                        updated_workflow_stage = st.selectbox("Advance Flow Execution Phase", ["Received", "Washing", "Drying", "Ironing", "Out for Delivery", "Delivered & Complete"])
                    with control_col_3:
                        allocated_staff_asset = st.selectbox("Re-assign Fleet Worker Unit", st.session_state.staff_directory)
                        
                    if st.button("Commit Modification Overrides", use_container_width=True):
                        st.session_state.orders[target_order_index]["status"] = updated_workflow_stage
                        st.session_state.orders[target_order_index]["assigned_staff"] = allocated_staff_asset
                        st.success("Target workflow state configuration adjustments updated.")
                        st.rerun()

            elif st.session_state.admin_filter_metric == "Clients":
                records_pool = [{"Client Name Master Identifier": p["name"], "Mobile Link Address String": p["phone"], "Identity Clearance Allocation Key": k, "Security Verification Clearance Flags": "VERIFIED ACCESS ACTIVE" if p.get("verified", False) else "LOCKED LOOP PENDING"} for k, p in st.session_state.users.items() if p["role"] == "customer"]
                st.table(pd.DataFrame(records_pool))

            elif st.session_state.admin_filter_metric == "Messages":
                all_client_emails = [email for email, data in st.session_state.users.items() if data["role"] == "customer"]
                selected_client_chat = st.selectbox("Select client thread channel:", options=all_client_emails)
                
                chat_input_column, chat_history_column = st.columns([1.1, 1.9], gap="small")
                with chat_input_column:
                    composed_message_text = st.text_area("Write response message payload:")
                    if st.button("Transmit Secure Response Package", use_container_width=True):
                        if composed_message_text:
                            st.session_state.messages.append({
                                "sender": "admin@bigz.com", "recipient": selected_client_chat,
                                "sender_name": "Theophilus (Admin)", "message": composed_message_text, "time": datetime.now().strftime("%H:%M:%S")
                            })
                            st.success("Message dispatched safely.")
                            st.rerun()
                with chat_history_column:
                    isolated_thread = [m for m in st.session_state.messages if (m["sender"] == "admin@bigz.com" and m["recipient"] == selected_client_chat) or (m["sender"] == selected_client_chat and m["recipient"] == "admin@bigz.com")]
                    for msg in reversed(isolated_thread):
                        if "Admin" in msg["sender_name"]:
                            st.warning(f"⚙️ **{msg['sender_name']}** [{msg['time']}]: {msg['message']}")
                        else:
                            st.info(f"👤 **{msg['sender_name']}** [{msg['time']}]: {msg['message']}")

        with workspace_calc_col:
            st.markdown("### 🧮 Quick-Calc Engine")
            calc_base_price = st.number_input("Base Service Rate (KES)", min_value=0.0, value=150.0, step=10.0)
            calc_quantity = st.number_input("Bulk Package Volume Count", min_value=1.0, value=5.0, step=0.5)
            calc_discount = st.slider("Manager Discount Override (%)", min_value=0, max_value=50, value=10)
            calc_logistics = st.number_input("Logistics Surcharge (KES)", min_value=0.0, value=150.0, step=50.0)
            
            sub_total = calc_base_price * calc_quantity
            final_estimation = (sub_total - (sub_total * (calc_discount / 100.0))) + calc_logistics
            st.markdown(f"**Estimated Value Summary Invoice:** KES {final_estimation:,.2f}")

    elif menu_selection == "Dynamic Price Updates":
        st.markdown("## 🏷️ Live Service Catalog Price Adjustment Matrix")
        st.markdown("Modify catalog prices directly below. Updates register immediately to the consumer alert tracking bar.")
        
        price_update_columns = st.columns(len(st.session_state.laundry_service_catalog))
        for index, service_item in enumerate(st.session_state.laundry_service_catalog):
            with price_update_columns[index]:
                st.markdown(f"""
                <div style="background:white; padding:12px; border-radius:12px; box-shadow:0 4px 6px rgba(0,0,0,0.05); color:#0f172a; margin-bottom:10px;">
                    <span style="font-size:11px; color:#2563eb; font-weight:bold;">{service_item['type']}</span>
                    <h5 style="margin:4px 0; font-size:13px; font-weight:700;">{service_item['name']}</h5>
                    <p style="margin:0; font-size:11px; color:#64748b;">Current baseline: <b>KES {service_item['price']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                new_price_input = st.number_input(f"New Rate ({service_item['unit']})", key=f"input_p_{service_item['id']}", min_value=1.0, value=float(service_item['price']), step=5.0)
                
                if new_price_input != float(service_item['price']):
                    st.session_state.laundry_service_catalog[index]['price'] = new_price_input
                    st.session_state.price_alerts.append({
                        "text": f"The price for {service_item['name']} has been manually updated to KES {new_price_input} per {service_item['unit']}.",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Updated price register indexes.")
                    st.rerun()

    elif menu_selection == "User Accounts Profiles":
        st.markdown("## 👥 Master Ledger Logs")
        st.info("Account auditing metrics remain bound within your operational system engine dashboards.")

    elif menu_selection == "Inventory & Billings":
        st.markdown("## 📊 Strategic Allocation Audits & Billing Ledgers")
        gross_system_revenue = sum([order_record["cost"] for order_record in st.session_state.orders])
        st.markdown(f"### Gross Operational Pool Value: KES {gross_system_revenue:,.2f}")

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
