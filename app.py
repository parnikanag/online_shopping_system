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

    menu = ["Add Customer", "Add Supplier", "Add Product", "Add Order",
    "Add Tracking Detail", "Add Admin", "View Customers",
    "View Suppliers", "View Products", "View Orders", "View Tracking Detail", "View Admins",
    "Update Customer", "Delete Customer",
    "Update Supplier", "Delete Supplier",
    "Update Product", "Delete Product",
    "Update Order", "Delete Order",
    "Update Tracking Detail", "Delete Tracking Detail",
    "Update Admin", "Delete Admin", "Clear All Data",
    "Logout"]


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


        # --- VIEW TRACKING DETAIL ---
    elif choice == "View Tracking Detail":
        st.header("🚚 Tracking Detail List")
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
        st.write("DEBUG: Entered View Tracking Details section")  

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT TD.Track_id, TD.Prod_id, P.Prod_name, TD.Prod_price, TD.Prod_status
                FROM TRACKING_DETAIL TD
                LEFT JOIN PRODUCT P ON TD.Prod_id = P.Prod_id
            """)
            rows = cursor.fetchall()
            st.write("Rows fetched:", rows)  # Debug output
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Product ID", "Product Name", "Price", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ No tracking details found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
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

    # --- UPDATE SUPPLIER---

    elif choice == "Update Supplier":
        st.header("🔄 Update Supplier")
        
        supplier_id = st.text_input("Enter Supplier ID to update")
        
        if st.button("Load Supplier"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM SUPPLIER WHERE Supplier_id = %s", (supplier_id,))
                data = cursor.fetchone()
                if data:
                    # Use session state to hold values
                    st.session_state['name'] = data[1]
                    st.session_state['address'] = data[2]
                else:
                    st.warning("⚠️ Supplier not found")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()
        
        if 'name' in st.session_state and 'address' in st.session_state:
            name = st.text_input("Supplier Name", value=st.session_state['name'])
            address = st.text_area("Supplier Address", value=st.session_state['address'])
            
            if st.button("Update"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE SUPPLIER SET Supplier_name=%s, Supplier_address=%s WHERE Supplier_id=%s",
                        (name, address, supplier_id)
                    )
                    conn.commit()
                    st.success("✅ Supplier updated successfully")
                    # Clear session state after update
                    del st.session_state['name']
                    del st.session_state['address']
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()


    # --- UPDATE PRODUCT ---
    elif choice == "Update Product":
        st.header("🔄 Update Product")
        
        product_id = st.text_input("Enter Product ID to update")
        
        if st.button("Load Product"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM PRODUCT WHERE Prod_id = %s", (product_id,))
                data = cursor.fetchone()
                if data:
                    # Store values in session state for persistence
                    st.session_state['prod_name'] = data[1]
                    st.session_state['prod_price'] = data[2]
                else:
                    st.warning("⚠️ Product not found")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()
        
        # Show input fields only if data loaded
        if 'prod_name' in st.session_state and 'prod_price' in st.session_state:
            name = st.text_input("Product Name", value=st.session_state['prod_name'])
            price = st.number_input("Product Price", value=float(st.session_state['prod_price']), format="%.2f")
            
            if st.button("Update"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE PRODUCT SET Prod_name=%s, Prod_price=%s WHERE Prod_id=%s",
                        (name, price, product_id)
                    )
                    conn.commit()
                    st.success("✅ Product updated successfully")
                    # Clear session state after update
                    del st.session_state['prod_name']
                    del st.session_state['prod_price']
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

   

    # --- UPDATE ORDER ---
    elif choice == "Update Order":
        st.header("🔄 Update Order")
        order_no_str = st.text_input("Enter Order No to update")

        if st.button("Load Order"):
            try:
                order_no = int(order_no_str)
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ORDERS WHERE Order_no = %s", (order_no,))
                data = cursor.fetchone()
                if data:
                    st.session_state['order_no'] = order_no
                    st.session_state['order_date'] = data[1]
                    st.session_state['order_amount'] = float(data[2])
                    st.session_state['customer_id'] = str(data[3])
                else:
                    st.warning("⚠️ Order not found")
            except ValueError:
                st.error("❌ Please enter a valid Order No (number)")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()

        if 'order_no' in st.session_state:
            order_date = st.date_input("Order Date", value=st.session_state['order_date'])
            order_amount = st.number_input("Order Amount", value=st.session_state['order_amount'], format="%.2f")
            customer_id_str = st.text_input("Customer ID", value=st.session_state['customer_id'])

            if st.button("Update"):
                try:
                    order_no = st.session_state['order_no']
                    order_amount_float = float(order_amount)
                    customer_id = int(customer_id_str)  # Convert Customer ID to int!

                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE ORDERS SET Order_date=%s, Order_amount=%s, Customer_id=%s WHERE Order_no=%s",
                        (order_date, order_amount_float, customer_id, order_no)
                    )
                    conn.commit()

                    if cursor.rowcount > 0:
                        st.success("✅ Order updated successfully")
                        # Clear session state to reset form
                        del st.session_state['order_no']
                        del st.session_state['order_date']
                        del st.session_state['order_amount']
                        del st.session_state['customer_id']
                    else:
                        st.warning("⚠️ No rows updated. Please check the Order No.")
                except ValueError:
                    st.error("❌ Customer ID must be a number.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

    # --- UPDATE TRACKING DETAIL ---
    elif choice == "Update Tracking Detail":
        st.header("🔄 Update Tracking Detail")
        tracking_id_input = st.text_input("Enter Tracking ID to update")

        if st.button("Load Detail"):
            if not tracking_id_input.isdigit():
                st.error("❌ Tracking ID must be a number.")
            else:
                tracking_id = int(tracking_id_input)
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM TRACKING_DETAIL WHERE Tracking_id = %s", (tracking_id,))
                    data = cursor.fetchone()
                    if data:
                        st.session_state['tracking_id'] = tracking_id
                        st.session_state['prod_id'] = data[1]
                        st.session_state['prod_name'] = data[2]
                        st.session_state['prod_price'] = float(data[3])
                        st.session_state['prod_status'] = data[4]
                    else:
                        st.warning("⚠️ Tracking detail not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

        # Display update form if data was loaded
        if 'tracking_id' in st.session_state:
            new_prod_id = st.text_input("Product ID", value=str(st.session_state['prod_id']))
            new_prod_name = st.text_input("Product Name", value=st.session_state['prod_name'])
            new_prod_price = st.number_input("Product Price", value=st.session_state['prod_price'], format="%.2f")
            new_prod_status = st.text_input("Product Status", value=st.session_state['prod_status'])

            if st.button("Update"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE TRACKING_DETAIL SET Prod_id = %s, Prod_name = %s, Prod_price = %s, Prod_status = %s WHERE Tracking_id = %s",
                        (new_prod_id, new_prod_name, new_prod_price, new_prod_status, st.session_state['tracking_id']))
                    conn.commit()
                    if cursor.rowcount > 0:
                        st.success("✅ Tracking detail updated successfully")
                    else:
                        st.warning("⚠️ No changes were made.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

    # --- UPDATE ADMIN ---
    elif choice == "Update Admin":
        st.header("🔄 Update Admin")
        admin_id_input = st.text_input("Enter Admin ID to update")

        if st.button("Load Admin"):
            if not admin_id_input.isdigit():
                st.error("❌ Admin ID must be a number.")
            else:
                admin_id = int(admin_id_input)
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM ADMIN WHERE Admin_id = %s", (admin_id,))
                    data = cursor.fetchone()
                    if data:
                        # Store values in session state so they persist across reruns
                        st.session_state['admin_id'] = admin_id
                        st.session_state['admin_name'] = data[1]
                        st.session_state['role'] = data[2]
                    else:
                        st.warning("⚠️ Admin not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

        # Display update form if data is loaded
        if 'admin_id' in st.session_state:
            new_name = st.text_input("Admin Name", value=st.session_state['admin_name'])
            new_role = st.text_input("Role", value=st.session_state['role'])

            if st.button("Update"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE ADMIN SET Admin_name = %s, Role = %s WHERE Admin_id = %s",
                                (new_name, new_role, st.session_state['admin_id']))
                    conn.commit()
                    if cursor.rowcount > 0:
                        st.success("✅ Admin updated successfully")
                    else:
                        st.warning("⚠️ No update made (maybe same values)")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()


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
                    except Exception as e:
                        st.error(f"❌ Error deleting customer: {e}")
                    finally:
                        cursor.close()
                        conn.close()
            else:
                st.info("ℹ️ No customers available to delete.")
        except Exception as e:
            st.error(f"❌ Error fetching customer list: {e}")

    # --- DELETE SUPPLIER ---
    elif choice == "Delete Supplier":
        st.header("🗑️ Delete Supplier")
        supplier_id = st.text_input("Enter Supplier ID to delete")
        if st.button("Delete"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM SUPPLIER WHERE SUPPLIER_ID = %s", (supplier_id,))
                conn.commit()
                st.success("✅ Supplier deleted successfully")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()
# --- DELETE PRODUCT ---
    elif choice == "Delete Product":
        st.header("🗑️ Delete Product")
        product_id = st.text_input("Enter Product ID to delete")
        if st.button("Delete"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM PRODUCT WHERE Prod_id = %s", (product_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    st.success("✅ Product deleted successfully")
                else:
                    st.warning("⚠️ Product ID not found")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()


    # --- DELETE ORDER ---
    elif choice == "Delete Order":
        st.header("🗑️ Delete Order")
        order_id = st.text_input("Enter Order ID to delete")

        if st.button("Delete"):
            try:
                order_id_int = int(order_id)  # Convert to int since Order_no is INT
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ORDERS WHERE Order_no = %s", (order_id_int,))
                conn.commit()

                if cursor.rowcount > 0:
                    st.success("✅ Order deleted successfully")
                else:
                    st.warning("⚠️ Order not found. Nothing was deleted.")
            except ValueError:
                st.error("❌ Please enter a valid numeric Order ID.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()


    # --- DELETE TRACKING DETAIL ---
    elif choice == "Delete Tracking Detail":
        st.header("🗑️ Delete Tracking Detail")
        tracking_id = st.text_input("Enter Tracking ID to delete")
        if st.button("Delete"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM TRACKING_DETAIL WHERE TRACKING_ID = %s", (tracking_id,))
                conn.commit()
                st.success("✅ Tracking detail deleted successfully")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()

    # --- DELETE ADMIN ---
    elif choice == "Delete Admin":
        st.header("🗑️ Delete Admin")
        admin_id = st.text_input("Enter Admin ID to delete")
        if st.button("Delete"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ADMIN WHERE ADMIN_ID = %s", (admin_id,))
                conn.commit()
                st.success("✅ Admin deleted successfully")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()
     # --- Clear All the data in the database ---
    elif choice == "Clear All Data":
        st.header("⚠️ Clear All Data")
        st.warning("This will delete ALL data from all tables. This action cannot be undone.")

        if st.button("Clear Database"):
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Order matters if you have foreign key constraints. Delete child tables first.

                cursor.execute("DELETE FROM TRACKING_DETAIL")
                cursor.execute("DELETE FROM ORDERS")
                cursor.execute("DELETE FROM PRODUCT")
                cursor.execute("DELETE FROM CUSTOMER")
                cursor.execute("DELETE FROM SUPPLIER")
                cursor.execute("DELETE FROM ADMIN")
                cursor.execute("DELETE FROM USERS")

                conn.commit()
                st.success("✅ All data cleared successfully!")
            except Exception as e:
                st.error(f"❌ Error clearing data: {e}")
            finally:
                cursor.close()
                conn.close()



# --- LOGOUT ---
    elif choice == "Logout":
        st.success("🔒 Logged out successfully!")
        st.session_state.clear()
        st.rerun()

# --- FOOTER ---
st.markdown("""
<hr style="margin-top: 40px; border: 1px solid #ddd;">
<div style='text-align: center; color: gray; font-size: 14px; padding: 10px;'>
    Made By Neha P, Niharika TN, Parnika Nag, Reshika Hima Gowda
</div>
""", unsafe_allow_html=True)

