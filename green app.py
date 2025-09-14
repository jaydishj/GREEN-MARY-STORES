import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd
import sqlite3
import os

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f8ff; /* light blue background */
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0); /* remove top header background */
}

[data-testid="stSidebar"] {
    background-color: #e6ffe6; /* light green sidebar */
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
# Create 2 equal columns
col1, col2, col3, col4 = st.columns([1,2,2,1])

with col2:
    st.image("images.png", caption="SMC COLLEGE", width=120)

with col3:
    st.image("MARY.jpg", caption="OUR LADY OF SORROWS", width=120)

# ------------------ HTML + CSS ------------------
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SMC STORES</title>
<style>
body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    color: #fff;
}
/* Animated gradient background */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(-45deg, #8B0000, #B22222, #FFD700, #8B0000);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    z-index: -1;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
/* Header */
header {
  display: flex;
  flex-direction: column;  /* stack logo + text vertically */
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: linear-gradient(45deg, #f9a825, #ef6c00);
  color: white;
}


header h1 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
    margin: 10px 0;
}
header p {
    font-size: 1.1rem;
    color: #fff;
    margin-bottom: 20px;
}
/* Product grid */
.products {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
    max-width: 1100px;
    margin: auto;
}
/* Product card */
.card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid #FFD700;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
.card h3 {
    color: #FFD700;
    margin: 10px 0;
}
.card p {
    margin: 5px 0;
    font-size: 1.1rem;
}
/* Buy button */
.buy-btn {
    display: inline-block;
    margin-top: 10px;
    padding: 10px 18px;
    border: none;
    border-radius: 25px;
    background: linear-gradient(45deg, #FFD700, #FFB800);
    color: #8B0000;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
.buy-btn:hover {
    background: linear-gradient(45deg, #FFCC33, #FFD700);
    transform: scale(1.05);
}
</style>
</head>
<body>
<!-- Header Section -->
<header>
    <h1>SMC STORE</h1>
    <p>BY,</p>
    <p>DEPARTMENT OF BOTANY</p> 
    <p>ST. MARY'S COLLEGE (THOOTHUKUDI)</p>
</header>

<!-- Products Section -->
<section class="products">
    <div class="card">
        <h3>Dry Amla</h3>
        <p>₹100</p>
        <button class="buy-btn">Buy Now</button>
    </div>
    <div class="card">
        <h3>Ragi Powder</h3>
        <p>₹120</p>
        <button class="buy-btn">Buy Now</button>
    </div>
    <div class="card">
        <h3>Masala Tea</h3>
        <p>₹150</p>
        <button class="buy-btn">Buy Now</button>
    </div>
    <div class="card">
        <h3>Herbal Hair Oil</h3>
        <p>₹80</p>
        <button class="buy-btn">Buy Now</button>
    </div>
</section>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)

# ------------------ DATABASE ------------------
DB_FILE = "orders.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (name TEXT, address TEXT, phone TEXT, pincode TEXT,
                  payment TEXT, gpay_number TEXT, txn_id TEXT,
                  items TEXT, screenshot TEXT)''')
    conn.commit()
    conn.close()

def save_order(order):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""INSERT INTO orders
                 (name, address, phone, pincode, payment, gpay_number, txn_id, items, screenshot)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (order["name"], order["address"], order["phone"], order["pincode"],
               order["payment"], order.get("gpay_number"), order.get("transaction"),
               str(order.get("items")), order.get("screenshot")))
    conn.commit()
    conn.close()

def load_orders():
    conn = sqlite3.connect(DB_FILE)
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

# ------------------ SESSION ------------------
if "page" not in st.session_state: st.session_state.page = "login"
if "cart" not in st.session_state: st.session_state.cart = []
if "admin_logged" not in st.session_state: st.session_state.admin_logged = False

# ---- LOGIN PAGE ----
if st.session_state.page == "login":
    st.title("🌱 Welcome to SMC STORE🌱")
    st_lottie(login_anim, height=200)
    st.subheader("🔑 Sign In")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    if st.button("Sign In"):
        if email == "admin" and password == "smctuty":
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
    st.image("first.jpg", caption="🌾Welcome to SMC STORE🌾", use_container_width=True )

    st.markdown("""
    Welcome to 🌱**SMC STORE** 🌱  
    An initiative by **St. Mary’s College (Autonomous), Thoothukudi – Department of Botany**.  

    Our store proudly offers **eco-friendly, organic, and herbal products** crafted with care and scientific expertise by our Botany students. 🌿 
    """)
    
    st.image("second.jpg", caption="Department of Botany", use_container_width=False)

    st.markdown("""
    ## ✨ Why Choose Us?
    - 100% Natural and Sustainable Products 🍃  
    - Promoting Student Innovation and Entrepreneurship 🎓  
    - Supporting Local Farmers and Communities 👨‍🌾👩‍🌾  
    - Quality assured through academic research and practice 🔬  

    Together, we aim to blend **traditional knowledge with modern science**, ensuring health, sustainability, and innovation for a greener tomorrow. 🌍💚  
    """)

    st.markdown("""
    ## 📞 Contact Info  
    **Dr. Sr. A. Arockia Jenecius Alphonse**  
    Head  
    Department of Botany  
    St. Mary’s College (Autonomous), Thoothukudi, Tamil Nadu  
    Contact No: +91 89407 39291  
    """)


    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("third.jpg", use_container_width=True)
   
    st.markdown("""
    ## 🌱 Our Promise 🌱  
    Every product is made with natural ingredients, ensuring **purity, freshness, and eco-friendliness.  
    """)

    st.markdown("""
    ## 🌿 Our Mission  🌿
    To bring nature closer to people by providing sustainable herbal solutions while empowering students and farmers.  
    """)

    st.image("fourth.jpg", caption="🌾 Freshness Guaranteed", use_container_width=True)
    st_lottie(store_anim, height=250)

    if st.button("View Products"):
        st.session_state.page = "products"
        st.rerun()


# ---- PRODUCTS PAGE ----
elif st.session_state.page == "products":
    st.header("🛒 Products")
    products = [
        {
            "name": "Dry amla",
            "price": 100,
            "images": [ "ONE.jpg"]
        },
        {
            "name": "Ragi powder",
            "price": 100,
            "images": ["TWO.jpg"]
        },
        {
            "name": "Masala tea powder",
            "price": 100,
            "images": [ "THREE.jpg"]
        },
        {
            "name": "Herbal hair growth oil",
            "price": 80,
            "images": [ "FOUR.jpg"]
        },
        {
            "name": "Face pack powder",
            "price": 100,
            "images": ["FIVE.jpg"]
        },
        {
            "name": "Rose petal jam",
            "price": 85,
            "images": [ "SIX.jpg"]
        }
    ]

    for p in products:
        st.subheader(f"{p['name']} - ₹{p['price']}")

        # Show all images for that product
        for img in p["images"]:
            st.image(img, width=150)

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

# ---- PRODUCTS PAGE ----
elif st.session_state.page == "products":
    st.header("🛒 Products")
    products = [
        {"name":"Dry amla","price":100,"images":["ONE.jpg"]},
        {"name":"Ragi powder","price":100,"images":["TWO.jpg"]},
        {"name":"Masala tea powder","price":100,"images":["THREE.jpg"]},
        {"name":"Herbal hair growth oil","price":80,"images":["FOUR.jpg"]},
        {"name":"Face pack powder","price":100,"images":["FIVE.jpg"]},
        {"name":"Rose petal jam","price":85,"images":["SIX.jpg"]}
    ]
    for p in products:
        st.subheader(f"{p['name']} - ₹{p['price']}")
        for img in p["images"]:
            st.image(img, width=150)
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
    Name = st.text_input("Enter your name:")
    address = st.text_area("Enter Delivery Address:")
    phone = st.text_input("Enter your phone number:")
    pincode = st.text_input("Enter your pincode")
    txn = ""
    file_path = None

    if payment == "GPay":
        st.markdown("### 📱 Pay using GPay")
        st.info("Send your payment to **GPay Number: 89407 39291**")
        txn = st.text_input("Enter your GPay Transaction ID after payment:")
        payment_screenshot = st.file_uploader("Upload GPay Payment Screenshot", type=["png","jpg","jpeg"])
        if payment_screenshot is not None:
            os.makedirs("screenshots", exist_ok=True)
            file_path = os.path.join("screenshots", payment_screenshot.name)
            with open(file_path, "wb") as f:
                f.write(payment_screenshot.getbuffer())
            st.success("✅ Screenshot uploaded successfully!")
            st.image(file_path, caption="Uploaded Payment Screenshot", width=300)

    if st.button("Confirm Order"):
        order = {
            "name": Name,
            "address": address,
            "phone": phone,
            "pincode": pincode,
            "payment": payment,
            "transaction": txn if payment=="GPay" else "N/A",
            "screenshot": file_path if file_path else "N/A",
            "items": st.session_state.cart.copy(),
            "gpay_number": "89407 39291" if payment=="GPay" else "N/A"
        }
        save_order(order)
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
            df = pd.DataFrame(
                orders,
                columns=["Name","Address","Phone","Pincode","Payment","GPay Number","Transaction ID","Items","Screenshot"]
            )
            st.dataframe(df, use_container_width=True)

            for i, order in enumerate(orders):
                screenshot_path = order[-1]
                if screenshot_path != "N/A" and os.path.exists(screenshot_path):
                    with open(screenshot_path, "rb") as f:
                        img_bytes = f.read()
                        st.download_button(
                            label=f"⬇ Download Screenshot (Order {i+1})",
                            data=img_bytes,
                            file_name=os.path.basename(screenshot_path),
                            mime="image/png"
                        )
                        st.image(img_bytes, caption=f"Screenshot for Order {i+1}", width=300)

        if st.button("Logout"):
            st.session_state.admin_logged = False
            st.session_state.page = "login"
            st.rerun()
