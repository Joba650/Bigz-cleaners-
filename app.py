import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. PLATFORM CONFIGURATION & CONSTANTS
# ==============================================================================
DATABASE_FILE_PATH = "users_db.json"

st.set_page_config(
    page_title="BIGZ CLEANERS AI",
    page_icon="🧺",
    layout="wide"
)

# Active service catalog matching the tap selection requirements
if "laundry_service_catalog" not in st.session_state:
    st.session_state.laundry_service_catalog = [
        {"id": "srv_wash_fold", "name": "Laundry Washing", "price": 200.0, "unit": "7KG", "type": "Wash & Fold", "img": "https://images.unsplash.com/photo-1545173168-9f1947eebd01?w=500&auto=format&fit=crop&q=60", "desc": "Premium automated wash, crisp structural tumble fold, packed by batch."},
        {"id": "srv_carpet", "name": "Carpet Cleaning", "price": 150.0, "unit": "sqm", "type": "Specialty Clean", "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500&auto=format&fit=crop&q=60", "desc": "Deep fiber extraction therapy, sanitizing wash, high-heat air dry."},
        {"id": "srv_duvet", "name": "Duvet Cleaning", "price": 500.0, "unit": "Piece", "type": "Dry Clean", "img": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=500&auto=format&fit=crop&q=60", "desc": "Anti-allergen processing cycle optimized for heavy premium bedding comfort."}
    ]

# ==============================================================================
# 2. PERSISTENT LOCAL STORAGE ENGINE 
# ==============================================================================
def load_user_database() -> dict:
    default_records = {
        "admin@bigz.com": {"name": "Theophilus Mose", "phone": "0116993710", "password": "admin123", "role": "admin", "verified": True},
        "sarachen@gmail.com": {
            "name": "Sarah Chen", "phone": "(03) 236-6500", "password": "password123", "role": "customer",
            "address": "123 Saved Address From Street, West, Buil, 4003", "verified": True,
            "wallet_points": 250, "saved_cards": ["•••• •••• •••• 4321"],
            "preferences": {"Detergent": "Normal", "Starched Shirts": "Medium"}
        }
    }
    if not os.path.exists(DATABASE_FILE_PATH):
        with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(default_records, f, indent=4)
        return default_records
    try:
        with open(DATABASE_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default_records

def save_user_profile(email_key: str, profile_data: dict) -> None:
    current_db = load_user_database()
    current_db[email_key.lower().strip()] = profile_data
    with open(DATABASE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(current_db, f, indent=4)

st.session_state.users = load_user_database()

# ==============================================================================
# 3. RUNTIME MEMORY STATE INITIALIZATION
# ==============================================================================
state_defaults = {
    "logged_in": False, "current_user": "", "current_email": "", "current_role": "",
    "selected_service_id": "srv_wash_fold",
    "delivery_riders": [
        {"name": "David", "location": "Nakuru Town", "orders": 4, "status": "On Delivery"},
        {"name": "Kelvin", "location": "Njoro", "orders": 2, "status": "Pickup"}
    ],
    "notifications": [
        "Order #1234 delayed by 15 mins",
        "Payment confirmed via secure gateway"
    ],
    "recent_orders": [
        {"id": "#1234", "customer": "Sarah Chen", "service": "Laundry Washing", "status": "Washing"},
        {"id": "#1235", "customer": "Brian Mwangi", "service": "Duvet Cleaning", "status": "Ready"}
    ],
    "staff_activity": [
        {"name": "John", "role": "Pickup Rider", "active": True},
        {"name": "Mercy", "role": "Ironing", "active": True}
    ],
    "orders": [
        {"tracking": "1234", "customer": "Sarah Chen", "email": "sarachen@gmail.com", "service": "Laundry Washing", "quantity": "1 Batch", "bag_size": "Medium", "detergent": "Normal", "cost": 200.0, "pickup_logistics": "Immediate", "address": "123 Saved Address From Street", "payment_gateway": "Secure Card", "status": "Washing", "assigned_staff": "John", "created_at": "2026-05-28"}
    ]
}
for key, val in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ==============================================================================
# 4. DESIGN FRAMEWORK (CSS INJECTION - SAFELY ENCLOSED IN STRINGS)
# ==============================================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e3a8a, #0284c7);
        background-attachment: fixed;
    }
    .dashboard-container {
        background-color: #f8fafc;
        border-radius: 16px;
        padding: 24px;
        color: #1e293b;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .dashboard-header {
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px;
    }
    .service-tap-box {
        background-color: white;
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        margin-bottom: 15px;
        color: #1e293b;
    }
    .service-tap-box-selected {
        background-color: #f0f9ff;
        border-color: #0284c7;
        box-shadow: 0 0 0 3px rgba(2,132,199,0.3);
    }
    .mobile-frame {
        background-color: #f8fafc;
        border-radius: 32px;
        padding: 0px;
        color: #1e293b;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        max-width: 450px;
        margin: 0 auto;
        overflow: hidden;
        border: 4px solid #cbd5e1;
    }
    .mobile-header {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        padding: 24px;
    }
    .stat-card {
        background-color: white;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .data-card {
        background-color: white;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
    .status-badge-blue {
        background-color: #dbeafe;
        color: #1d4ed8;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }
    .footer { 
        text-align: center; 
        color: #94a3b8; 
        padding: 30px 0; 
        margin-top: 40px; 
        border-top: 1px solid rgba(255,255,255,0.1); 
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. SIDEBAR MANAGEMENT SYSTEM
# ==============================================================================
st.sidebar.title("🧺 BIGZ CLEANERS")

if st.session_state.logged_in:
    u_email = st.session_state.current_email
    user_record = st.session_state.users.get(u_email)
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 10px 0;">
        <h3 style="color: white; margin: 0;">{user_record['name']}</h3>
        <p style="color: #cbd5e1; font-size: 12px; margin: 0;">{st.session_state.current_role.upper()} HUB</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.current_role == "customer":
        menu = st.sidebar.radio("Navigation Menu", ["Client Dashboard", "My Profile Settings"])
    else:
        menu = st.sidebar.radio("Admin Menu", ["Operations Dashboard", "System Database Ledger"])

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Terminate Session", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ==============================================================================
# 6. SIGN-IN PORTAL / ACCESS HUB
# ==============================================================================
if not st.session_state.logged_in:
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown("<h1 style='color: white; font-size: 48px; margin-top: 50px;'>BIGZ CLEANERS AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #cbd5e1; font-size: 18px;'>High-Performance Automated Fabric Care Infrastructure Engine.</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("### Secure Gateway Login")
            email_input = st.text_input("Account Email", value="sarachen@gmail.com")
            pass_input = st.text_input("Password", type="password", value="password123")
            if st.form_submit_button("Authenticate"):
                clean_email = email_input.lower().strip()
                if clean_email in st.session_state.users and st.session_state.users[clean_email]["password"] == pass_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = st.session_state.users[clean_email]["name"]
                    st.session_state.current_email = clean_email
                    st.session_state.current_role = st.session_state.users[clean_email]["role"]
                    st.rerun()
                else:
                    st.error("Invalid secure matching credentials.")

# ==============================================================================
# 7. CLIENT INTERFACES (MATCHING THE MOCKUPS EXACTLY)
# ==============================================================================
elif st.session_state.logged_in and st.session_state.current_role == "customer":

    if menu == "Client Dashboard":
        st.markdown("<h1 style='color: white;'>Client Dashboard Hub 🧺</h1>", unsafe_allow_html=True)
        
        col_main, col_side = st.columns([2, 1], gap="medium")
        
        with col_main:
            # Quick Schedule Block matching Mockup #1
            st.markdown("""
            <div class="dashboard-container">
                <h3 class="dashboard-header">📅 Quick Schedule Service Pipeline</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Tap catalog interface
            st.markdown("##### 1. Select Active Service Layer Category")
            catalog_cols = st.columns(3)
            for idx, srv in enumerate(st.session_state.laundry_service_catalog):
                with catalog_cols[idx]:
                    selected_flag = st.session_state.selected_service_id == srv["id"]
                    box_class = "service-tap-box-selected" if selected_flag else ""
                    st.markdown(f"""
                    <div class="service-tap-box {box_class}">
                        <img src="{srv['img']}" style="width:100%; height:110px; object-fit:cover;" />
                        <div style="padding: 10px;">
                            <h5 style="margin:0; font-weight:bold; color:#1e3a8a;">{srv['name']}</h5>
                            <span style="font-size:13px; color:#0284c7; font-weight:bold;">KES {srv['price']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Pick {srv['name']}", key=f"select_srv_{srv['id']}", use_container_width=True):
                        st.session_state.selected_service_id = srv["id"]
                        st.rerun()

            active_srv = next(s for s in st.session_state.laundry_service_catalog if s["id"] == st.session_state.selected_service_id)
            
            # Booking Form
            with st.form("quick_schedule_form"):
                st.markdown(f"**Booking Parameters for: {active_srv['name']}**")
                c_f1, c_f2 = st.columns(2)
                p_date = c_f1.date_input("Pickup Date")
                d_date = c_f2.date_input("Expected Delivery Date")
                p_time = st.selectbox("Preferred Time Window", ["7:00 AM - 10:00 AM", "12:00 PM - 3:00 PM", "6:00 PM - 9:00 PM"])
                
                if st.form_submit_button("Proceed to Payment & Confirm Delivery"):
                    new_order = {
                        "tracking": str(datetime.now().strftime("%M%S")),
                        "customer": user_record["name"], "email": st.session_state.current_email,
                        "service": active_srv["name"], "quantity": "1 Batch", "bag_size": "Standard",
                        "detergent": user_record["preferences"].get("Detergent", "Normal"), 
                        "cost": active_srv["price"], "pickup_logistics": f"{p_date} @ {p_time}",
                        "address": user_record["address"], "payment_gateway": "Secure Card",
                        "status": "Washing", "assigned_staff": "David", "created_at": "2026-05-28"
                    }
                    st.session_state.orders.append(new_order)
                    st.success("Order dispatched directly into the system pipeline array.")
                    st.rerun()

        with col_side:
            # Active Orders Block matching Mockup #1
            st.markdown("""
            <div class="dashboard-container">
                <h3 class="dashboard-header">📦 Active Orders</h3>
            </div>
            """, unsafe_allow_html=True)
            
            client_orders = [o for o in st.session_state.orders if o["email"] == st.session_state.current_email]
            if not client_orders:
                st.caption("No running operations logged.")
            else:
                for order in client_orders:
                    st.markdown(f"""
                    <div class="data-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <b>Order #{order['tracking']}</b>
                            <span class="status-badge-blue">{order['status']}</span>
                        </div>
                        <p style="margin:4px 0 0 0; font-size:13px; color:#64748b;">Service: {order['service']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif menu == "My Profile Settings":
        st.markdown("<h1 style='color: white;'>User Profile Hub 👤</h1>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns([1.5, 1.5], gap="medium")
        
        with col_p1:
            st.markdown("""
            <div class="dashboard-container">
                <h3 class="dashboard-header">👤 Account Information Data</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("profile_update_form"):
                u_name = st.text_input("Name Reference", value=user_record["name"])
                u_phone = st.text_input("Primary Contact Line", value=user_record["phone"])
                u_address = st.text_input("Verified Delivery Address", value=user_record["address"])
                
                if st.form_submit_button("Update Core Profile Information"):
                    user_record["name"] = u_name
                    user_record["phone"] = u_phone
                    user_record["address"] = u_address
                    save_user_profile(st.session_state.current_email, user_record)
                    st.success("Profile saved successfully.")
                    st.rerun()

        with col_p2:
            st.markdown("""
            <div class="dashboard-container">
                <h3 class="dashboard-header">⚙️ System Wash Preferences</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("preferences_form"):
                det_type = st.selectbox("Detergent Formula Type", ["Normal Pro-Clean", "Organic Eco-Scented", "Hypoallergenic Sensitive"])
                starch_level = st.selectbox("Starched Shirts Treatment Level", ["No Starch Treatment", "Medium Crispy Stiffness", "Maximum Heavy Armor"])
                
                if st.form_submit_button("Lock Preferences Settings"):
                    user_record["preferences"] = {"Detergent": det_type, "Starched Shirts": starch_level}
                    save_user_profile(st.session_state.current_email, user_record)
                    st.success("Washing configuration metrics locked.")
                    st.rerun()

# ==============================================================================
# 8. MASTER ADMINISTRATIVE HUB VIEW (WITH REAL-TIME ANALYTICS PLOTS)
# ==============================================================================
elif st.session_state.logged_in and st.session_state.current_role == "admin":
    
    if menu == "Operations Dashboard":
        st.markdown("<h1 style='color: white;'>Administrative Operations Command Terminal</h1>", unsafe_allow_html=True)
        
        col_mock, col_charts = st.columns([1.1, 1.9], gap="large")
        
        with col_mock:
            st.markdown('<div class="mobile-frame">', unsafe_allow_html=True)
            
            # --- HEADER BLOCK ---
            st.markdown(f"""
            <div class="mobile-header">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="color: white; font-size: 22px; font-weight: bold; margin: 0;">Bigz Cleaners</h2>
                        <p style="color: rgba(255,255,255,0.8); font-size: 13px; margin: 2px 0 0 0;">Admin Control Framework</p>
                    </div>
                    <div style="width:40px; height:40px; background:rgba(255,255,255,0.2); border-radius:50%; text-align:center; line-height:40px; font-weight:bold; color:white;">A</div>
                </div>
                <div style="background-color: rgba(255,255,255,0.1); border-radius: 12px; padding: 12px; margin-top: 15px;">
                    <p style="margin: 0; font-size: 13px; color: white; opacity:0.9;">Today's Accrued Revenue Gross</p>
                    <h2 style="margin: 2px 0 0 0; color: white; font-size: 24px; font-weight: 800;">KES 17,500</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- STATS ---
            st.markdown("<div style='padding: 16px;'>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            g1.markdown("""<div class="stat-card"><small style="color:#64748b;">Orders Today</small><h4 style="margin:4px 0; font-weight:bold;">48</h4></div>""", unsafe_allow_html=True)
            g2.markdown("""<div class="stat-card"><small style="color:#64748b;">Active Riders</small><h4 style="margin:4px 0; font-weight:bold;">2 Live</h4></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # --- RECENT ENTRIES ---
            st.markdown("<div style='padding: 0 16px;'><h4 style='font-size:16px; font-weight:bold; margin-bottom:8px;'>Recent Pipeline Entries</h4></div>", unsafe_allow_html=True)
            st.markdown("<div style='padding: 0 16px;'>", unsafe_allow_html=True)
            for r_order in st.session_state.recent_orders:
                st.markdown(f"""
                <div class="data-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b>{r_order['id']} - {r_order['customer']}</b>
                        <span class="status-badge-blue">{r_order['status']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # --- NOTIFICATIONS BLOCK ---
            st.markdown("<div style='padding: 12px 16px;'><h4 style='font-size:16px; font-weight:bold; margin-bottom:8px;'>System Notifications</h4></div>", unsafe_allow_html=True)
            st.markdown("<div style='padding: 0 16px;'>", unsafe_allow_html=True)
            for item in st.session_state.notifications:
                st.markdown(f"""<div style="background:#fff7ed; color:#c2410c; border:1px solid #ffedd5; padding:10px; border-radius:8px; font-size:12px; margin-bottom:8px;">⚠️ {item}</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with col_charts:
            st.markdown("""<div style="background-color:rgba(255,255,255,0.08); padding:20px; border-radius:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom:20px;">
                <h3 style="color:white; margin:0;">📊 Real-Time Process Dashboard Charts</h3>
                <p style="color:#94a3b8; font-size:13px; margin:0;">High-fidelity graphical layouts generated dynamically from active data frames.</p>
            </div>""", unsafe_allow_html=True)
            
            df = pd.DataFrame(st.session_state.orders)
            
            # Display charts
            st.markdown("<h5 style='color:white;'>Pipeline Status Stage Distributions</h5>", unsafe_allow_html=True)
            st.bar_chart(df['status'].value_counts(), use_container_width=True)
            
            st.markdown("<h5 style='color:white;'>Service Volume Revenue Shares</h5>", unsafe_allow_html=True)
            st.pie_chart(df, values='cost', names='service', use_container_width=True)

    elif menu == "System Database Ledger":
        st.markdown("## 📊 Active Operational Pipeline Database Engine")
        
        df_ledger = pd.DataFrame(st.session_state.orders)
        st.dataframe(df_ledger[["tracking", "customer", "service", "cost", "status", "assigned_staff"]], use_container_width=True, hide_index=True)
        
        st.markdown("### ⚙️ Direct Status Node Modifications Override Panel")
        with st.form("override_form"):
            t_idx = st.selectbox("Select Target Pipeline Entry Code Context", options=range(len(st.session_state.orders)), format_func=lambda x: f"Order ID #{st.session_state.orders[x]['tracking']} - {st.session_state.orders[x]['customer']}")
            c_s1, c_s2 = st.columns(2)
            n_status = c_s1.selectbox("New Target Status Node", ["Received", "Washing", "Drying", "Ironing", "Out for Delivery", "Delivered & Complete"])
            n_rider = c_s2.selectbox("Assign Courier Node Link", ["David", "Kelvin", "John", "Unassigned Pool"])
            
            if st.form_submit_button("Commit Changes to Core Datastore Structure"):
                st.session_state.orders[t_idx]["status"] = n_status
                st.session_state.orders[t_idx]["assigned_staff"] = n_rider
                st.success("Pipeline array changes successfully applied.")
                st.rerun()

# ==============================================================================
# 9. FOOTER BASE LAYERS
# ==============================================================================
st.markdown("""
<div class="footer">
    🧺 BIGZ CLEANERS AI LABS <br>
    System Compliant Blueprint Core — Production Secure Operational Layer <br>
    © 2026 BIGZ CLEANERS
</div>
""", unsafe_allow_html=True)
