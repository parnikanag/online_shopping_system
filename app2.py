import streamlit as st
import pandas as pd
from db_connection import get_connection

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- AUTH FUNCTIONS ---
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def user_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE username=%s", (username,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def signup_user(username, password):
    if user_exists(username):
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def rerun_app():
    st.rerun()

# --- LOGIN/SIGNUP PAGE ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="Online Shopping System", layout="centered")

    st.markdown("""
    <div style='background:#7c3aed; padding:25px; border-radius:20px; text-align:center; box-shadow:0 8px 20px rgba(124,58,237,0.3);'>
        <h1 style='color:white;'>Online Shopping System</h1>
        <p style='font-size:20px; color:#ddd;'>DBMS Mini Project Login</p>
    </div>
    """, unsafe_allow_html=True)

    option = st.radio("Choose Option", ["Login 🔐", "Sign Up 📝"], horizontal=True)
    username = st.text_input("Username", max_chars=30)
    password = st.text_input("Password", type="password", max_chars=30)

    if option == "Login 🔐":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                rerun_app()
            else:
                st.error("❌ Invalid credentials.")
    else:
        if st.button("Sign Up"):
            if signup_user(username, password):
                st.success("✅ Account created. Please log in.")
            else:
                st.warning("⚠️ Username already exists.")

