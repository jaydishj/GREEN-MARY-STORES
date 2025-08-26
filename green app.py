import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd
import sqlite3


# Inject custom frontend
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Green Mary Store</title>
<style>
  body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    color: #333;
    overflow-x: hidden;
    background: #fdfdfd;
  }

  /* Floating flowers background */
  .flower {
    position: fixed;
    top: -100px;
    width: 50px;
    height: 50px;
    background-image: url('https://png.pngtree.com/png-vector/20230310/ourmid/pngtree-hand-painted-pink-flower-png-image_6649407.png');
    background-size: cover;
    animation: fall linear infinite;
    z-index: -1;
    opacity: 0.8;
  }
  @keyframes fall {
    0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
  }

  /* Header */
  header {
    text-align: center;
    padding: 30px;
    font-size: 2.2rem;
    font-weight: bold;
    color: #6a1b9a;
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
    background: #fff;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #eee;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    cursor: pointer;
  }

  .card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
  }

  .card img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 15px;
  }

  .card h3 {
    color: #6a1b9a;
    margin: 10px 0;
  }

  .card p {
    margin: 5px 0;
    font-size: 1.1rem;
  }

  /* Sign-in Modal */
  .modal {
    display: none;
    position: fixed;
    z-index: 100;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
  }
  .modal-content {
    background: #fff;
    margin: 10% auto;
    padding: 20px;
    border-radius: 15px;
    max-width: 400px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  }
  .modal-content h2 {
    margin-bottom: 15px;
    color: #6a1b9a;
  }
  .modal-content input {
    width: 80%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 8px;
    border: 1px solid #ccc;
  }
  .modal-content button {
    padding: 10px 20px;
    border: none;
    border-radius: 25px;
    background: #6a1b9a;
    color: #fff;
    font-weight: bold;
    cursor: pointer;
  }
  .close {
    float: right;
    font-size: 20px;
    cursor: pointer;
    color: #aaa;
  }
  .close:hover {
    color: #000;
  }
</style>
</head>
<body>
  <!-- Floating flowers -->
  <div class="flower" style="left:10%; animation-duration:12s;"></div>
  <div class="flower" style="left:30%; animation-duration:15s;"></div>
  <div class="flower" style="left:50%; animation-duration:10s;"></div>
  <div class="flower" style="left:70%; animation-duration:14s;"></div>
  <div class="flower" style="left:90%; animation-duration:11s;"></div>

  <!-- Header -->
  <header>🌸 Welcome to Green Mary Store 🌸</header>

  <!-- Products -->
  <section class="products">
    <div class="card" onclick="openModal()">
      <img src="https://via.placeholder.com/150" alt="Dry Amla">
      <h3>Dry Amla</h3>
      <p>₹100</p>
    </div>
    <div class="card" onclick="openModal()">
      <img src="https://via.placeholder.com/150" alt="Ragi Powder">
      <h3>Ragi Powder</h3>
      <p>₹120</p>
    </div>
    <div class="card" onclick="openModal()">
      <img src="https://via.placeholder.com/150" alt="Masala Tea">
      <h3>Masala Tea</h3>
      <p>₹150</p>
    </div>
  </section>

  <!-- Sign-in Modal -->
  <div id="signinModal" class="modal">
    <div class="modal-content">
      <span class="close" onclick="closeModal()">&times;</span>
      <h2>Sign In</h2>
      <input type="text" placeholder="Email">
      <input type="password" placeholder="Password">
      <button onclick="alert('Signed in!')">Sign In</button>
    </div>
  </div>

<script>
function openModal() {
  document.getElementById("signinModal").style.display = "block";
}
function closeModal() {
  document.getElementById("signinModal").style.display = "none";
}
</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)

# Render it
components.html(html_code, height=900, scrolling=True)


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
    st.image("LOGO.jpg", width=180)
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
    st.image("first.jpg", caption="🌾 Welcome to Green Mary Stores", use_container_width=True)

    st.markdown("""
    Welcome to **GREEN MARY STORES** 🌱  
    An initiative by **St. Mary’s College (Autonomous), Thoothukudi – Department of Botany**.  

    Our store proudly offers **eco-friendly, organic, and herbal products** crafted with care and scientific expertise by our Botany students. 🌿 
    """)
    st.image("second.jpg", caption="Department of Botany", use_container_width=False)

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
        st.image("third.jpg", use_container_width=True)
    with col2:
        st.write("""
        🌱 **Our Promise:**  
        Every product is made with natural ingredients, ensuring **purity, freshness, and eco-friendliness**.  
        """)

    st.markdown("""
    ## 🌿 Our Mission  
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
        {"name": "Dry amla", "price": 100, "image": "AMLA.jpg"},
        {"name": "Ragi powder", "price": 100, "image": "RAGI.jpg"},
        {"name": "Masala tea powder", "price": 100, "image": "MASALA.jpg"},
        {"name": "Herbal hair growth oil", "price": 80, "image": "HERBAL.jpg"},
        {"name": "Face pack powder", "price": 100, "image": "FACEPACK.jpg"},
        {"name": "Rose petal jam", "price": 85, "image": "ROSE.jpg"}
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
