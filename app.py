import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. GLOBAL SYSTEM CONFIGURATION & CONSTANTS
# ==============================================================================
DATABASE_FILE_PATH = "users_db.json"
APP_THEME_COLOR_PRIMARY = "#2563eb"
APP_THEME_COLOR_SECONDARY = "#3b82f6"

# Unified pricing catalog
LAUNDRY_SERVICE_CATALOG = [
    {"name": "Wash & Fold (General Wear)", "price": 100, "unit": "KG", "type": "Wash & Fold"},
    {"name": "Wash, Dry, Iron & Fold", "price": 140, "unit": "KG", "type": "Wash & Fold"},
    {"name": "Heavy Blanket / Duvet", "price": 400, "unit": "Piece", "type": "Dry Clean"},
    {"name": "Official Suits (Jacket & Trousers)", "price": 500, "unit": "Suit", "type": "Dry Clean"},
    {"name": "Sneaker / Canvas Shoe Cleaning", "price": 200, "unit": "Pair", "type": "Wash & Fold"}
]

st.set_page_config(
    page_title="BIGZ CLEANERS",
    page_icon="🧺",
    layout="wide"
)

# ==============================================================================
# 2. PERSISTENT STORAGE LAYER ENGINE (JSON FILE BASE)
# ==============================================================================
def load_user_database() -> dict:
    """Reads user records from disk file or returns system defaults if missing."""
    default_records = {
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
            "preferences": {
                "Detergent type": "Scented Organic", 
                "Starched Shirts": "Medium Crispy Stiffness"
            }
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
    """Saves or edits a specific user profile on local storage disk."""
    current_database = load_user_database()
    clean_email = email_key.lower().strip()
    current_database[clean_email] = profile_data
    
    with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as file_handle:
        json.dump(current_database, file_handle, indent=4)


# Ensure user database is globally read from disk file on every rerun loop
st.session_state.users = load_user_database()

# ==============================================================================
# 3. INITIALIZE STATE RUNTIME MEMORY
# ==============================================================================
state_defaults = {
    "logged_in": False,
    "current_user": "",
    "current_email": "",
    "current_role": "",
    "messages": [],
    "pending_verification": None,
    "inventory": {
        "Detergent (L)": 180, 
        "Fabric Softener (L)": 95, 
        "Tags & Bags (Pcs)": 450
    },
    "staff_directory": ["Alex Chen", "Marix Mason", "John Doe", "Theophilus mose"],
    "orders": [
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
            "payment_gateway": "Secure Card Payment Gateway", "status": "Washing", "assigned_staff": "Alex Chen",
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
}

for state_key, default_value in state_defaults.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value

# ==============================================================================
# 4. GRAPHICAL UI ELEMENT CUSTOMIZATION (CSS STYLE CODES)
# ==============================================================================
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #020617, #0f172a, #1e3a8a, #0284c7);
        background-attachment: fixed;
    }}
    .service-card {{ 
        background: white; 
        padding: 22px; 
        border-radius: 16px; 
        margin-bottom: 20px; 
        color: #0f172a; 
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); 
        border-top: 5px solid {APP_THEME_COLOR_PRIMARY};
    }}
    .footer {{ 
        text-align: center; 
        color: #94a3b8; 
        padding: 40px 0; 
        margin-top: 60px; 
        border-top: 1px solid rgba(255,255,255,0.1); 
    }}
    div[data-testid="stExpander"] {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }}
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
        <div style="width: 70px; height: 70px; background: {APP_THEME_COLOR_SECONDARY}; border-radius: 50%; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white;">
            {initial_letter}
        </div>
        <h4 style="color: white; margin: 0;">{user_record['name']}</h4>
        <p style="color: #cbd5e1; font-size: 12px; margin: 2px 0 0 0;">{active_role.upper()} HUB</p>
        <p style="color: #4ade80; font-size: 11px; margin-top: 6px;">● Secure Layer Connected</p>
    </div>
    """, unsafe_allow_html=True)

    if active_role == "customer":
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

# ==============================================================================
# 6. UNVERIFIED LAYER A: PUBLIC LANDING ARCHITECTURE
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
        
        # FIXED: Added the columns assignment statement here to fix the NameError crash
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
            
        st.markdown("""
        <div style="margin-top: 45px; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 25px;">
            <p style="color: #cbd5e1; font-style: italic; font-size: 15px; margin-bottom: 5px;">
                "Managing my laundry has never been simpler! Dynamic updates give complete peace of mind."
            </p>
            <p style="color: #60a5fa; font-weight: 600; font-size: 14px;">– Sarah Chen, Business Partner</p>
        </div>
        """, unsafe_allow_html=True)

    with authorization_portal_column:
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: white; font-weight: 700;'>GET STARTED OR LOG IN</h2></div>", unsafe_allow_html=True)
        
        if st.session_state.pending_verification:
            st.markdown(f"""
            <div style="background: #fffbeb; border-left: 5px solid #d97706; padding: 20px; border-radius: 12px; color: #92400e; margin-bottom: 20px;">
                <h4 style="margin: 0 0 6px 0; font-weight: 700;">⚠️ Email Verification Security Loop</h4>
                <p style="font-size: 14px; margin: 0;">A system dispatch link has been pushed to: <b>{st.session_state.pending_verification}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Simulate Incoming Verification Confirm Link", use_container_width=True):
                target_email = st.session_state.pending_verification.lower().strip()
                if target_email in st.session_state.users:
                    updated_profile = st.session_state.users[target_email]
                    updated_profile["verified"] = True
                    save_user_profile(target_email, updated_profile)
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
                    input_email = st.text_input("Registered Email Address", placeholder="name@domain.com")
                    input_password = st.text_input("Secure Account Password", type="password", placeholder="••••••••")
                    
                    if st.form_submit_button("LOG IN TO DASHBOARD", use_container_width=True):
                        clean_login_email = input_email.lower().strip()
                        if clean_login_email in st.session_state.users:
                            matched_user_record = st.session_state.users[clean_login_email]
                            if matched_user_record["password"] == input_password:
                                if not matched_user_record.get("verified", False):
                                    st.error("Account registration sequence remains unverified. Entry halted.")
                                else:
                                    st.session_state.logged_in = True
                                    st.session_state.current_user = matched_user_record["name"]
                                    st.session_state.current_email = clean_login_email
                                    st.session_state.current_role = matched_user_record["role"]
                                    st.rerun()
                            else:
                                st.error("Invalid password authentication handshake.")
                        else:
                            st.error("Profile identity mismatch or data entry empty.")
                            
            with signup_tab:
                st.markdown("<p style='color: #cbd5e1; font-weight: bold; margin-bottom: 15px;'>CREATE YOUR FREE ACCOUNT</p>", unsafe_allow_html=True)
                selected_role_type = st.selectbox("Assign Profile Blueprint Type:", ["Client / Consumer Account", "Admin / Production Staff"])
                
                with st.form("signup_panel_form"):
                    signup_name = st.text_input("Full Signature Name")
                    signup_phone = st.text_input("Phone Communication Line")
                    signup_email_raw = st.text_input("Email Account Address")
                    signup_address = st.text_input("Primary Physical Delivery Location")
                    signup_password = st.text_input("Set Custom Access Password", type="password")
                    
                    if st.form_submit_button("SUBMIT APPLICATION FILES", use_container_width=True):
                        clean_signup_email = signup_email_raw.lower().strip()
                        if clean_signup_email in st.session_state.users:
                            st.error("Account token identifier already registered.")
                        elif not clean_signup_email or not signup_password:
                            st.error("Required fields cannot remain blank.")
                        else:
                            assigned_role = "customer" if "Client" in selected_role_type else "admin"
                            is_verified_by_default = True if assigned_role == "admin" else False
                            
                            new_profile_blueprint = {
                                "name": signup_name, 
                                "phone": signup_phone, 
                                "address": signup_address,
                                "password": signup_password, 
                                "role": assigned_role, 
                                "verified": is_verified_by_default,
                                "saved_cards": ["•••• •••• •••• 1111"],
                                "preferences": {"Detergent type": "Scented Organic", "Starched Shirts": "No Starch Treatment"}
                            }
                            
                            save_user_profile(clean_signup_email, new_profile_blueprint)
                            
                            if assigned_role == "customer":
                                st.session_state.pending_verification = clean_signup_email
                            else:
                                st.success("Administrative clearance granted! Log in via portal.")
                            st.rerun()

