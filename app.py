import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="BIGZ CLEANERS",
    page_icon="🧺",
    layout="wide"
)

# ======================================
# CUSTOM CSS
# ======================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e3a8a,
            #2563eb,
            #38bdf8
        );
        color: white;
    }

    .main-title {
        text-align:center;
        font-size:60px;
        font-weight:bold;
        color:white;
        margin-top:10px;
    }

    .sub-title {
        text-align:center;
        font-size:22px;
        color:#dbeafe;
        margin-bottom:40px;
    }

    .service-card {
        background:white;
        padding:20px;
        border-radius:20px;
        box-shadow:0px 4px 15px rgba(0,0,0,0.2);
        margin-bottom:30px;
        color:black;
    }

    .tracking-box {
        background:#ffffff;
        color:black;
        padding:25px;
        border-radius:15px;
        margin-top:20px;
    }

    .footer {
        text-align:center;
        padding:30px;
        color:white;
        font-size:18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ======================================
# HEADER
# ======================================

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

# ======================================
# HERO IMAGE
# ======================================

st.image(
    "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?q=80&w=1600&auto=format&fit=crop",
    use_container_width=True
)

st.write("")
st.write("")

# ======================================
# SERVICES
# ======================================

services = [
    {
        "name": "Clothes Washing",
        "price": "KSH 200 Per 7KG",
        "description": "Professional washing, drying and folding.",
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
        "description": "Deep stain and dirt removal.",
        "image": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Curtain Cleaning",
        "price": "KSH 500 Per Pair",
        "description": "Professional curtain washing and drying.",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Duvet Cleaning",
        "price": "KSH 700 Each",
        "description": "Heavy duvet deep cleaning service.",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1200&auto=format&fit=crop"
    },
    {
        "name": "Shoe Cleaning",
        "price": "KSH 350 Per Pair",
        "description": "Sneaker and leather shoe polishing.",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1200&auto=format&fit=crop"
    }
]

st.markdown(
    "## OUR PROFESSIONAL SERVICES"
)

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

        st.write(
            service["description"]
        )

        st.success(
            service["price"]
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

# ======================================
# ORDER SECTION
# ======================================

st.markdown("---")

st.markdown("# PLACE AN ORDER")

with st.form("order_form"):

    customer_name = st.text_input(
        "Customer Name"
    )

    customer_phone = st.text_input(
        "Phone Number"
    )

    service_selected = st.selectbox(
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

    uploaded_image = st.file_uploader(
        "Upload Laundry Image"
    )

    submit_order = st.form_submit_button(
        "Create Order"
    )

if submit_order:

    tracking_code = (
        "BIGZ-" +
        str(datetime.now().strftime("%H%M%S"))
    )

    estimated_time = (
        datetime.now() +
        timedelta(hours=24)
    )

    st.success("ORDER CREATED SUCCESSFULLY")

    st.markdown(
        f"""
        <div class="tracking-box">

        <h2>Order Tracking Details</h2>

        <h3>Tracking Code:</h3>
        <p>{tracking_code}</p>

        <h3>Status:</h3>
        <p>Pending Pickup</p>

        <h3>Estimated Completion:</h3>
        <p>{estimated_time}</p>

        <h3>Pickup Location:</h3>
        <p>{pickup_location}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================
# ORDER TRACKING
# ======================================

st.markdown("---")

st.markdown("# TRACK YOUR ORDER")

tracking_input = st.text_input(
    "Enter Tracking Code"
)

if tracking_input:

    st.markdown(
        f"""
        <div class="tracking-box">

        <h2>Tracking Results</h2>

        <p><b>Tracking Code:</b> {tracking_input}</p>

        <p><b>Status:</b> Washing In Progress</p>

        <p><b>Pickup Time:</b> {datetime.now()}</p>

        <p><b>Estimated Delivery:</b>
        {datetime.now() + timedelta(hours=5)}</p>

        <p><b>Processing Stage:</b>
        Washing & Drying</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================
# LIVE CHAT SECTION
# ======================================

st.markdown("---")

st.markdown("# CUSTOMER SUPPORT CHAT")

chat_name = st.text_input(
    "Your Name"
)

chat_message = st.text_area(
    "Write Message"
)

if st.button("Send Message"):

    if chat_name and chat_message:

        st.success(
            f"Message Sent Successfully by {chat_name}"
        )

        st.info(chat_message)

# ======================================
# ADMIN DASHBOARD
# ======================================

st.markdown("---")

st.markdown("# ADMIN DASHBOARD")

admin_data = {
    "Orders Today": [25],
    "Completed": [18],
    "Pending": [7],
    "Revenue": [35000]
}

admin_df = pd.DataFrame(admin_data)

st.dataframe(
    admin_df,
    use_container_width=True
)

# ======================================
# PROCESSING TIME TRACKER
# ======================================

st.markdown("---")

st.markdown("# LAUNDRY PROCESS TRACKER")

process_steps = [
    "Pickup Completed",
    "Washing Started",
    "Drying Started",
    "Ironing Started",
    "Packaging Started",
    "Out For Delivery",
    "Delivered"
]

for step in process_steps:
    st.checkbox(step)

# ======================================
# FOOTER
# ======================================

st.markdown(
    """
    <div class="footer">

    🧺 BIGZ CLEANERS <br>

    Trusted Professional Laundry Partner <br><br>

    © 2026 BIGZ CLEANERS <br>
    Nairobi, Kenya

    </div>
    """,
    unsafe_allow_html=True
)