# --- MAIN APP AFTER LOGIN ---
else:
    st.set_page_config(page_title="Online Shopping System", layout="wide")

    st.markdown("""
    <div style='background:#c4b5fd; padding:20px; border-radius:15px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);'>
        <h1 style='color:#4c1d95;'>Online Shopping System</h1>
        <p style='font-size:18px; color:#5b21b6;'>DBMS Mini Project Showcase</p>
    </div>
    """, unsafe_allow_html=True)

    menu = [ "Add Customer", "Add Supplier", "Add Product", "Add Order",
    "Add Tracking Detail", "Add Admin", "View Customers",
    "View Suppliers", "View Products", "View Orders", "View Tracking Detail", "View Admins",
    "Update Customer", "Delete Customer", "Logout"]
    choice = st.sidebar.radio("📋 Select Operation", menu)

    # --- ADD CUSTOMER ---
    if choice == "Add Customer":
        st.header("➕ Add New Customer")
        with st.form("add_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                customer_name = st.text_input("Customer Name", placeholder="e.g. Parnika Nag")
                customer_address = st.text_input("Customer Address", placeholder="e.g. Bengaluru, Karnataka")
            with col2:
                customer_contact = st.text_input("Customer Contact", placeholder="e.g. 9876543210")
            if st.form_submit_button("Add Customer"):
                if customer_name and customer_address and customer_contact:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO CUSTOMER (Customer_name, Customer_address, Customer_contact) VALUES (%s, %s, %s)",
                            (customer_name, customer_address, customer_contact)
                        )
                        conn.commit()
                        st.success("✅ Customer added successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.warning("⚠️ Please fill all fields.")

    # --- ADD SUPPLIER ---
    elif choice == "Add Supplier":
        st.header("➕ Add New Supplier")
        with st.form("add_supplier_form", clear_on_submit=True):
            supplier_name = st.text_input("Supplier Name")
            supplier_address = st.text_input("Supplier Address")
            if st.form_submit_button("Add Supplier"):
                if supplier_name and supplier_address:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO SUPPLIER (Supplier_name, Supplier_address) VALUES (%s, %s)",
                            (supplier_name, supplier_address)
                        )
                        conn.commit()
                        st.success("✅ Supplier added successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.warning("⚠️ Please fill all fields.")

    # --- ADD PRODUCT ---
    elif choice == "Add Product":
        st.header("➕ Add New Product")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Supplier_id, Supplier_name FROM SUPPLIER")
            suppliers = cursor.fetchall()
            supplier_dict = {f"{sid} - {sname}": sid for sid, sname in suppliers}
        except Exception as e:
            st.error(f"❌ Error fetching suppliers: {e}")
            suppliers = []
        finally:
            cursor.close()
            conn.close()

        if suppliers:
            with st.form("add_product_form", clear_on_submit=True):
                product_name = st.text_input("Product Name")
                product_price = st.number_input("Product Price", min_value=0.0, format="%.2f")
                selected_supplier = st.selectbox("Select Supplier", list(supplier_dict.keys()))
                if st.form_submit_button("Add Product"):
                    if product_name and product_price > 0:
                        supplier_id = supplier_dict[selected_supplier]
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO PRODUCT (Prod_name, Prod_price, Supplier_id) VALUES (%s, %s, %s)",
                                (product_name, product_price, supplier_id)
                            )
                            conn.commit()
                            st.success("✅ Product added successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        st.warning("⚠️ Please fill all fields and enter valid price.")
        else:
            st.info("ℹ️ No suppliers found. Please add a supplier first.")

    # --- ADD ORDER ---
    elif choice == "Add Order":
        st.header("➕ Add New Order")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
            customers = cursor.fetchall()
            cursor.execute("SELECT Prod_id, Prod_name FROM PRODUCT")
            products = cursor.fetchall()
            customer_dict = {f"{cid} - {cname}": cid for cid, cname in customers}
            product_dict = {f"{pid} - {pname}": pid for pid, pname in products}
        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
            customers, products = [], []
        finally:
            cursor.close()
            conn.close()

        if customers and products:
            with st.form("add_order_form", clear_on_submit=True):
                selected_customer = st.selectbox("Select Customer", list(customer_dict.keys()))
                selected_product = st.selectbox("Select Product", list(product_dict.keys()))
                order_date = st.date_input("Order Date")
                order_amount = st.number_input("Order Amount", min_value=0.0, format="%.2f")
                if st.form_submit_button("Add Order"):
                    if order_amount > 0:
                        customer_id = customer_dict[selected_customer]
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO ORDERS (Order_date, Order_amount, Customer_id) VALUES (%s, %s, %s)",
                                (order_date, order_amount, customer_id)
                            )
                            conn.commit()
                            st.success("✅ Order added successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        st.warning("⚠️ Please enter a valid order amount.")
        else:
            st.info("ℹ️ Please add customers and products first.")

    # --- ADD TRACKING DETAIL ---
    elif choice == "Add Tracking Detail":
        st.header("➕ Add Tracking Detail")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Prod_id, Prod_name FROM PRODUCT")
            products = cursor.fetchall()
            product_dict = {f"{pid} - {pname}": (pid, pname) for pid, pname in products}
        except Exception as e:
            st.error(f"❌ Error fetching products: {e}")
            products = []
        finally:
            cursor.close()
            conn.close()

        if products:
            with st.form("add_tracking_form", clear_on_submit=True):
                selected_product = st.selectbox("Select Product", list(product_dict.keys()))
                prod_status = st.text_input("Product Status (e.g. shipped, delivered)")
                prod_price = st.number_input("Product Price", min_value=0.0, format="%.2f")
                if st.form_submit_button("Add Tracking Detail"):
                    if prod_status and prod_price > 0:
                        prod_id, prod_name = product_dict[selected_product]
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO TRACKING_DETAIL (Prod_id, Prod_name, Prod_price, Prod_status) VALUES (%s, %s, %s, %s)",
                                (prod_id, prod_name, prod_price, prod_status)
                            )
                            conn.commit()
                            st.success("✅ Tracking detail added successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        st.warning("⚠️ Please fill all fields and enter valid price.")
        else:
            st.info("ℹ️ Please add products first.")

    # --- ADD ADMIN ---
    elif choice == "Add Admin":
        st.header("➕ Add Admin User")
        with st.form("add_admin_form", clear_on_submit=True):
            admin_name = st.text_input("Admin Name")
            admin_role = st.text_input("Role", placeholder="e.g. Manager, Supervisor")

            if st.form_submit_button("Add Admin"):
                if admin_name and admin_role:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO ADMIN (Admin_name, Role) VALUES (%s, %s)",
                            (admin_name, admin_role)
                        )
                        conn.commit()
                        st.success("✅ Admin user added successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.warning("⚠️ Please fill all fields.")

    # --- VIEW CUSTOMERS ---
    elif choice == "View Customers":
        st.header("📋 Customer List")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CUSTOMER")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Address", "Contact"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No customers found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # --- VIEW PRODUCT ---
    elif choice == "View Products":
        st.header("📦 Product List")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Price", "Supplier ID"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No products found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

     # --- VIEW ORDER ---
    elif choice == "View Orders":
        st.header("🧾 Order List")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ORDERS")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["Order ID", "Date", "Amount", "Customer ID"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No orders found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # --- VIEW SUPPLIERS---
    elif choice == "View Suppliers":
        st.header("🚚 Supplier List")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SUPPLIER")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Address"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No suppliers found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # --- VIEW ADMINS ---
    elif choice == "View Admins":
        st.header("👨‍💼 Admin List")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ADMIN")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Role"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No admins found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()



    # --- VIEW Tracking Detail ---
    elif choice == "View Tracking Details":
        st.header("📦 Tracking Details")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TRACKING_DETAIL")
            rows = cursor.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Product ID", "Product Name", "Price", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No tracking details found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()


    # --- UPDATE CUSTOMER ---
    elif choice == "Update Customer":
        st.header("✏️ Update Customer Info")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
            customers = cursor.fetchall()
            cursor.close()
            conn.close()

            if customers:
                customer_dict = {f"{cid} - {name}": cid for cid, name in customers}
                selected = st.selectbox("Select Customer to Update", list(customer_dict.keys()))
                selected_id = customer_dict[selected]

                # Fetch existing details for the selected customer
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT Customer_name, Customer_address, Customer_contact FROM CUSTOMER WHERE Customer_id = %s", (selected_id,))
                cust = cursor.fetchone()
                cursor.close()
                conn.close()

                if cust:
                    with st.form("update_customer_form"):
                        name = st.text_input("Customer Name", value=cust[0])
                        address = st.text_input("Customer Address", value=cust[1])
                        contact = st.text_input("Customer Contact", value=cust[2])

                        if st.form_submit_button("Update Customer"):
                            if name and address and contact:
                                try:
                                    conn = get_connection()
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "UPDATE CUSTOMER SET Customer_name = %s, Customer_address = %s, Customer_contact = %s WHERE Customer_id = %s",
                                        (name, address, contact, selected_id)
                                    )
                                    conn.commit()
                                    st.success("✅ Customer updated successfully!")
                                except Exception as e:
                                    st.error(f"❌ Error updating customer: {e}")
                                finally:
                                    cursor.close()
                                    conn.close()
                            else:
                                st.warning("⚠️ Please fill all fields.")
                else:
                    st.error("❌ Customer not found.")
            else:
                st.info("ℹ️ No customers available to update.")
        except Exception as e:
            st.error(f"❌ Error fetching customers: {e}")