# ==============================================================================
# 7. AUTHORIZED LAYER B: CONSUMER WORKSPACE PAGES
# ==============================================================================
elif st.session_state.logged_in and active_role == "customer":
    
    # NEW FEATURE 1: Loyalty Rewards System Calculation
    client_all_orders = [o for o in st.session_state.orders if o["email"] == active_email]
    total_spent = sum([order["cost"] for order in client_all_orders])
    loyalty_points = int(total_spent // 100) # 1 Point for every 100 KES spent
    
    if menu_selection == "Service Dashboard":
        dashboard_header_col1, dashboard_header_col2 = st.columns([2, 1])
        with dashboard_header_col1:
            st.markdown("## 🧺 Premium Laundry Processing Packages Catalog")
        with dashboard_header_col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #eab308, #ca8a04); padding: 10px 18px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="font-size: 11px; font-weight: bold; letter-spacing: 1px; opacity: 0.9;">BIGZ LOYALTY CLUB</span>
                <h3 style="margin: 2px 0 0 0; font-weight: 800;">⭐ {loyalty_points} REWARD POINTS</h3>
            </div>
            """, unsafe_allow_html=True)
        
        card_column_1, card_column_2, card_column_3 = st.columns(3)
        for index, item in enumerate(LAUNDRY_SERVICE_CATALOG):
            selected_column = [card_column_1, card_column_2, card_column_3][index % 3]
            with selected_column:
                st.markdown(f"""
                <div class="service-card">
                    <h3 style="margin: 0; color: #1e3a8a;">{item['name']}</h3>
                    <p style="margin: 5px 0; font-size: 14px; color: #64748b;">Processing Line: <b>{item['type']}</b></p>
                    <h4 style="margin: 10px 0 0 0; color: #10b981;">KES {item['price']} per {item['unit']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.markdown("## ➕ Initialize Custom Order Pipeline")
        
        with st.expander("Configure Flowchart Multi-Step Order Intake Engine", expanded=True):
            selected_type = st.radio("Step 1: Specify Pipeline Operational Processing Type", ["Wash & Fold", "Dry Clean"], horizontal=True)
            filtered_services = [s for s in LAUNDRY_SERVICE_CATALOG if s["type"] == selected_type]
            
            chosen_service_name = st.selectbox("Step 2: Select Targeted System Package", [s["name"] for s in filtered_services])
            service_profile = next(s for s in LAUNDRY_SERVICE_CATALOG if s["name"] == chosen_service_name)
            
            order_quantity = st.number_input(f"Step 2.1: Quantity Selection ({service_profile['unit']})", min_value=1, value=1)
            calculated_total_cost = service_profile["price"] * order_quantity
            
            logistics_col_1, logistics_col_2 = st.columns(2)
            delivery_date = logistics_col_1.date_input("Step 3: Schedule Pickup Date Anchor")
            delivery_time = logistics_col_2.time_input("Step 3.1: Select Fleet Scheduling Time Window")
            logistics_address = st.text_input("Step 3.2: Logistic Route Destination Mapping", value=user_record.get("address", ""))
            
            st.markdown(f"### Total Pipeline Cost Matrix Evaluation: <span style='color:#10b981;'>KES {calculated_total_cost}</span>", unsafe_allow_html=True)
            payment_method_gateway = st.selectbox("Step 4: Secure Transaction Gateway Routing Matrix", ["M-Pesa Express", "Secure Card Payment Gateway"])
            
            if st.button("💳 Proceed & Trigger Payment Engine Settlement", use_container_width=True):
                if not logistics_address:
                    st.error("Route mapping field context validation required before checkout.")
                else:
                    unique_tracking_id = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    new_order_record = {
                        "tracking": unique_tracking_id, "customer": user_record["name"], "email": active_email,
                        "service": chosen_service_name, "quantity": f"{order_quantity} {service_profile['unit']}", "cost": calculated_total_cost,
                        "pickup_logistics": f"{delivery_date} at {delivery_time}", "address": logistics_address,
                        "payment_gateway": f"{payment_method_gateway} (Transaction Confirmed)", "status": "Pickup",
                        "assigned_staff": "Pending Scheduling Hub Allocation", "created_at": datetime.now().strftime("%m/%d/%y")
                    }
                    st.session_state.orders.append(new_order_record)
                    st.balloons()
                    st.success(f"Processing Order Stream generated successfully! ID Token: {unique_tracking_id}")
                    st.rerun()

        st.markdown("### Profile Manifest Active Tracking Vectors")
        client_active_orders = [order for order in st.session_state.orders if order["email"] == active_email]
        if not client_active_orders:
            st.caption("No active tracking segments allocated currently under this consumer record profile context.")
        else:
            tracking_grid_columns = st.columns(4)
            for index, order in enumerate(client_active_orders):
                grid_column_target = tracking_grid_columns[index % 4]
                with grid_column_target:
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; color: black; margin-bottom: 15px;">
                        <span style="float: right; font-size: 11px; background: #dbeafe; color: #1e40af; padding: 2px 6px; border-radius: 8px; font-weight: bold;">{order['status']}</span>
                        <h4 style="margin: 0 0 5px 0; color: #1e3a8a;">{order['tracking']}</h4>
                        <p style="margin: 5px 0 0 0; font-size: 12px; color: #475569;">Package: {order['service']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif menu_selection == "My Profile Account":
        st.markdown("## 👤 Configuration Preferences & Profile Management")
        profile_edit_col, settings_wallet_col = st.columns([1.1, 0.9], gap="large")
        
        with profile_edit_col:
            st.markdown("### Core Registration Data Modification Registry")
            with st.form("profile_data_form"):
                modified_name = st.text_input("Profile Display Name Entity", value=user_record["name"])
                modified_phone = st.text_input("Active Communications Connection String", value=user_record["phone"])
                modified_address = st.text_area("Default Operational Delivery Address Log", value=user_record.get("address", ""))
                
                if st.form_submit_button("Commit Account Database Mutation"):
                    user_record["name"] = modified_name
                    user_record["phone"] = modified_phone
                    user_record["address"] = modified_address
                    save_user_profile(active_email, user_record)
                    st.success("Storage registers updated effectively inside central database file.")
                    st.rerun()

        with settings_wallet_col:
            st.markdown("### Vault Storage Credit Methods Tokens")
            for credit_card_mask in user_record.get("saved_cards", []):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
                    <p style="margin: 0; font-size: 10px; opacity: 0.7; letter-spacing: 1px;">BIGZ GATEWAY WALLET INTEGRATION</p>
                    <h3 style="margin: 8px 0; letter-spacing: 3px;">{credit_card_mask}</h3>
                    <p style="margin: 0; font-size: 11px; text-align: right; opacity: 0.9;">SECURE SIGNATURE VERIFIED</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### System Formulation Metrics & Preferences")
            preferred_detergent = st.selectbox("Default Detergent Type Formula Profile", ["Scented Organic", "Hypoallergenic Neutral", "Heavy Stain-Fighter Extra"])
            preferred_starch = st.selectbox("Garment Stiffness Calibration Ratio", ["No Starch Treatment", "Medium Crispy Stiffness", "High Executive Starched Stiff"])
            if st.button("Overwrite Custom Configuration Maps"):
                user_record["preferences"]["Detergent type"] = preferred_detergent
                user_record["preferences"]["Starched Shirts"] = preferred_starch
                save_user_profile(active_email, user_record)
                st.success("Preferences synchronized permanently to backend database storage registries.")

# ==============================================================================
# 8. AUTHORIZED LAYER C: ADMINISTRATIVE HUB CONTROL ENGINE
# ==============================================================================
elif st.session_state.logged_in and active_role == "admin":
    
    if menu_selection == "Main Operations Ledger":
        st.markdown("## ⚙️ Administration Engine Real-Time Process Control Dashboard")
        
        st.markdown("### 🔍 Enterprise Core System Service Tracking Pipeline")
        if not st.session_state.orders:
            st.info("System process logs contain zero running context objects currently.")
        else:
            matrix_ledger = [
                {
                    "Index Pointer": index,
                    "Order ID Vector": entry["tracking"],
                    "Client Context": entry["customer"],
                    "Processing Lifecycle Stage": entry["status"],
                    "Deployed Fleet Asset": entry["assigned_staff"],
                    "System Timestamp": entry["created_at"]
                } for index, entry in enumerate(st.session_state.orders)
            ]
            orders_dataframe = pd.DataFrame(matrix_ledger)
            
            # NEW FEATURE 2: Interactive Real-Time Search & Pipeline Status Filter Engine
            filter_col1, filter_col2 = st.columns([2, 1])
            with filter_col1:
                search_query = st.text_input("🔍 Quick Search Registry Ledger (Type Track ID or Customer Name)", placeholder="e.g. Sarah Chen or BIGZ-12341")
            with filter_col2:
                status_filter = st.selectbox("🎯 Filter by Processing Phase", ["All Statuses", "Pickup", "Washing", "Drying", "Fold", "Ready for Delivery"])
            
            # Applying live query rules to data layout view
            filtered_df = orders_dataframe.copy()
            if search_query:
                filtered_df = filtered_df[
                    filtered_df["Order ID Vector"].str.contains(search_query, case=False) | 
                    filtered_df["Client Context"].str.contains(search_query, case=False)
                ]
            if status_filter != "All Statuses":
                filtered_df = filtered_df[filtered_df["Processing Lifecycle Stage"] == status_filter]
                
            st.dataframe(filtered_df.drop(columns=["Index Pointer"]), use_container_width=True, hide_index=True)
            
            st.markdown("#### Production Workflow State Manipulation Unit")
            control_col_1, control_col_2, control_col_3 = st.columns(3)
            with control_col_1:
                target_order_index = st.selectbox(
                    "Select Target Pipeline Execution ID Context", 
                    options=orders_dataframe["Index Pointer"], 
                    format_func=lambda x: f"Order #{st.session_state.orders[x]['tracking']} [{st.session_state.orders[x]['customer']}]"
                )
            with control_col_2:
                updated_workflow_stage = st.selectbox(
                    "Advance Flowchart Execution Phase", 
                    ["Pickup", "Washing", "Drying", "Fold", "Ready for Delivery", "Delivered & Complete"]
                )
            with control_col_3:
                allocated_staff_asset = st.selectbox("Re-assign Operational Fleet Worker Unit", st.session_state.staff_directory)
                
            if st.button("Commit Production Modification Instructions Override", use_container_width=True):
                st.session_state.orders[target_order_index]["status"] = updated_workflow_stage
                st.session_state.orders[target_order_index]["assigned_staff"] = allocated_staff_asset
                
                st.session_state.messages.append({
                    "name": "SYSTEM PRODUCTION AUTOMATION BOT",
                    "message": f"Order Framework Context Update Notification [{st.session_state.orders[target_order_index]['tracking']}]: Package lifecycle status progressed to '{updated_workflow_stage}' under deployment tracker asset: {allocated_staff_asset}.",
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.success("Target workflow state configuration adjustments updated across operations ledger logs.")
                st.rerun()

        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("### Distribution Mapping Dispatch Vectors Matrix")
            st.info("🌐 Core GPS Fleet Matrix Mapping Connection Layer Connected Nominally.")
            st.markdown("""
            <div style="background: white; padding: 18px; border-radius: 12px; color: black; border-left: 5px solid #a855f7;">
                <b>Active Shift Route Log Tracking Checklist:</b><br>
                • Alex Chen — Route Segment Northwest Alpha Operational Block (08:00 - 12:00)<br>
                • Marix Mason — Route Segment Central Core Cargo Zone (13:00 - 17:00)
            </div>
            """, unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("### Expand Core Product Catalog Framework Matrix")
            with st.form("catalog_append_form"):
                append_catalog_name = st.text_input("New Core Service Label")
                append_catalog_price = st.number_input("Rate Calculation Standard Asset Value (KES)", min_value=10, value=150)
                append_catalog_unit = st.selectbox("Unit Metric Scale", ["KG", "Piece", "Pair", "Suit"])
                append_catalog_category = st.selectbox("Pipeline System Assignment Type Context", ["Wash & Fold", "Dry Clean"])
                
                if st.form_submit_button("Append Service Package Vector To Core Arrays"):
                    if append_catalog_name:
                        LAUNDRY_SERVICE_CATALOG.append({
                            "name": append_catalog_name, 
                            "price": append_catalog_price, 
                            "unit": append_catalog_unit, 
                            "type": append_catalog_category
                        })
                        st.success(f"Production matrix catalog expanded: Added target row asset vector '{append_catalog_name}'")
                    else:
                        st.error("Operation validation aborted. Name parameters missing definitions.")

    elif menu_selection == "User Accounts Profiles":
        st.markdown("## 👥 Active Database Consumers Master Profiles Register Ledger (Recalled From JSON Database)")
        records_pool = []
        for database_email, profile_node in st.session_state.users.items():
            if profile_node["role"] == "customer":
                records_pool.append({
                    "Client Name Master Identifier": profile_node["name"],
                    "Mobile Link Address String": profile_node["phone"],
                    "Identity Clearance Allocation Key": database_email,
                    "Security Verification Clearance Flags": "VERIFIED ACCESS ACTIVE" if profile_node.get("verified", False) else "LOCKED LOOP PENDING"
                })
        if records_pool:
            st.table(pd.DataFrame(records_pool))
        else:
            st.caption("No registered records located inside user data arrays.")

    elif menu_selection == "Inventory & Billings":
        st.markdown("## 📊 Strategic Allocation Audits & Billing Balance Ledgers")
        inventory_graph_col, fiscal_card_col = st.columns(2)
        
        with inventory_graph_col:
            st.markdown("### Material Commodity Supply Reservoirs")
            inventory_dataframe = pd.DataFrame.from_dict(st.session_state.inventory, orient='index', columns=['Current Resource Level'])
            st.bar_chart(inventory_dataframe)
            
            st.markdown("#### Adjust Supply Levels")
            for asset_key, quantity_value in st.session_state.inventory.items():
                updated_inventory_quantity = st.number_input(f"Stock Level Reservoir Monitor: {asset_key}", min_value=0, value=int(quantity_value), key=f"inv_input_{asset_key}")
                st.session_state.inventory[asset_key] = updated_inventory_quantity
            
        with fiscal_card_col:
            st.markdown("### Central Aggregated Accounting Audited Summaries")
            gross_system_revenue = sum([order_record["cost"] for order_record in st.session_state.orders])
            
            # NEW FEATURE 3: Predictive Smart Growth Matrix Valuation Forecast Card
            projected_forecast_revenue = gross_system_revenue * 1.25 # Projected 25% scale multiplier loop
            
            accounting_col1, accounting_col2 = st.columns(2)
            with accounting_col1:
                st.markdown(f"""
                <div style="background: white; color: #0f172a; padding: 22px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #10b981;">
                    <p style="margin: 0; font-size: 11px; color: #64748b; font-weight: bold; letter-spacing: 0.5px;">GROSS REVENUE POOL</p>
                    <h2 style="margin: 5px 0; color: #10b981; font-weight: 800;">KES {gross_system_revenue:,.2f}</h2>
                    <p style="font-size: 11px; margin: 0; color: #64748b;">Audits: Functioning Nominally</p>
                </div>
                """, unsafe_allow_html=True)
            with accounting_col2:
                st.markdown(f"""
                <div style="background: white; color: #0f172a; padding: 22px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid {APP_THEME_COLOR_SECONDARY};">
                    <p style="margin: 0; font-size: 11px; color: #64748b; font-weight: bold; letter-spacing: 0.5px;">NEXT MONTH FORECAST</p>
                    <h2 style="margin: 5px 0; color: {APP_THEME_COLOR_SECONDARY}; font-weight: 800;">KES {projected_forecast_revenue:,.2f}</h2>
                    <p style="font-size: 11px; margin: 0; color: #16a34a;">📈 +25% Growth Loop Expected</p>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# 9. UNIVERSAL LOGICAL LINK: LIVE COMMUNICATIONS CENTRAL CHAT DECK ROUTER
# ==============================================================================
if st.session_state.logged_in:
    show_chat_gate = False
    if active_role == "customer" and menu_selection == "Support Messaging Desk":
        show_chat_gate = True
    elif active_role == "admin" and menu_selection == "Main Operations Ledger":
        show_chat_gate = True
        
    if show_chat_gate:
        st.markdown("---")
        st.markdown("## 💬 Centralized Communications Network Support Routing Hub")
        chat_input_column, chat_history_column = st.columns([1, 2], gap="medium")
        
        with chat_input_column:
            composed_message_text = st.text_area("Compose System Operational Message Dispatch Package:", placeholder="Enter your logging parameters here...")
            if st.button("Transmit Packet Matrix Payload To Central Queue", use_container_width=True):
                if composed_message_text:
                    st.session_state.messages.append({
                        "name": user_record["name"],
                        "message": composed_message_text,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Data stream message matrix package successfully loaded into core stream channels.")
                    st.rerun()
                    
        with chat_history_column:
            st.markdown("#### Message Streaming Framework Ledger Streams")
            if not st.session_state.messages:
                st.caption("Active operational chat communication channels contain zero data logs traffic objects.")
            else:
                for active_message in reversed(st.session_state.messages):
                    st.info(f"🕒 [{active_message['time']}] **{active_message['name']}**: {active_message['message']}")

# ==============================================================================
# 10. SYSTEM RUNTIME APP PLATFORM TERMINAL BASE FOOTER
# ==============================================================================
st.markdown("""
<div class="footer">
    🧺 BIGZ CLEANERS <br>
    System Compliant Blueprint Core — Trusted Production Engine Unified Framework Terminal <br><br>
    © 2026 BIGZ CLEANERS
</div>
""", unsafe_allow_html=True)
