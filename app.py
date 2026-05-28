# =========================================================
# BIGZ CLEANERS - SMART LAUNDRY MANAGEMENT SYSTEM
# STREAMLIT CLOUD SAFE VERSION
# =========================================================
# INSTALL:
# pip install streamlit pandas
#
# RUN:
# streamlit run app.py
# =========================================================

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# =========================================================
# SAFE ENCRYPTION SYSTEM
# =========================================================

try:
    import bcrypt

    BCRYPT_AVAILABLE = True

    def hash_password(password):
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

    def verify_password(password, hashed):
        return bcrypt.checkpw(
            password.encode(),
            hashed
        )

except ModuleNotFoundError:

    import hashlib

    BCRYPT_AVAILABLE = False

    def hash_password(password):
        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    def verify_password(password, hashed):
        return (
            hashlib.sha256(
                password.encode()
            ).hexdigest()
            == hashed
        )

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
# SERVICES DATABASE
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
# STYLING
# =========================================================

st.markdown("""
<style>

.main {
    background-color:#f5f7fa;
}

.big-title {
    font-size:45px;
    font-weight:bold;
    color:#0066cc;
}

.card {
    background:white;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}

.metric-card {
    background:#ffffff;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
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

if BCRYPT_AVAILABLE:
    st.success("Secure Encryption Active")
else:
    st.warning("Fallback Encryption Active")

# =========================================================
# SIDEBAR MENU
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
        "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?q=80&w=1200",
        use_container_width=True
    )

    st.markdown("## Our Laundry Services")

    cols = st.columns(len(services))

    for i, (service, price) in enumerate(services.items()):

        with cols[i]:

            st.markdown(f"""
            <div class='card'>
            <h4>{service}</h4>
            <h2>KES {price}</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## Operational Workflow")

    st.code("""
Customer App
   ↓
Browse Services
   ↓
Select Service
   ↓
Choose Weight / Quantity
   ↓
Apply Promo Codes
   ↓
Dynamic Price Calculation
   ↓
Pickup Scheduling
   ↓
Secure Payment
   ↓
Admin Receives Order
   ↓
Laundry Processing
   ↓
Delivery Tracking
    """)

# =========================================================
# CLIENT SIGNUP
# =========================================================

elif menu == "Client Sign Up":

    st.subheader("Create New Client Account")

    with st.form("signup_form"):

        name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        address = st.text_area("Home Address")

        password = st.text_input(
            "Password",
            type="password"
        )

        tier = st.selectbox(
            "Customer Tier",
            [
                "Normal",
                "Wholesale",
                "VIP"
            ]
        )

        submit = st.form_submit_button(
            "Create Account"
        )

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

            st.success(
                "Account Created Successfully"
            )

# =========================================================
# CLIENT LOGIN
# =========================================================

elif menu == "Client Login":

    st.subheader("Client Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user_found = None

        for user in st.session_state.users:

            if user["email"] == email:
                user_found = user

        if user_found:

            if verify_password(
                password,
                user_found["password"]
            ):

                st.success(
                    f"Welcome {user_found['name']}"
                )

                st.markdown("---")

                st.subheader("Create Laundry Order")

                service = st.selectbox(
                    "Select Service",
                    list(services.keys())
                )

                quantity = st.number_input(
                    "Enter Weight / Quantity",
                    min_value=1,
                    step=1
                )

                pickup_date = st.date_input(
                    "Pickup Date"
                )

                pickup_time = st.time_input(
                    "Pickup Time"
                )

                location = st.text_input(
                    "Pickup Address"
                )

                promo = st.text_input(
                    "Promo Code"
                )

                # =================================
                # DYNAMIC PRICING
                # =================================

                base_price = services[service]

                subtotal = base_price * quantity

                # Tier Pricing Logic
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

                # =================================
                # PRICE SUMMARY
                # =================================

                st.markdown("## Price Summary")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Subtotal",
                        f"KES {subtotal:.0f}"
                    )

                with col2:
                    st.metric(
                        "Discount",
                        f"KES {discount:.0f}"
                    )

                with col3:
                    st.metric(
                        "Total",
                        f"KES {total:.0f}"
                    )

                # =================================
                # PLACE ORDER
                # =================================

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

                # =================================
                # USER ORDERS
                # =================================

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

                        <h4>Order #{order['order_id']}</h4>

                        <p><b>Service:</b> {order['service']}</p>

                        <p><b>Quantity:</b> {order['quantity']}</p>

                        <p><b>Total:</b> KES {order['total']}</p>

                        <p><b>Status:</b> {order['status']}</p>

                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.info("No Orders Yet")

            else:
                st.error("Wrong Password")

        else:
            st.error("Account Not Found")

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif menu == "Admin Dashboard":

    st.subheader("Admin Login")

    admin_user = st.text_input(
        "Admin Username"
    )

    admin_pass = st.text_input(
        "Admin Password",
        type="password"
    )

    if st.button("Access Dashboard"):

        if (
            admin_user == "admin"
            and admin_pass == "admin123"
        ):

            st.success("Admin Access Granted")

            tabs = st.tabs([
                "Orders",
                "Users",
                "Analytics",
                "Pricing",
                "Promos"
            ])

            # =================================
            # ORDERS TAB
            # =================================

            with tabs[0]:

                st.subheader("Laundry Orders")

                if st.session_state.orders:

                    for index, order in enumerate(
                        st.session_state.orders
                    ):

                        st.markdown(f"""
                        <div class='card'>

                        <h4>Order #{order['order_id']}</h4>

                        <p><b>Client:</b> {order['client']}</p>

                        <p><b>Service:</b> {order['service']}</p>

                        <p><b>Total:</b> KES {order['total']}</p>

                        <p><b>Status:</b> {order['status']}</p>

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

                            st.success(
                                "Status Updated"
                            )

                else:
                    st.info("No Orders Available")

            # =================================
            # USERS TAB
            # =================================

            with tabs[1]:

                st.subheader(
                    "Registered Clients"
                )

                if st.session_state.users:

                    users_df = pd.DataFrame([

                        {
                            "ID": u["id"],
                            "Name": u["name"],
                            "Email": u["email"],
                            "Tier": u["tier"]
                        }

                        for u in st.session_state.users

                    ])

                    st.dataframe(users_df)

                else:
                    st.info("No Users Yet")

            # =================================
            # ANALYTICS TAB
            # =================================

            with tabs[2]:

                st.subheader(
                    "Business Analytics"
                )

                total_orders = len(
                    st.session_state.orders
                )

                total_revenue = sum(

                    order["total"]

                    for order in st.session_state.orders

                )

                total_users = len(
                    st.session_state.users
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Orders",
                        total_orders
                    )

                with col2:
                    st.metric(
                        "Revenue",
                        f"KES {total_revenue:.0f}"
                    )

                with col3:
                    st.metric(
                        "Customers",
                        total_users
                    )

            # =================================
            # PRICING TAB
            # =================================

            with tabs[3]:

                st.subheader(
                    "Dynamic Pricing"
                )

                for service in services:

                    new_price = st.number_input(

                        f"{service} Price",

                        value=services[service]

                    )

                    services[service] = new_price

                st.success(
                    "Prices Updated"
                )

            # =================================
            # PROMOS TAB
            # =================================

            with tabs[4]:

                st.subheader(
                    "Promo Codes"
                )

                promo_name = st.text_input(
                    "Promo Name"
                )

                promo_value = st.number_input(
                    "Discount %",
                    min_value=1,
                    max_value=100
                )

                if st.button(
                    "Add Promo Code"
                ):

                    st.session_state.promos[
                        promo_name
                    ] = promo_value

                    st.success(
                        "Promo Added"
                    )

                st.write(
                    st.session_state.promos
                )

        else:
            st.error(
                "Invalid Admin Credentials"
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.write(
    "© 2026 BIGZ CLEANERS | Smart Laundry Platform"
            )
