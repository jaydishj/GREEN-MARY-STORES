import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd
import sqlite3

# ------------------ DB SETUP ------------------
def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (name TEXT, address TEXT, phone TEXT, pincode TEXT, 
                  payment TEXT, gpay_number TEXT, txn_id TEXT, items TEXT)''')
    conn.commit()
    conn.close()

def save_order(order):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""INSERT INTO orders 
            (name, address, phone, pincode, payment, gpay_number, txn_id, items) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
          (order["name"], order["address"], order["phone"], order["pincode"], 
           order["payment"], order.get("gpay_number"), order.get("txn_id"), 
           str(order.get("items"))))
    conn.commit()
    conn.close()

def load_orders():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ------------------ LOTTIE ------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

login_anim = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
store_anim = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t24tpvcu.json")
success_anim = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "cart" not in st.session_state:
    st.session_state.cart = []
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ---- LOGIN PAGE ----
if st.session_state.page == "login":
    st.image("c:/Users/Admin/Downloads/mary matha.jpg", width=180)
    st.title("🌱 Welcome to Green Mary Store")
    st_lottie(login_anim, height=200)

    st.subheader("🔑 Sign In")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")

    if st.button("Sign In"):
        if email == "admin" and password == "6384052655":
            st.session_state.admin_logged = True
            st.session_state.page = "admin"
            st.rerun()
        elif email and password:
            st.session_state.page = "store"
            st.rerun()
        else:
            st.error("⚠️ Please enter both Email and Password.")

# ---- STORE PAGE ----
elif st.session_state.page == "store":
    st.image("c:/Users/Admin/Downloads/1000508306.jpg", caption="🌾 Welcome to Green Mary Stores", use_container_width=True)

    st.markdown("""
    Welcome to **GREEN MARY STORES** 🌱  
    An initiative by **St. Mary’s College (Autonomous), Thoothukudi – Department of Botany**.  

    Our store proudly offers **eco-friendly, organic, and herbal products** crafted with care and scientific expertise by our Botany students. 🌿 
    """)
    st.image("c:/Users/Admin/Downloads/IMG-20250815-WA0020.jpg", caption="Department of Botany", use_container_width=False)

    st.markdown("""
    ✨ **Why Choose Us?**  
    - 100% Natural and Sustainable Products 🍃  
    - Promoting Student Innovation and Entrepreneurship 🎓  
    - Supporting Local Farmers and Communities 👨‍🌾👩‍🌾  
    - Quality assured through academic research and practice 🔬  

    Together, we aim to blend **traditional knowledge with modern science**, ensuring health, sustainability, and innovation for a greener tomorrow. 🌍💚  
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("c:/Users/Admin/Downloads/1000508303.jpg", use_container_width=True)
    with col2:
        st.write("""
        🌱 **Our Promise:**  
        Every product is made with natural ingredients, ensuring **purity, freshness, and eco-friendliness**.  
        """)

    st.markdown("""
    ## 🌿 Our Mission  
    To bring nature closer to people by providing sustainable herbal solutions while empowering students and farmers.  
    """)

    st.image("c:/Users/Admin/Downloads/1000508302.jpg", caption="🌾 Freshness Guaranteed", use_container_width=True)
    st_lottie(store_anim, height=250)

    if st.button("View Products"):
        st.session_state.page = "products"
        st.rerun()

# ---- PRODUCTS PAGE ----
elif st.session_state.page == "products":
    st.header("🛒 Products")
    products = [
        {"name": "Dry amla", "price": 100, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0022.jpg"},
        {"name": "Ragi powder", "price": 100, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0021.jpg"},
        {"name": "Masala tea powder", "price": 100, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0018.jpg"},
        {"name": "Herbal hair growth oil", "price": 80, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0023.jpg"},
        {"name": "Face pack powder", "price": 100, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0025.jpg"},
        {"name": "Rose petal jam", "price": 85, "image": "c:/Users/Admin/Downloads/IMG-20250815-WA0019.jpg"}
    ]
    for p in products:
        st.image(p["image"], width=150)
        st.subheader(f"{p['name']} - ₹{p['price']}")
        if st.button(f"Add to Cart: {p['name']}"):
            st.session_state.cart.append(p)
    if st.button("View Cart"):
        st.session_state.page = "cart"
        st.rerun()

# ---- CART PAGE ----
elif st.session_state.page == "cart":
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.warning("Cart is empty!")
    else:
        for item in st.session_state.cart:
            st.write(f"✔️ {item['name']} - ₹{item['price']}")
        total = sum([item["price"] for item in st.session_state.cart])
        st.success(f"Total: ₹{total}")
    if st.button("Place Order"):
        st.session_state.page = "order"
        st.rerun()

# ---- ORDER PAGE ----
elif st.session_state.page == "order":
    st.header("📦 Place Your Order")
    payment = st.radio("Choose Payment Method:", ["Cash on Delivery", "GPay"])
    if payment == "GPay":
        gpay = st.text_input("GPay number:", "12345678")
    Name = st.text_input("Enter your name:")
    address = st.text_area("Enter Delivery Address:")
    phone = st.text_input("Enter your phone number:")
    pincode = st.text_input("Enter your pincode")
    txn = ""
    if payment == "GPay":
        txn = st.text_input("Enter GPay Transaction ID:")

    if st.button("Confirm Order"):
        order = {
            "name": Name,
            "address": address,
            "phone": phone,
            "pincode": pincode,
            "payment": payment,
            "transaction": txn if payment == "GPay" else "N/A",
            "items": st.session_state.cart.copy()
        }

        save_order(order)   # ✅ Save to DB
        st_lottie(success_anim, height=200)
        st.success("✅ Order placed successfully!")
        st.info("🌱 Quote: 'Agriculture is the backbone of our nation.'")
        st.session_state.cart.clear()

# ---- ADMIN PAGE ----
elif st.session_state.page == "admin":
    st.header("🔑 Admin Dashboard")
    if not st.session_state.admin_logged:
        st.error("Unauthorized! Please login as admin.")
        st.session_state.page = "login"
        st.rerun()
    else:
        st.success("Welcome Admin! Here are all the orders 👇")
        orders = load_orders()
        if not orders:
            st.info("No orders placed yet.")
        else:
            df = pd.DataFrame(orders,columns=["Name","Address","Phone","Pincode","Payment","GPay Number","Transaction ID","Items"])
            st.dataframe(df, use_container_width=True)

        if st.button("Logout"):
            st.session_state.admin_logged = False
            st.session_state.page = "login"
            st.rerun()
