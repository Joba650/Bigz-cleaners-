# =========================================================
# BIGZ CLEANERS - SMART LAUNDRY MANAGEMENT SYSTEM
# Full Streamlit Website Script
# =========================================================
# INSTALL FIRST:
# pip install streamlit pandas bcrypt stripe
#
# RUN:
# streamlit run app.py
# =========================================================

import streamlit as st
import pandas as pd
import bcrypt
import uuid
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bigz Cleaners",
    page_icon="🧺",
    layout="wide"
)

# =========================================================
# SESSION STORAGE
# =========================================================

if "users" not in st.session_state:
    st.session_state.users = []

if "orders" not in st.session_state:
    st.session_state.orders = []

if "promos" not in st.session_state:
    st.session_state.promos = {
        "BIGZ10": 10,
        "WELCOME20": 20,
        "VIP30": 30
    }

# =========================================================
# STYLES
# =========================================================

st.markdown("""
<style>
.main {
    background-color:#f5f7fa;
}

.big-title {
    font-size:40px;
    font-weight:bold;
    color:#0066cc;
}

.card {
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom:15px;
}

.status-box {
    padding:10px;
    border-radius:10px;
    color:white;
    text-align:center;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<div class='big-title'>🧺 BIGZ CLEANERS</div>",
    unsafe_allow_html=True
)

st.write("Professional Smart Laundry Service Platform")

# =========================================================
# DATABASE TABLES (SIMULATION)
# =========================================================

services = {
    "Wash & Fold": 200,
    "Dry Cleaning": 350,
    "Ironing": 100,
    "Carpet Cleaning": 150,
    "Blanket Cleaning": 400
}

status_flow = [
    "Pickup Scheduled",
    "Picked Up",
    "Washing",
    "Drying",
    "Packaging",
    "Ready For Delivery",
    "Delivered"
]

# =========================================================
# SECURITY FUNCTIONS
# =========================================================

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Client Sign Up",
        "Client Login",
        "Admin Dashboard"
    ]
)

# =========================================================
# HOME PAGE
# =========================================================

if menu == "Home":

    st.image(
        "https://images.unsplash.com/photo-1521656693074-0ef32e80a5d5?q=80&w=1200",
        use_container_width=True
    )

    st.markdown("## Smart Laundry Services")

    cols = st.columns(5)

    for i, (service, price) in enumerate(services.items()):
        with cols[i]:
            st.markdown(f"""
            <div class='card'>
            <h4>{service}</h4>
            <h2>KES {price}</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## Operational Flow")

    st.code("""
Client App
   ↓
Browse Services
   ↓
Select Laundry Type
   ↓
Choose Weight / Quantity
   ↓
Apply Promo Codes
   ↓
Dynamic Price Calculation
   ↓
Pickup Scheduling
   ↓
Payment Processing
   ↓
Admin Receives Order
   ↓
Laundry Processing
   ↓
Delivery Tracking
    """)

# =========================================================
# CLIENT SIGN UP
# =========================================================

elif menu == "Client Sign Up":

    st.subheader("Create Account")

    with st.form("signup_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        address = st.text_area("Address")
        password = st.text_input("Password", type="password")

        tier = st.selectbox(
            "Customer Pricing Tier",
            ["Normal", "Wholesale", "VIP"]
        )

        submit = st.form_submit_button("Create Account")

        if submit:

            hashed = hash_password(password)

            st.session_state.users.append({
                "id": str(uuid.uuid4())[:8],
                "name": name,
                "email": email,
                "address": address,
                "password": hashed,
                "tier": tier,
                "role": "customer"
            })

            st.success("Account Created Successfully")

# =========================================================
# CLIENT LOGIN
# =========================================================

elif menu == "Client Login":

    st.subheader("Client Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user_found = None

        for user in st.session_state.users:
            if user["email"] == email:
                user_found = user

        if user_found:

            if verify_password(password, user_found["password"]):

                st.success(f"Welcome {user_found['name']}")

                st.markdown("---")

                st.subheader("Start New Order")

                service = st.selectbox(
                    "Select Service",
                    list(services.keys())
                )

                quantity = st.number_input(
                    "Enter Weight / Quantity",
                    min_value=1,
                    step=1
                )

                pickup_date = st.date_input("Pickup Date")

                pickup_time = st.time_input("Pickup Time")

                location = st.text_input("Pickup Address")

                promo = st.text_input("Promo Code")

                # =================================================
                # DYNAMIC PRICING ENGINE
                # =================================================

                base_price = services[service]

                subtotal = base_price * quantity

                # Tier Pricing
                if user_found["tier"] == "Wholesale":
                    subtotal *= 0.85

                elif user_found["tier"] == "VIP":
                    subtotal *= 0.75

                discount = 0

                if promo in st.session_state.promos:
                    discount = (
                        subtotal *
                        st.session_state.promos[promo]
                    ) / 100

                total = subtotal - discount

                st.markdown("## Price Summary")

                st.write(f"Subtotal: KES {subtotal}")
                st.write(f"Discount: KES {discount}")
                st.write(f"Total: KES {total}")

                if st.button("Place Order"):

                    order_id = str(uuid.uuid4())[:8]

                    st.session_state.orders.append({
                        "order_id": order_id,
                        "client": user_found["name"],
                        "email": user_found["email"],
                        "service": service,
                        "quantity": quantity,
                        "location": location,
                        "pickup_date": str(pickup_date),
                        "pickup_time": str(pickup_time),
                        "subtotal": subtotal,
                        "discount": discount,
                        "total": total,
                        "status": "Pickup Scheduled",
                        "payment": "Paid",
                        "created": datetime.now()
                    })

                    st.success(
                        f"Order Created Successfully | ID: {order_id}"
                    )

                # =================================================
                # USER ORDERS
                # =================================================

                st.markdown("---")
                st.subheader("My Orders")

                user_orders = [
                    o for o in st.session_state.orders
                    if o["email"] == user_found["email"]
                ]

                if user_orders:

                    for order in user_orders:

                        st.markdown(f"""
                        <div class='card'>
                        <h4>Order ID: {order['order_id']}</h4>
                        <p>Service: {order['service']}</p>
                        <p>Total: KES {order['total']}</p>
                        <p>Status: {order['status']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.info("No orders yet.")

            else:
                st.error("Invalid Password")

        else:
            st.error("Account Not Found")

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif menu == "Admin Dashboard":

    st.subheader("Admin Login")

    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type="password")

    if st.button("Access Dashboard"):

        if admin_user == "admin" and admin_pass == "admin123":

            st.success("Admin Access Granted")

            tabs = st.tabs([
                "Orders",
                "Users",
                "Analytics",
                "Pricing",
                "Promos"
            ])

            # =================================================
            # ORDERS TAB
            # =================================================

            with tabs[0]:

                st.subheader("Laundry Orders")

                if st.session_state.orders:

                    for index, order in enumerate(
                        st.session_state.orders
                    ):

                        st.markdown(f"""
                        <div class='card'>
                        <h4>Order #{order['order_id']}</h4>
                        <p>Client: {order['client']}</p>
                        <p>Service: {order['service']}</p>
                        <p>Total: KES {order['total']}</p>
                        <p>Status: {order['status']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        new_status = st.selectbox(
                            f"Update Status {order['order_id']}",
                            status_flow,
                            key=index
                        )

                        if st.button(
                            f"Save Status {order['order_id']}"
                        ):
                            st.session_state.orders[index][
                                "status"
                            ] = new_status

                            st.success("Status Updated")

                else:
                    st.info("No orders available.")

            # =================================================
            # USERS TAB
            # =================================================

            with tabs[1]:

                st.subheader("Registered Clients")

                if st.session_state.users:

                    users_df = pd.DataFrame(
                        [
                            {
                                "ID": u["id"],
                                "Name": u["name"],
                                "Email": u["email"],
                                "Tier": u["tier"]
                            }
                            for u in st.session_state.users
                        ]
                    )

                    st.dataframe(users_df)

                else:
                    st.info("No users registered.")

            # =================================================
            # ANALYTICS TAB
            # =================================================

            with tabs[2]:

                st.subheader("Business Analytics")

                total_orders = len(st.session_state.orders)

                revenue = sum(
                    order["total"]
                    for order in st.session_state.orders
                )

                customers = len(st.session_state.users)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Orders", total_orders)

                with col2:
                    st.metric("Revenue", f"KES {revenue}")

                with col3:
                    st.metric("Customers", customers)

            # =================================================
            # PRICING TAB
            # =================================================

            with tabs[3]:

                st.subheader("Dynamic Pricing Control")

                for service in services:

                    new_price = st.number_input(
                        f"{service} Price",
                        value=services[service]
                    )

                    services[service] = new_price

                st.success("Pricing Updated")

            # =================================================
            # PROMOS TAB
            # =================================================

            with tabs[4]:

                st.subheader("Discount Codes")

                promo_name = st.text_input("Promo Name")

                promo_value = st.number_input(
                    "Discount %",
                    min_value=1,
                    max_value=100
                )

                if st.button("Create Promo"):

                    st.session_state.promos[
                        promo_name
                    ] = promo_value

                    st.success("Promo Code Added")

                st.markdown("### Existing Promo Codes")

                st.write(st.session_state.promos)

        else:
            st.error("Invalid Admin Credentials")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.write("© 2026 BIGZ CLEANERS | Smart Laundry Platform")
