import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 0. CORE CONFIGURATION & ARCHITECTURE SETUP
# ==========================================
st.set_page_config(
    page_title="Bigz Cleaners Enterprise", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize live pricing matrix in system memory
if "current_rates" not in st.session_state:
    st.session_state.current_rates = {
        "clothes_rate": 200,
        "carpet_rate": 150,
        "duvet_rate": 500
    }

# Simulate Persistent Database Tier
if "mock_db_users" not in st.session_state:
    st.session_state.mock_db_users = {
        "JL-111111": {"name": "Admin Chief", "role": "Admin", "pass": "admin123"},
        "JL-222222": {"name": "Rider Express", "role": "Rider", "pass": "rider123"},
        "JL-333333": {"name": "Kamau Njoro", "role": "Customer", "pass": "customer123"}
    }

if "mock_db_orders" not in st.session_state:
    st.session_state.mock_db_orders = [
        {"Order ID": "ORD-4821", "User Tag": "JL-333333", "Rider": "JL-222222", "Clothes (Kg)": 14, "Carpets (SqIn)": 0, "Duvets": 1, "Cost": 900, "Status": "Washing", "Location": "Njoro, Ngondu Court", "Date": "2026-05-29"},
        {"Order ID": "ORD-8829", "User Tag": "JL-333333", "Rider": "None", "Clothes (Kg)": 0, "Carpets (SqIn)": 10, "Duvets": 0, "Cost": 1500, "Status": "Pickup Requested", "Location": "Njoro Market, Block B", "Date": "2026-05-30"}
    ]

if "user_session" not in st.session_state:
    st.session_state.user_session = None

# ==========================================
# 1. DESIGN SPECIFICATION: SAFE TYPOGRAPHY
# ==========================================
st.title("BIGZ CLEANERS ENTERPRISE")
st.subheader("Integrated Multi-Tenant Logistics & Textile Care Platform")
st.divider()

# ==========================================
# 2. GLOBAL ROLE-BASED ACCESS CONTROLLER
# ==========================================
if not st.session_state.user_session:
    login_card, register_card = st.tabs(["Secure Corporate Portal Access", "Establish New Enterprise Account"])
    
    with register_card:
        st.write("### Client Onboarding Workspace")
        reg_name = st.text_input("Full Official Registration Name")
        reg_phone = st.text_input("Mobile Routing Terminal Number (M-Pesa Vector)")
        reg_pass = st.text_input("Set Structural Access Phrase", type="password")
        
        if st.button("Provisional Account Activation", use_container_width=True):
            if reg_name and reg_phone and reg_pass:
                generated_tag = f"JL-{random.randint(100000, 999999)}"
                st.session_state.mock_db_users[generated_tag] = {"name": reg_name, "role": "Customer", "pass": reg_pass}
                st.balloons()
                st.success(f"Account Initialized! System Tracking Tag Assigned: {generated_tag}")
                st.info("Log in using this structural tracking tag on the adjacent panel.")
            else:
                st.error("Operation halted: All authentication structures must be specified.")

    with login_card:
        st.write("### System Credentials Handshake")
        input_tag = st.text_input("Enter Structural Tracking Tag (e.g., JL-XXXXXX)").strip().upper()
        input_pass = st.text_input("System Entry Security Key", type="password")
        
        if st.button("Authorize Core Connectivity", use_container_width=True):
            if input_tag in st.session_state.mock_db_users and st.session_state.mock_db_users[input_tag]["pass"] == input_pass:
                user_data = st.session_state.mock_db_users[input_tag]
                st.session_state.user_session = {"tag": input_tag, "name": user_data["name"], "role": user_data["role"]}
                st.toast(f"Session established for profile: {user_data['name']}")
                st.rerun()
            else:
                st.error("Authentication handshake failed: Security metrics mismatch.")

# ==========================================
# 3. INTERFACE DEPENDENCY: ROUTING SEPARATION
# ==========================================
else:
    session = st.session_state.user_session
    rates = st.session_state.current_rates
    
    # Top Status Enterprise Communication Bar
    col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
    col_s1.write(f"Authorized Session: {session['name']} | Status: Online")
    col_s2.write(f"Access Level: {session['role']}")
    if col_s3.button("Terminate Secure Session", use_container_width=True):
        st.session_state.user_session = None
        st.rerun()
    st.divider()

    # ------------------------------------------
    # ARCHITECTURE CONTEXT A: CUSTOMER DASHBOARD
    # ------------------------------------------
    if session["role"] == "Customer":
        c_tab1, c_tab2, c_tab3 = st.tabs(["Dispatch Request Engine", "Real-Time Tracking & History", "Live Rates & Financials"])
        
        with c_tab3:
            st.write("### Dynamic Operational Rates")
            rate_df = pd.DataFrame({
                "Service Classification": ["Fabric Laundering", "Deep Carpet Restoration", "Heavy Duvets & Bedding", "Standard Pressing / Ironing"],
                "Base Valuation Matrix": [f"KES {rates['clothes_rate']} per 7 Kg load", f"KES {rates['carpet_rate']} per sq. inch", f"KES {rates['duvet_rate']} fixed unit rate", "Service Not Offered (N/A)"]
            })
            st.table(rate_df)
            
        with c_tab1:
            st.write("### Logistics Configuration Entry")
            with st.form("customer_order_form"):
                col_i1, col_i2, col_i3 = st.columns(3)
                v_clothes = col_i1.number_input("Fabric Volume (7 Kg Machine Loads)", min_value=0, step=1)
                v_carpet = col_i2.number_input("Carpet Metric Areas (Sq. Inches)", min_value=0, step=1)
                v_duvet = col_i3.number_input("Duvet Allocation Count", min_value=0, step=1)
                
                loc_txt = st.text_area("Detailed Fulfillment Coordinates / Gate / Apartment Number")
                target_date = st.date_input("Scheduled Logistics Window", min_value=datetime.today())
                
                # Dynamic Pricing Calculations
                base_calc = (v_clothes * rates["clothes_rate"]) + (v_carpet * rates["carpet_rate"]) + (v_duvet * rates["duvet_rate"])
                rush_surcharge = 150 if st.checkbox("Elevate to Express Rush Processing (+ KES 150)") else 0
                gross_valuation = base_calc + rush_surcharge
                
                st.write(f"### Total Statement Computation: KES {gross_valuation:,}")
                
                if st.form_submit_button("Authorize Logistics Pipeline Allocation"):
                    if gross_valuation == 0:
                        st.error("Operational processing parameters cannot evaluate to zero volumes.")
                    elif not loc_txt:
                        st.error("Logistics drop points must be explicitly articulated.")
                    else:
                        new_order_id = f"ORD-{random.randint(1000, 9999)}"
                        st.session_state.mock_db_orders.append({
                            "Order ID": new_order_id, "User Tag": session["tag"], "Rider": "None",
                            "Clothes (Kg)": v_clothes*7, "Carpets (SqIn)": v_carpet, "Duvets": v_duvet,
                            "Cost": gross_valuation, "Status": "Pickup Requested", "Location": loc_txt, "Date": str(target_date)
                        })
                        st.balloons()
                        st.success(f"Invoice Generated: {new_order_id} is registered to your Tag: {session['tag']}")

        with c_tab2:
            st.write("### Active Tracking Profiles")
            cust_orders = [o for o in st.session_state.mock_db_orders if o["User Tag"] == session["tag"]]
            
            if not cust_orders:
                st.info("Zero active system logs identified for current profile.")
            for o in cust_orders:
                st.write(f"#### Tracking Identifier: {o['Order ID']}")
                
                status_map = ["Pickup Requested", "Rider Assigned", "Washing", "Drying", "Out for Delivery", "Delivered"]
                curr_idx = status_map.index(o["Status"])
                
                progress_bar_val = (curr_idx + 1) / len(status_map)
                st.progress(progress_bar_val)
                
                tracker_line = ""
                for idx, step in enumerate(status_map):
                    if idx < curr_idx: tracker_line += f"~~{step}~~ -> "
                    elif idx == curr_idx: tracker_line += f"**{step}** -> "
                    else: tracker_line += f"{step} -> "
                st.write(tracker_line.rstrip(" -> "))
                
                st.write(f"Cost: KES {o['Cost']} | Location: {o['Location']}")
                st.divider()

    # ------------------------------------------
    # ARCHITECTURE CONTEXT B: COURIER RIDER PANEL
    # ------------------------------------------
    elif session["role"] == "Rider":
        st.write("### Assigned Logistics Routing Manifest")
        rider_jobs = [o for o in st.session_state.mock_db_orders if o["Rider"] == session["tag"]]
        unassigned_jobs = [o for o in st.session_state.mock_db_orders if o["Rider"] == "None"]
        
        r_tab1, r_tab2 = st.tabs(["Open Manifest Pipeline", "Available General Freight Market"])
        
        with r_tab1:
            if not rider_jobs:
                st.info("Zero logistics lines locked to your profile currently.")
            for o in rider_jobs:
                st.write(f"### Job {o['Order ID']}")
                st.write(f"Destination: {o['Location']} | Total: KES {o['Cost']}")
                new_stat = st.selectbox("Modify Status Node", ["Rider Assigned", "Washing", "Drying", "Out for Delivery", "Delivered"], key=o["Order ID"])
                if st.button("Update Ledger Link", key="btn_"+o["Order ID"]):
                    o["Status"] = new_stat
                    st.success("Logistics tracking line synchronized.")
                    st.rerun()
                st.divider()
                        
        with r_tab2:
            if not unassigned_jobs:
                st.info("Zero unassigned packages available in logistics queues.")
            for o in unassigned_jobs:
                st.write(f"Order: {o['Order ID']} - Route: {o['Location']} (Value: KES {o['Cost']})")
                if st.button("Claim Route Access Contract", key="claim_"+o["Order ID"]):
                    o["Rider"] = session["tag"]
                    o["Status"] = "Rider Assigned"
                    st.success("Manifest tracking path assigned.")
                    st.rerun()

    # ------------------------------------------
    # ARCHITECTURE CONTEXT C: ADMINISTRATIVE DASHBOARD
    # ------------------------------------------
    elif session["role"] in ["Admin", "Super Admin"]:
        adm_tab1, adm_tab2 = st.tabs(["Business Performance", "System Price Control Center"])
        
        with adm_tab1:
            st.write("## Executive Strategic Analytics Matrix")
            df_all = pd.DataFrame(st.session_state.mock_db_orders)
            total_rev = df_all["Cost"].sum() if not df_all.empty else 0
            total_jobs = len(df_all)
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Gross Invoices", f"KES {total_rev:,}")
            col_m2.metric("Pipeline Log Count", f"{total_jobs} Requests")
            col_m3.metric("Active System Footprint", f"{len(st.session_state.mock_db_users)} Users")
                
            st.divider()
            
            if not df_all.empty:
                st.write("### Revenue Velocity Analysis")
                fig = px.bar(df_all, x="Date", y="Cost", color="Status", title="Financial Freight Output Logs per Window", barmode="group")
                st.plotly_chart(fig, use_container_width=True)
                
            st.write("### Active Freight Ledger Master Core Table")
            st.dataframe(df_all, use_container_width=True)
            
            st.write("### Operational Asset Levels (Chemical Monitoring)")
            col_ch1, col_ch2, col_ch3 = st.columns(3)
            col_ch1.metric("Industrial Detergent Fluid", "134.5 Liters", delta="-4.2L")
            col_ch2.metric("Premium Conditioning Softener", "65.0 Liters", delta="-1.5L")
            col_ch3.metric("Concentrated Spot Agent", "22.1 Kg", delta="Stable")

        with adm_tab2:
            st.write("## Adjust Global System Pricing Configuration")
            st.write("Modifying these variables alters pricing structures across all customer portals instantly.")
            
            with st.form("price_control_form"):
                col_p1, col_p2, col_p3 = st.columns(3)
                
                new_clothes = col_p1.number_input("Set Clothes Rate (per 7kg load)", min_value=0, value=st.session_state.current_rates["clothes_rate"])
                new_carpet = col_p2.number_input("Set Carpet Rate (per Sq. Inch)", min_value=0, value=st.session_state.current_rates["carpet_rate"])
                new_duvet = col_p3.number_input("Set Duvet Fixed Rate", min_value=0, value=st.session_state.current_rates["duvet_rate"])
                
                if st.form_submit_button("Broadcast New Rates to Website", use_container_width=True):
                    st.session_state.current_rates["clothes_rate"] = new_clothes
                    st.session_state.current_rates["carpet_rate"] = new_carpet
                    st.session_state.current_rates["duvet_rate"] = new_duvet
                    st.success("Rates successfully updated globally!")
                    st.rerun()
