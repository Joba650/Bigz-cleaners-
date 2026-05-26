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
            "name": "Alex Rodriguez",
            "phone": "0700000000",
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
    st.session_state.staff = ["Alex Chen", "Marix Mason", "John Doe", "Alex Rodriguez"]

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
            "payment_gateway": "M-Pesa Express", "status": "Drying", "assigned_staff": "Alex Rodriguez",
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
                                    st.session_state.current_email = login_email
                                    st.session_state.current_role = user["role"]
                                    st.rerun()
                            else:
                                st.error("Invalid password authentication handshake.")
                        else:
                            st.error("Profile identity mismatch or data entry empty.")
                            
            with signup_tab:
                st.markdown("<p style='color: #cbd5e1; font-weight: bold; margin-bottom: 15px;'>CREATE YOUR FREE ACCOUNT</p>", unsafe_allow_html=True)
                reg_role = st.selectbox("Assign Profile Context Target Blueprint:", ["Client / Consumer Account", "Admin / Production Staff"])
                
                with st.form("signup_panel_form"):
                    new_name = st.text_input("Full Signature Name")
                    new_phone = st.text_input("Phone Communication Line")
                    new_email = st.text_input("Email Account Address")
                    new_address = st.text_input("Primary Physical Delivery Location")
                    new_password = st.text_input("Set Custom Access Password", type="password")
                    
                    if st.form_submit_button("SUBMIT APPLICATION FILES", use_container_width=True):
                        if new_email in st.session_state.users:
                            st.error("Account token identifier already registered.")
                        elif not new_email or not new_password:
                            st.error("Required fields cannot remain blank.")
                        else:
                            assigned_role = "customer" if "Client" in reg_role else "admin"
                            is_verified = True if assigned_role == "admin" else False
                            
                            st.session_state.users[new_email] = {
                                "name": new_name, "phone": new_phone, "address": new_address,
                                "password": new_password, "role": assigned_role, "verified": is_verified,
                                "saved_cards": ["•••• •••• •••• 1111"],
                                "preferences": {"Detergent type": "Scented Organic", "Starched Shirts": "No Starch Treatment"}
                            }
                            if assigned_role == "customer":
                                st.session_state.pending_verification = new_email
                            else:
                                st.success("Administrative clearance granted! Log in via portal.")
                            st.rerun()

