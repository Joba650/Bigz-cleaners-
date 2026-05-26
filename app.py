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
        
        feature_one_col,