# --- DELETE CUSTOMER ---
    elif choice == "Delete Customer":
        st.header("🗑️ Delete Customer")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
            customers = cursor.fetchall()
            cursor.close()
            conn.close()

            if customers:
                customer_dict = {f"{cid} - {name}": cid for cid, name in customers}
                selected = st.selectbox("Select Customer to Delete", list(customer_dict.keys()))
                selected_id = customer_dict[selected]

                if st.button("Delete Customer"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM CUSTOMER WHERE Customer_id = %s", (selected_id,))
                        conn.commit()
                        st.success("✅ Customer deleted successfully!")
                        st.experimental_rerun()  # Note: Replace this with st.experimental_rerun() if your Streamlit version supports it, otherwise use st.experimental_set_query_params or other workaround.
                    except Exception as e:
                        st.error(f"❌ Error deleting customer: {e}")
                    finally:
                        cursor.close()
                        conn.close()
            else:
                st.info("ℹ️ No customers available to delete.")
        except Exception as e:
            st.error(f"❌ Error fetching customers: {e}")

# --- LOGOUT ---
    elif choice == "Logout":
        st.success("🔒 Logged out successfully!")
        st.session_state.clear()
        st.experimental_rerun()

# --- FOOTER ---
st.markdown("""
<hr style="margin-top: 40px; border: 1px solid #ddd;">
<div style='text-align: center; color: gray; font-size: 14px; padding: 10px;'>
    Made By Neha P, Niharika TN, Parnika Nag, Reshika Hima Gowda
</div>
""", unsafe_allow_html=True)

