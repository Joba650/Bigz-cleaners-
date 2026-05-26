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

# Unified pricing catalog with system visual identifiers
LAUNDRY_SERVICE_CATALOG = [
    {
        "id": "srv_wash_fold",
        "name": "Wash & Fold (General Wear)", 
        "price": 100, 
        "unit": "KG", 
        "type": "Wash & Fold",
        "image_url": "https://images.unsplash.com/photo-1545173168-9f1907e80033?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "srv_wash_iron",
        "name": "Wash, Dry, Iron & Fold", 
        "price": 140, 
        "unit": "KG", 
        "type": "Wash & Fold",
        "image_url": "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "srv_duvet",
        "name": "Heavy Blanket / Duvet", 
        "price": 400, 
        "unit": "Piece", 
        "type": "Dry Clean",
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "srv_suits",
        "name": "Official Suits (Jacket & Trousers)", 
        "price": 500, 
        "unit": "Suit", 
        "type": "Dry Clean",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": "srv_shoes",
        "name": "Sneaker / Canvas Shoe Cleaning", 
        "price": 200, 
        "unit": "Pair", 
        "type": "Wash & Fold",
        "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&auto=format&fit=crop&q=60"
    }
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
    current_database = load_user_database()
    clean_email = email_key.lower().strip()
    current_database[clean_email] = profile_data
    
    with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as file_handle:
        json.dump(current_database, file_handle, indent=4)

st.session_state.users = load_user_database()

# ==============================================================================
# 3. INITIALIZE STATE RUNTIME MEMORY
# ==============================================================================
state_defaults = {
    "logged_in": False,
    "current_user": "",
    "current_email": "",
    "current_role": "",
    "selected_service_id": LAUNDRY_SERVICE_CATALOG[0]["id"],  # Default selection pointer
    "messages": [
        {"name": "SYSTEM", "message": "Welcome to BIGZ Cleaners Messaging Desk Support.", "time": "12:00:00"}
    ],
    "notifications": [
        {"text": "Welcome back! Check your service dashboard for active timelines.", "timestamp": "Just Now"}
    ],
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
        padding: 0px; 
        border-radius: 16px; 
        margin-bottom: 20px; 
        color: #0f172a; 
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); 
        overflow: hidden;
        border: 2px solid transparent;
        transition: all 0.2s ease-in-out;
    }}
    .service-card-selected {{
        background: white; 
        padding: 0px; 
        border-radius: 16px; 
        margin-bottom: 20px; 
        color: #0f172a; 
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); 
        overflow: hidden;
        border: 3px solid #3b82f6;
    }}
    .service-img {{
        width: 100%;
        height: 160px;
        object-fit: cover;
    }}
    .service-content {{
        padding: 16px;
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
    </div>
    """, unsafe_allow_html=True)

    if active_role == "customer":
        menu_selection = st.sidebar.radio("Navigation Control Menu", ["Service Dashboard", "💬 Messages Support Desk", "My Profile Account"])
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
    
    # Broadcast alerts to clients dynamically
    if st.session_state.notifications:
        with st.container():
            latest_notif = st.session_state.notifications[-1]
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #1e3a8a, #2563eb); color: white; padding: 12px 20px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div><strong>🔔 Notification Update:</strong> {latest_notif['text']}</div>
                <div style="font-size: 11px; opacity: 0.8; font-weight: bold;">{latest_notif['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)

    if menu_selection == "Service Dashboard":
        st.markdown("## 🧺 Interactive Service Menu")
        st.markdown("*Tap directly on any package card's selection button to load it instantly into your pipeline below.*")
        
        # Displaying services horizontally inside modern columns with visuals
        card_columns = st.columns(len(LAUNDRY_SERVICE_CATALOG))
        
        for index, item in enumerate(LAUNDRY_SERVICE_CATALOG):
            with card_columns[index]:
                # Determine custom style variant based on click state tracker memory
                is_selected = st.session_state.selected_service_id == item["id"]
                style_class = "service-card-selected" if is_selected else "service-card"
                
                st.markdown(f"""
                <div class="{style_class}">
                    <img src="{item['image_url']}" class="service-img" alt="{item['name']}">
                    <div class="service-content">
                        <span style="font-size: 11px; font-weight: bold; background: #f1f5f9; padding: 3px 8px; border-radius: 20px; color: #475569;">
                            {item['type']}
                        </span>
                        <h4 style="margin: 10px 0 5px 0; color: #0f172a; font-size: 15px; font-weight: 700; line-height: 1.3;">{item['name']}</h4>
                        <p style="margin: 0; color: #10b981; font-weight: bold; font-size: 14px;">KES {item['price']} / {item['unit']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Interactive trigger button built onto layout
                button_label = "✅ Selected Package" if is_selected else "📥 Tap to Select"
                if st.button(button_label, key=f"btn_{item['id']}", use_container_width=True, type="secondary" if not is_selected else "primary"):
                    st.session_state.selected_service_id = item["id"]
                    st.rerun()
                
        st.markdown("---")
        
        # Pull active service mapping structure from state selection engine index
        selected_service_profile = next(s for s in LAUNDRY_SERVICE_CATALOG if s["id"] == st.session_state.selected_service_id)
        
        st.markdown(f"## ➕ Order Placement Pipeline (`Selected: {selected_service_profile['name']}`)")
        
        with st.expander("Configure Flowchart Multi-Step Order Intake Engine", expanded=True):
            st.info(f"✨ Currently compiling invoice requirements for: **{selected_service_profile['name']}** at KES {selected_service_profile['price']} per {selected_service_profile['unit']}")
            
            order_quantity = st.number_input(f"Step 1: Specify Quantity ({selected_service_profile['unit']})", min_value=1, value=1)
            calculated_total_cost = selected_service_profile["price"] * order_quantity
            
            logistics_col_1, logistics_col_2 = st.columns(2)
            delivery_date = logistics_col_1.date_input("Step 2: Schedule Pickup Date Anchor")
            delivery_time = logistics_col_2.time_input("Step 2.1: Select Fleet Scheduling Time Window")
            logistics_address = st.text_input("Step 2.2: Logistic Route Destination Mapping", value=user_record.get("address", ""))
            
            st.markdown(f"### Total Pipeline Cost Matrix Evaluation: <span style='color:#10b981;'>KES {calculated_total_cost}</span>", unsafe_allow_html=True)
            payment_method_gateway = st.selectbox("Step 3: Secure Transaction Gateway Routing Matrix", ["M-Pesa Express", "Secure Card Payment Gateway"])
            
            if st.button("💳 Proceed & Trigger Payment Engine Settlement", use_container_width=True):
                if not logistics_address:
                    st.error("Route mapping field context validation required before checkout.")
                else:
                    unique_tracking_id = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    new_order_record = {
                        "tracking": unique_tracking_id, "customer": user_record["name"], "email": active_email,
                        "service": selected_service_profile["name"], "quantity": f"{order_quantity} {selected_service_profile['unit']}", "cost": calculated_total_cost,
                        "pickup_logistics": f"{delivery_date} at {delivery_time}", "address": logistics_address,
                        "payment_gateway": f"{payment_method_gateway} (Transaction Confirmed)", "status": "Pickup",
                        "assigned_staff": "Pending Scheduling Hub Allocation", "created_at": datetime.now().strftime("%m/%d/%y")
                    }
                    st.session_state.orders.append(new_order_record)
                    
                    st.session_state.notifications.append({
                        "text": f"New order successfully placed! Tracker ID: {unique_tracking_id}",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
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

    elif menu_selection == "💬 Messages Support Desk":
        st.markdown("## 💬 Direct Helpdesk Communications Central Queue")
        st.markdown("Text our management and administrative staff directly. Responses show up here instantly.")
        
        chat_input_column, chat_history_column = st.columns([1, 2], gap="medium")
        
        with chat_input_column:
            composed_message_text = st.text_area("Write your message to the Admin:", placeholder="Type question about packages, deliveries or pricing...")
            if st.button("✉️ Transmit Message Stream Payload", use_container_width=True):
                if composed_message_text:
                    st.session_state.messages.append({
                        "name": f"{user_record['name']} (Client)",
                        "message": composed_message_text,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Message dispatched to administrative terminal dashboard panels.")
                    st.rerun()
                    
        with chat_history_column:
            st.markdown("#### Live Communication History")
            for active_message in reversed(st.session_state.messages):
                if "Admin" in active_message["name"] or "SYSTEM" in active_message["name"]:
                    st.warning(f"🛠️ **{active_message['name']}** [{active_message['time']}]: {active_message['message']}")
                else:
                    st.info(f"👤 **{active_message['name']}** [{active_message['time']}]: {active_message['message']}")

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

# ==============================================================================
# 8. AUTHORIZED LAYER C: ADMINISTRATIVE HUB CONTROL ENGINE
# ==============================================================================
elif st.session_state.logged_in and active_role == "admin":
    
    total_customers_count = len([u for u in st.session_state.users.values() if u["role"] == "customer"])
    
    if menu_selection == "Main Operations Ledger":
        st.markdown("## ⚙️ Administration Engine Real-Time Process Control Dashboard")
        
        analytics_col_1, analytics_col_2, analytics_col_3 = st.columns(3)
        with analytics_col_1:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; color: #0f172a; border-left: 5px solid #10b981; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <span style="font-size: 28px;">👥</span>
                <h3 style="margin: 5px 0 0 0; font-weight: 800; color: #111827;">{total_customers_count} Registered Clients</h3>
                <p style="margin: 0; font-size: 12px; color: #6b7280;">Utilizing Application Solutions</p>
            </div>
            """, unsafe_allow_html=True)
        with analytics_col_2:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; color: #0f172a; border-left: 5px solid #2563eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <span style="font-size: 28px;">📦</span>
                <h3 style="margin: 5px 0 0 0; font-weight: 800; color: #111827;">{len(st.session_state.orders)} Orders</h3>
                <p style="margin: 0; font-size: 12px; color: #6b7280;">Total System Log Count</p>
            </div>
            """, unsafe_allow_html=True)
        with analytics_col_3:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; text-align: center; color: #0f172a; border-left: 5px solid #f59e0b; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <span style="font-size: 28px;">💬</span>
                <h3 style="margin: 5px 0 0 0; font-weight: 800; color: #111827;">{len(st.session_state.messages)} Logs</h3>
                <p style="margin: 0; font-size: 12px; color: #6b7280;">Interactions In Queue Desk</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
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
            st.dataframe(orders_dataframe.drop(columns=["Index Pointer"]), use_container_width=True, hide_index=True)
            
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
                old_status = st.session_state.orders[target_order_index]["status"]
                st.session_state.orders[target_order_index]["status"] = updated_workflow_stage
                st.session_state.orders[target_order_index]["assigned_staff"] = allocated_staff_asset
                
                tracking_id = st.session_state.orders[target_order_index]['tracking']
                st.session_state.notifications.append({
                    "text": f"Order {tracking_id} status changed from {old_status} to {updated_workflow_stage}!",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                st.success("Target workflow state configuration adjustments updated. Notification dispatched to client!")
                st.rerun()

        st.markdown("---")
        st.markdown("### 💬 Active Communication Matrix Hub (Responding to Clients)")
        chat_input_column, chat_history_column = st.columns([1, 2], gap="medium")
        
        with chat_input_column:
            composed_message_text = st.text_area("Write response message payload back to clients:", placeholder="Enter answer details here...")
            if st.button("Transmit Packet Matrix Payload To Chat Logs", use_container_width=True):
                if composed_message_text:
                    st.session_state.messages.append({
                        "name": "Theophilus (Admin)",
                        "message": composed_message_text,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.session_state.notifications.append({
                        "text": f"New message from support staff: '{composed_message_text[:40]}...'",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    st.success("Message loaded onto public stream channels successfully.")
                    st.rerun()
                    
        with chat_history_column:
            st.markdown("#### Message Streaming Framework Ledger Streams")
            for active_message in reversed(st.session_state.messages):
                if "Admin" in active_message["name"]:
                    st.warning(f"⚙️ **{active_message['name']}** [{active_message['time']}]: {active_message['message']}")
                else:
                    st.info(f"👤 **{active_message['name']}** [{active_message['time']}]: {active_message['message']}")

    elif menu_selection == "User Accounts Profiles":
        st.markdown("## 👥 Active Database Consumers Master Profiles Register Ledger")
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

    elif menu_selection == "Inventory & Billings":
        st.markdown("## 📊 Strategic Allocation Audits & Billing Balance Ledgers")
        inventory_graph_col, fiscal_card_col = st.columns(2)
        
        with inventory_graph_col:
            st.markdown("### Material Commodity Supply Reservoirs")
            inventory_dataframe = pd.DataFrame.from_dict(st.session_state.inventory, orient='index', columns=['Current Resource Level'])
            st.bar_chart(inventory_dataframe)
            
        with fiscal_card_col:
            st.markdown("### Central Aggregated Accounting Audited Summaries")
            gross_system_revenue = sum([order_record["cost"] for order_record in st.session_state.orders])
            st.markdown(f"""
            <div style="background: white; color: #0f172a; padding: 30px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #10b981;">
                <p style="margin: 0; font-size: 12px; color: #64748b; font-weight: bold; letter-spacing: 0.5px;">GROSS REVENUE FINANCIAL VALUE POOL</p>
                <h1 style="margin: 10px 0 25px 0; color: #10b981; font-size: 42px; font-weight: 800;">KES {gross_system_revenue:,.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

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
