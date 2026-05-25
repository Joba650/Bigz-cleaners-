import streamlit as st
import random
import pandas as pd
from datetime import datetime

# --- CONFIGURATION & DATABASE SIMULATION ---
st.set_page_config(page_title="Jojo Laundry Services", page_icon="🧺", layout="centered")

# Simulate a database using Streamlit's session state
if "users" not in st.session_state:
    # Pre-populating with a few mock clients so the percentage counter works immediately for you to see!
    st.session_state.users = {
        "JL-482910": {"name": "John Kamau", "phone": "0712345678"},
        "JL-883012": {"name": "Mary Atieno", "phone": "0722112233"},
        "JL-194823": {"name": "David Mwangi", "phone": "0733445566"},
        "JL-773912": {"name": "Grace Wanjiku", "phone": "0700998877"}
    }
if "orders" not in st.session_state:
    # Starting with one active order from Mary to show how the counter calculates percentages
    st.session_state.orders = [
        {
            "Order ID": "ORD-5521",
            "User Tag": "JL-883012",
            "Customer": "Mary Atieno",
            "Phone": "0722112233",
            "7kg Clothes Loads": 2,
            "Carpet Inches": 0,
            "Location": "Njoro Town, near stage",
            "Est. Cost": 400,
            "Status": "Pending Pickup"
        }
    ]
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# --- HELPER FUNCTIONS ---
def generate_unique_account():
    """Generates a unique 6-digit numeric account format to prevent cloth mix-ups."""
    while True:
        acc_num = f"JL-{random.randint(100000, 999999)}"
        if acc_num not in st.session_state.users:
            return acc_num

# --- APP UI ---
st.title("🧺 Jojo Laundry & Carpet Services")
st.write("Fast, reliable cleaning picked up and delivered straight to your door.")

# --- SIDEBAR: PRICING & SERVICES ---
st.sidebar.header("💰 Our Rates & Services")
st.sidebar.markdown("""
* **🫓 Carpets:** KSh 150 per sq. inch
* **👕 Clothes (Wash & Dry):** KSh 200 per 7 Kg load
* **🥼 Ironing Services:** *Not Applicable (Not Offered)*
---
⚠️ *Every customer is assigned a unique **Numeric Tag** (e.g., JL-123456). This tag is attached to your clothes during washing and sun-drying to strictly prevent any mix-ups.*
""")

# --- USER AUTHENTICATION SECTION ---
if not st.session_state.logged_in_user:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register New Account"])
    
    # Registration Tab
    with tab2:
        st.subheader("Create an Account")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_phone = st.text_input("Phone Number (for M-Pesa/Delivery)", key="reg_phone")
        
        if st.button("Register"):
            if reg_name and reg_phone:
                account_id = generate_unique_account()
                st.session_state.users[account_id] = {"name": reg_name, "phone": reg_phone}
                st.success(f"🎉 Account created successfully! Your unique Clothes Tag Number is: **{account_id}**")
                st.info("Please write this down or screenshot it. Use it to login below.")
            else:
                st.error("Please fill in all fields.")

    # Login Tab
    with tab1:
        st.subheader("Login to Request Pickup")
        login_id = st.text_input("Enter your Unique Tag Number (e.g., JL-123456)").strip().upper()
        
        if st.button("Login"):
            if login_id in st.session_state.users:
                st.session_state.logged_in_user = login_id
                st.rerun()
            else:
                st.error("Account number not found. Please register if you don't have one.")

# --- LOGGED IN USER INTERFACE (ORDERING) ---
else:
    user_id = st.session_state.logged_in_user
    user_info = st.session_state.users[user_id]
    
    st.success(f"Logged in as: **{user_info['name']}** | Tag Number: **{user_id}**")
    if st.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.divider()
    st.header("🚚 Request a Pickup & Delivery")
    
    with st.form("order_form"):
        st.subheader("1. Select Services Needed")
        
        # Service Inputs
        wash_7kg = st.number_input("Clothes (per 7 Kg load) - KSh 200", min_value=0, step=1, value=0)
        carpet_inch = st.number_input("Carpet Size (Total Square Inches) - KSh 150", min_value=0, step=1, value=0)
        
        st.subheader("2. Delivery & Location Details")
        pickup_location = st.text_area("Detailed Location / Estate / Apartment & House No.", 
                                       placeholder="e.g., Njoro Town, Oasis Apartments, House B4")
        
        pickup_date = st.date_input("Preferred Pickup Date", min_value=datetime.today())
        additional_notes = st.text_input("Special instructions (e.g., 'Separate white clothes')")
        
        # Calculate Estimated Cost
        est_cost = (wash_7kg * 200) + (carpet_inch * 150)
        st.markdown(f"### 💵 Estimated Cost: **KSh {est_cost:,}**")
        
        submit_order = st.form_submit_button("Submit Pickup Request")
        
        if submit_order:
            if est_cost == 0:
                st.error("Please select at least one item to clean.")
            elif not pickup_location:
                st.error("Please provide your delivery/pickup location.")
            else:
                # Save Order Details
                order_data = {
                    "Order ID": f"ORD-{random.randint(1000, 9999)}",
                    "User Tag": user_id,
                    "Customer": user_info["name"],
                    "Phone": user_info["phone"],
                    "7kg Clothes Loads": wash_7kg,
                    "Carpet Inches": carpet_inch,
                    "Location": pickup_location,
                    "Est. Cost": est_cost,
                    "Status": "Pending Pickup"
                }
                st.session_state.orders.append(order_data)
                st.balloons()
                st.success(f"📦 Order placed successfully!")

# --- ADMIN VIEW & PERFECT PERCENTAGE COUNTER ---
st.divider()
if st.checkbox("⚙️ View Business Dashboard (Admin Only)", value=True):
    st.header("📊 Business Analytics & Visibility")
    
    total_registered_clients = len(st.session_state.users)
    active_orders_count = len(st.session_state.orders)
    
    # Calculate Percentage Counter
    if total_registered_clients > 0:
        active_workload_percentage = (active_orders_count / total_registered_clients) * 100
    else:
        active_workload_percentage = 0.0

    # Display Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Registered Clients", value=total_registered_clients)
    col2.metric(label="Active Requests", value=active_orders_count)
    col3.metric(label="Active Client Demand", value=f"{active_workload_percentage:.1f}%")
    
    # Progress bar for visual impact
    st.progress(min(active_workload_percentage / 100, 1.0))
    st.caption(f"**{active_workload_percentage:.1f}%** of your total registered customer base is currently waiting for laundry services.")

    # Service Type Breakdown calculations
    if active_orders_count > 0:
        df_orders = pd.DataFrame(st.session_state.orders)
        
        clothes_orders = len(df_orders[df_orders["7kg Clothes Loads"] > 0])
        carpet_orders = len(df_orders[df_orders["Carpet Inches"] > 0])
        
        pct_clothes = (clothes_orders / active_orders_count) * 100
        pct_carpet = (carpet_orders / active_orders_count) * 100
        
        st.subheader("🎯 Service Type Visibility")
        st.write(f"👕 **Clothes Washing:** {pct_clothes:.1f}% of active orders include clothes.")
        st.write(f"🫓 **Carpet Cleaning:** {pct_carpet:.1f}% of active orders include carpets.")

    # Incoming Orders Data Table
    st.subheader("📥 Incoming Pickup & Delivery Requests")
    if st.session_state.orders:
        st.dataframe(pd.DataFrame(st.session_state.orders))
    else:
        st.write("No active pickup requests right now.")