# =========================================
# LAYER B: AUTHENTICATED CLIENT DASHBOARDS
# =========================================
elif st.session_state.logged_in and user_role == "customer":
    
    if menu_selection == "Service Dashboard":
        st.markdown("## 🧺 Dashboard Access: Premium Laundry Catalog")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        for idx, s in enumerate(services):
            target_col = [col_c1, col_c2, col_c3][idx % 3]
            with target_col:
                st.markdown(f"""
                <div class="service-card">
                    <h3 style="margin: 0; color: #1e3a8a;">{s['name']}</h3>
                    <p style="margin: 5px 0; font-size: 14px; color: #64748b;">Processing Line: <b>{s['type']}</b></p>
                    <h4 style="margin: 10px 0 0 0; color: #10b981;">KES {s['price']} per {s['unit']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.markdown("## ➕ Initialize Custom Order Sequence Pipeline")
        
        with st.expander("Configure Flowchart Multi-Step Order Intake Engine", expanded=True):
            srv_type = st.radio("Step 1: Specify Operational Processing Pipeline Type", ["Wash & Fold", "Dry Clean"], horizontal=True)
            f_services = [s for s in services if s["type"] == srv_type]
            
            selected_s = st.selectbox("Step 2: Select Targeted System Package", [s["name"] for s in f_services])
            matched_s = next(s for s in services if s["name"] == selected_s)
            
            qty = st.number_input(f"Step 2.1: Quantity Selection ({matched_s['unit']})", min_value=1, value=1)
            total_cost = matched_s["price"] * qty
            
            col_t1, col_t2 = st.columns(2)
            p_date = col_t1.date_input("Step 3: Schedule Pickup Date Anchor")
            p_time = col_t2.time_input("Step 3.1: Select Fleet Scheduling Time Window")
            p_addr = st.text_input("Step 3.2: Logistic Route Destination Mapping", value=user_record.get("address", ""))
            
            st.markdown(f"### Total Pipeline Cost Matrix Evaluation: <span style='color:#10b981;'>KES {total_cost}</span>", unsafe_allow_html=True)
            p_gateway = st.selectbox("Step 4: Secure Transaction Gateway Routing Matrix", ["M-Pesa Express", "Secure Card Payment Gateway"])
            
            if st.button("💳 Proceed & Trigger Payment Engine Settlement", use_container_width=True):
                if not p_addr:
                    st.error("Route mapping field context validation required before checkout.")
                else:
                    tracking_code = "BIGZ-" + datetime.now().strftime("%H%M%S")
                    new_order = {
                        "tracking": tracking_code, "customer": user_record["name"], "email": user_email,
                        "service": selected_s, "quantity": f"{qty} {matched_s['unit']}", "cost": total_cost,
                        "pickup_logistics": f"{p_date} at {p_time}", "address": p_addr,
                        "payment_gateway": f"{p_gateway} (Transaction Confirmed)", "status": "Pickup",
                        "assigned_staff": "Pending Scheduling Hub Allocation", "created_at": datetime.now().strftime("%m/%d/%y")
                    }
                    st.session_state.orders.append(new_order)
                    st.balloons()
                    st.success(f"Processing Order Stream generated successfully! ID Token: {tracking_code}")
                    st.rerun()

        st.markdown("### Profile Manifest Active Tracking Vectors")
        c_orders = [o for o in st.session_state.orders if o["email"] == user_email]
        if not c_orders:
            st.caption("No real-time tracking loops running currently on this account configuration.")
        else:
            col_grid = st.columns(4)
            for idx, o in enumerate(c_orders):
                target_col = col_grid[idx % 4]
                with target_col:
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; color: black; margin-bottom: 15px;">
                        <span style="float: right; font-size: 11px; background: #dbeafe; color: #1e40af; padding: 2px 6px; border-radius: 8px; font-weight: bold;">{o['status']}</span>
                        <h4 style="margin: 0 0 5px 0; color: #1e3a8a;">{o['tracking']}</h4>
                        <p style="margin: 5px 0 0 0; font-size: 12px; color: #475569;">Package: {o['service']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif menu_selection == "My Profile Account":
        st.markdown("## 👤 Configuration Preferences & Profile Management")
        col_p1, col_p2 = st.columns([1.1, 0.9], gap="large")
        
        with col_p1:
            st.markdown("### Core Registration Storage Data")
            with st.form("profile_data_form"):
                e_name = st.text_input("Profile Display Name Entity", value=user_record["name"])
                e_phone = st.text_input("Active Communications Connection String", value=user_record["phone"])
                e_addr = st.text_area("Default Operational Delivery Address Log", value=user_record.get("address", ""))
                if st.form_submit_button("Commit Account Database Mutation"):
                    user_record["name"] = e_name
                    user_record["phone"] = e_phone
                    user_record["address"] = e_addr
                    st.success("Storage registers updated effectively across core systems.")
                    st.rerun()

        with col_p2:
            st.markdown("### Vault Storage Credit Methods Tokens")
            for card in user_record.get("saved_cards", []):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
                    <p style="margin: 0; font-size: 10px; opacity: 0.7; letter-spacing: 1px;">BIGZ GATEWAY WALLET INTEGRATION</p>
                    <h3 style="margin: 8px 0; letter-spacing: 3px;">{card}</h3>
                    <p style="margin: 0; font-size: 11px; text-align: right; opacity: 0.9;">SECURE SIGNATURE VERIFIED</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### System Formulation Metrics & Preferences")
            p_det = st.selectbox("Default Detergent Type Formula Profile", ["Scented Organic", "Hypoallergenic Neutral", "Heavy Stain-Fighter Extra"])
            p_starch = st.selectbox("Garment Stiffness Calibration Ratio", ["No Starch Treatment", "Medium Crispy Stiffness", "High Executive Starched Stiff"])
            if st.button("Overwrite Custom Configuration Maps"):
                user_record["preferences"]["Detergent type"] = p_det
                user_record["preferences"]["Starched Shirts"] = p_starch
                st.success("Preferences saved successfully.")

# =========================================
# LAYER C: AUTHENTICATED ADMINISTRATIVE HUB
# =========================================
elif st.session_state.logged_in and user_role == "admin":
    
    if menu_selection == "Main Operations Ledger":
        st.markdown("## ⚙️ Administration Engine Real-Time Process Dashboard")
        
        st.markdown("### 🔍 Enterprise Core System Service Tracking Pipeline")
        if not st.session_state.orders:
            st.info("System process logs contain zero running context objects currently.")
        else:
            matrix_ledger = []
            for idx, o in enumerate(st.session_state.orders):
                matrix_ledger.append({
                    "Index Pointer": idx,
                    "Order ID Vector": o["tracking"],
                    "Client Context": o["customer"],
                    "Processing Lifecycle Stage": o["status"],
                    "Deployed Fleet Asset": o["assigned_staff"],
                    "System Timestamp": o["created_at"]
                })
            df_ledger = pd.DataFrame(matrix_ledger)
            st.dataframe(df_ledger.drop(columns=["Index Pointer"]), use_container_width=True, hide_index=True)
            
            st.markdown("#### Production Workflow State Manipulation Unit")
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                t_idx = st.selectbox("Select Target Pipeline Execution ID Context", options=df_ledger["Index Pointer"], format_func=lambda x: f"Order #{st.session_state.orders[x]['tracking']} [{st.session_state.orders[x]['customer']}]")
            with col_a2:
                t_stage = st.selectbox("Advance Flowchart Execution Phase", ["Pickup", "Washing", "Drying", "Fold", "Ready for Delivery", "Delivered & Complete"])
            with col_a3:
                t_staff = st.selectbox("Re-assign Operational Fleet Worker Unit", st.session_state.staff)
                
            if st.button("Commit Production Modification Instructions Override", use_container_width=True):
                st.session_state.orders[t_idx]["status"] = t_stage
                st.session_state.orders[t_idx]["assigned_staff"] = t_staff
                
                # Automated tracking message engine mock simulation
                st.session_state.messages.append({
                    "name": "SYSTEM PRODUCTION AUTOMATION BOT",
                    "message": f"Order Framework Context Update Notification [{st.session_state.orders[t_idx]['tracking']}]: Your package processing stage moved cleanly to '{t_stage}' under supervision of tracking courier asset: {t_staff}.",
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                st.success("Target workflow state configurations adjusted in centralized operational logs.")
                st.rerun()

        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("### Distribution Mapping Dispatch Vectors Matrix")
            st.info("🌐 Core GPS Mapping Active. Routing links verified for 4 active logistical worker nodes.")
            st.markdown("""
            <div style="background: white; padding: 18px; border-radius: 12px; color: black; border-left: 5px solid #a855f7;">
                <b>Active Shift Route Dispatches Checklist:</b><br>
                • Alex Chen — Route Segment Northwest Alpha (08:00 - 12:00)<br>
                • Marix Mason — Route Segment Central Core Cargo Zone (13:00 - 17:00)
            </div>
            """, unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("### Expand Core Product Catalog Framework")
            with st.form("catalog_append_form"):
                a_name = st.text_input("New Core Service Label")
                a_price = st.number_input("Rate Calculation Standard (KES)", min_value=10, value=150)
                a_unit = st.selectbox("Unit Metric Scale", ["KG", "Piece", "Pair", "Suit"])
                a_cat = st.selectbox("Pipeline System Assignment Type", ["Wash & Fold", "Dry Clean"])
                if st.form_submit_button("Append Service Package Vector To Core Arrays"):
                    if a_name:
                        services.append({"name": a_name, "price": a_price, "unit": a_unit, "type": a_cat})
                        st.success(f"Production matrix catalog expanded: Added entry '{a_name}'")
                    else:
                        st.error("Operation validation aborted. Name parameters missing definitions.")

    elif menu_selection == "User Accounts Profiles":
        st.markdown("## 👥 Active Database Consumers Master Profiles Register Ledger")
        records_pool = []
        for em, u in st.session_state.users.items():
            if u["role"] == "customer":
                records_pool.append({
                    "Client Name Master Identifier": u["name"],
                    "Mobile Link Address String": u["phone"],
                    "Identity Clearance Allocation Key": em,
                    "Security Verification Clearance Flags": "VERIFIED ACCESS ACTIVE" if u.get("verified", False) else "LOCKED LOOP PENDING"
                })
        if records_pool:
            st.table(pd.DataFrame(records_pool))
        else:
            st.caption("No registered records located in dynamic volatility system arrays.")

    elif menu_selection == "Inventory & Billings":
        st.markdown("## 📊 Strategic Allocation Audits & Billing Balance Ledgers")
        col_an1, col_an2 = st.columns(2)
        
        with col_an1:
            st.markdown("### Material Commodity Supply Reservoirs")
            inv_df = pd.DataFrame.from_dict(st.session_state.inventory, orient='index', columns=['Current Resource Level'])
            st.bar_chart(inv_df)
            
            st.markdown("#### Adjust Supply Levels")
            for asset, quantity in st.session_state.inventory.items():
                new_qty = st.number_input(f"Stock level: {asset}", min_value=0, value=int(quantity), key=f"inv_input_{asset}")
                st.session_state.inventory[asset] = new_qty
            
        with col_an2:
            st.markdown("### Central Aggregated Accounting Audited Summaries")
            gross_revenue = sum([o["cost"] for o in st.session_state.orders])
            st.markdown(f"""
            <div style="background: white; color: #0f172a; padding: 30px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 12px; color: #64748b; font-weight: bold; letter-spacing: 0.5px;">GROSS REVENUE FINANCIAL VALUE POOL</p>
                <h1 style="margin: 10px 0 25px 0; color: #10b981; font-size: 42px; font-weight: 800;">KES {gross_revenue:,.2f}</h1>
                <hr style="border-color: #f1f5f9; margin: 15px 0;">
                <p style="font-size: 13px; margin: 6px 0;"><b>Secure Gateway Transaction Audits:</b> Systems Functioning Nominally</p>
                <p style="font-size: 13px; margin: 6px 0;"><b>Outstanding Remittance Liabilities Queue:</b> KES 0.00 Cleared Balance</p>
            </div>
            """, unsafe_allow_html=True)

# =========================================
# UNIVERSAL LOGICAL COMPONENT: SUPPORT CORE CHAT
# =========================================
if st.session_state.logged_in:
    if (user_role == "customer" and menu_selection == "Support Messaging Desk") or (user_role == "admin" and menu_selection == "Main Operations Ledger"):
        st.markdown("---")
        st.markdown("## 💬 Centralized Communications Network Support Routing Hub")
        col_ch1, col_ch2 = st.columns([1, 2], gap="medium")
        
        with col_ch1:
            c_msg = st.text_area("Compose System Operational Message Dispatch Package:", placeholder="Enter your inquiry or logging issue parameters here...")
            if st.button("Transmit Packet Matrix Payload To Central Queue", use_container_width=True):
                if c_msg:
                    st.session_state.messages.append({
                        "name": user_record["name"],
                        "message": c_msg,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.success("Data stream payload safely transmitted.")
                    st.rerun()
                    
        with col_ch2:
            st.markdown("#### Message Streaming Framework Ledger Streams")
            if not st.session_state.messages:
                st.caption("Active operational log chat channels contain zero traffic records.")
            else:
                for msg in reversed(st.session_state.messages):
                    st.info(f"🕒 [{msg['time']}] **{msg['name']}**: {msg['message']}")

# =========================================
# SYSTEM CORE FOOTER
# =========================================
st.markdown("""
<div class="footer">
🧺 BIGZ CLEANERS <br>
System Compliant Blueprint Core — Trusted Production Engine Framework Terminal <br><br>
© 2026 BIGZ CLEANERS
</div>
""", unsafe_allow_html=True)
