import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="BIGZ CLEANERS",
    page_icon="🧺",
    layout="wide"
)

# =========================================
# SESSION STATES
# =========================================

if "users" not in st.session_state:
    st.session_state.users = {
        "admin@bigz.com": {
            "name": "BIGZ ADMIN",
            "phone": "0700000000",
            "password": "admin123",
            "role": "admin"
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_role" not in st.session_state:
    st.session_state.current_role = ""

if "saved_email" not in st.session_state:
    st.session_state.saved_email = ""

if "orders" not in st.session_state:
    st.session_state.orders = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #1d4ed8,
            #38bdf8
        );
        background-attachment: fixed;
        color: white;
    }

    .main-title {
        text-align:center;
        font-size:65px;
        font-weight:bold;
        color:white;
    }

    .sub-title {
        text-align:center;
        font-size:24px;
        color:#dbeafe;
        margin-bottom:30px;
    }

    .service-card {
        background:white;
        padding:20px;
        border-radius:20px;
        margin-bottom:25px;
        color:black;
        box-shadow:0px 4px 15px rgba(0,0,0,0.25);
    }

    .track-box {
        background:white;
        color:black;
        padding:25px;
        border-radius:18px;
        margin-top:20px;
    }

    .footer {
        text-align:center;
        color:white;
        padding:30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# HEADER
# =========================================

st.markdown(
    """
    <div class="main-title">
        🧺 BIGZ CLEANERS
    </div>

    <div class="sub-title">
        Smart Laundry & Cleaning Services <br>
        Fast Pickup • Deep Cleaning • Professional Care
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# HERO IMAGE
# =========================================

st.image(
    "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?q=80&w=1600&auto=format&fit=crop",
    use_container_width=True
)

# =========================================
# ACCOUNT SYSTEM
# =========================================

st.markdown("---")
st.markdown("# CUSTOMER ACCOUNT SYSTEM")

register_tab, login_tab = st.tabs([
    "Create Account",
    "Login"
])

# =========================================
# REGISTER
# =========================================

with register_tab:

    new_name = st.text_input("Full Name")

    new_phone = st.text_input("Phone Number")

    new_email = st.text_input("Email Address")

    new_password = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Create Account"):

        if new_email in st.session_state.users:

            st.error(
                "Account Already Exists"
            )

        else:

            st.session_state.users[new_email] = {
                "name": new_name,
                "phone": new_phone,
                "password": new_password,
                "role": "customer"
            }

            st.success(
                "Customer Account Created Successfully"
            )

# =========================================
# LOGIN
# =========================================

with login_tab:

    login_email = st.text_input(
        "Email"
    )

    login_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login Account"):

        if login_email in st.session_state.users:

            user = st.session_state.users[
                login_email
            ]

            if user["password"] == login_password:

                st.session_state.logged_in = True

                st.session_state.current_user = (
                    user["name"]
                )

                st.session_state.current_role = (
                    user["role"]
                )

                st.session_state.saved_email = (
                    login_email
                )

                st.success(
                    f"Welcome {user['name']}"
                )

                st.rerun()

            else:

                st.error(
                    "Wrong Password"
                )

        else:

            st.error(
                "Account Not Found"
            )

# =========================================
# LOGGED IN USER
# =========================================

if st.session_state.logged_in:

    st.success(
        f"Logged in as {st.session_state.current_user}"
    )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_role = ""

        st.rerun()

# =========================================
# SERVICES DATA
# =========================================

services = [
    {
        "name": "Clothes Washing",
        "price": "KSH 200 Per 7KG",
        "description": "Professional washing and drying.",
        "image": "https://images.unsplash.com/photo-1521656693074-0ef32e80a5d5?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Carpet Cleaning",
        "price": "KSH 150 Per Meter",
        "description": "Deep carpet shampoo cleaning.",
        "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Sofa Cleaning",
        "price": "KSH 1200 Per Set",
        "description": "Deep sofa stain removal.",
        "image": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Curtain Cleaning",
        "price": "KSH 500 Per Pair",
        "description": "Professional curtain cleaning.",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Shoe Cleaning",
        "price": "KSH 350 Per Pair",
        "description": "Sneaker and leather polishing.",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1200&auto=format&fit=crop"
    }
]

# =========================================
# PROTECTED SERVICES
# =========================================

st.markdown("---")

if st.session_state.logged_in:

    st.markdown("# OUR SERVICES")

    col1, col2, col3 = st.columns(3)

    for index, service in enumerate(services):

        column = [col1, col2, col3][index % 3]

        with column:

            st.markdown(
                '<div class="service-card">',
                unsafe_allow_html=True
            )

            st.image(
                service["image"],
                use_container_width=True
            )

            st.markdown(
                f"### {service['name']}"
            )

            st.write(service["description"])

            st.success(service["price"])

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

else:

    st.warning(
        "Create Account And Login To Access BIGZ CLEANERS Services"
    )

# =========================================
# CLIENT PROFILE
# =========================================

if st.session_state.logged_in:

    st.markdown("---")
    st.markdown("# CLIENT PROFILE")

    total_customer_orders = len([
        o for o in st.session_state.orders
        if o['customer'] == st.session_state.current_user
    ])

    completed_customer_orders = len([
        o for o in st.session_state.orders
        if (
            o['customer'] == st.session_state.current_user
            and
            o['completed'] == True
        )
    ])

    loyalty_points = total_customer_orders * 10

    st.metric(
        "Loyalty Points",
        loyalty_points
    )

    st.metric(
        "Completed Orders",
        completed_customer_orders
    )

# =========================================
# ORDER CREATION
# =========================================

st.markdown("---")

if st.session_state.logged_in:

    st.markdown("# PLACE ORDER")

    with st.form("order_form"):

        customer_phone = st.text_input(
            "Phone Number"
        )

        selected_service = st.selectbox(
            "Select Service",
            [s["name"] for s in services]
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        pickup_location = st.text_input(
            "Pickup Location"
        )

        create_order = st.form_submit_button(
            "Create Order"
        )

    if create_order:

        tracking_code = (
            "BIGZ-" +
            datetime.now().strftime("%H%M%S")
        )

        order = {
            "customer": st.session_state.current_user,
            "phone": customer_phone,
            "service": selected_service,
            "quantity": quantity,
            "location": pickup_location,
            "tracking": tracking_code,
            "status": "Pending Pickup",
            "completed": False,
            "created": str(datetime.now())
        }

        st.session_state.orders.append(order)

        st.success(
            "ORDER CREATED SUCCESSFULLY"
        )

        st.markdown(
            f"""
            <div class="track-box">

            <h2>Order Tracking</h2>

            <p><b>Tracking Code:</b>
            {tracking_code}</p>

            <p><b>Status:</b>
            Pending Pickup</p>

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================
# ORDER TRACKING
# =========================================

st.markdown("---")
st.markdown("# TRACK YOUR ORDER")

tracking_input = st.text_input(
    "Enter Tracking Code"
)

if tracking_input:

    found = False

    for order in st.session_state.orders:

        if order["tracking"] == tracking_input:

            found = True

            st.markdown(
                f"""
                <div class="track-box">

                <h2>Tracking Results</h2>

                <p><b>Customer:</b>
                {order['customer']}</p>

                <p><b>Status:</b>
                {order['status']}</p>

                <p><b>Service:</b>
                {order['service']}</p>

                </div>
                """,
                unsafe_allow_html=True
            )

    if not found:
        st.error("Tracking Code Not Found")

# =========================================
# CUSTOMER CHAT
# =========================================

st.markdown("---")
st.markdown("# CUSTOMER SUPPORT CHAT")

chat_message = st.text_area(
    "Write Message"
)

if st.button("Send Message"):

    if chat_message:

        st.session_state.messages.append({
            "name": st.session_state.current_user,
            "message": chat_message,
            "time": str(datetime.now())
        })

        st.success("Message Sent")

for msg in st.session_state.messages:

    st.info(
        f"{msg['name']}: {msg['message']}"
    )

# =========================================
# ADMIN PROFILE & DASHBOARD
# =========================================

if (
    st.session_state.logged_in
    and
    st.session_state.current_role == "admin"
):

    st.markdown("---")
    st.markdown("# ADMIN DASHBOARD")

    total_customers = len([
        u for u in st.session_state.users.values()
        if u['role'] == 'customer'
    ])

    total_orders = len(
        st.session_state.orders
    )

    completed_orders = len([
        o for o in st.session_state.orders
        if o['completed'] == True
    ])

    pending_orders = (
        total_orders - completed_orders
    )

    total_messages = len(
        st.session_state.messages
    )

    completion_percentage = 0

    if total_orders > 0:

        completion_percentage = (
            completed_orders /
            total_orders
        ) * 100

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Customers",
            total_customers
        )

    with metric2:
        st.metric(
            "Orders",
            total_orders
        )

    with metric3:
        st.metric(
            "Chats",
            total_messages
        )

    with metric4:
        st.metric(
            "Delivery %",
            f"{completion_percentage:.1f}%"
        )

    analytics_data = pd.DataFrame({
        "Category": [
            "Completed",
            "Pending",
            "Customers",
            "Chats"
        ],
        "Count": [
            completed_orders,
            pending_orders,
            total_customers,
            total_messages
        ]
    })

    st.bar_chart(
        analytics_data.set_index(
            "Category"
        )
    )

    st.line_chart(
        analytics_data.set_index(
            "Category"
        )
    )

    st.progress(
        int(completion_percentage)
    )

    st.markdown(
        "## UPDATE ORDER STATUS"
    )

    for index, order in enumerate(
        st.session_state.orders
    ):

        st.write(
            f"{order['tracking']} - {order['customer']}"
        )

        new_status = st.selectbox(
            f"Status {index}",
            [
                "Pending Pickup",
                "Picked Up",
                "Washing",
                "Drying",
                "Ironing",
                "Packaging",
                "Out For Delivery",
                "Delivered"
            ],
            key=index
        )

        if st.button(
            f"Save {index}"
        ):

            order['status'] = new_status

            if new_status == "Delivered":
                order['completed'] = True

            st.success(
                "Order Updated"
            )

# =========================================
# FOOTER
# =========================================

st.markdown(
    """
    <div class="footer">

    🧺 BIGZ CLEANERS <br>

    Trusted Laundry Partner <br><br>

    © 2026 BIGZ CLEANERS

    </div>
    """,
    unsafe_allow_html=True
)
