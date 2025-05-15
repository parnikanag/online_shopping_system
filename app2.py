import streamlit as st
import pandas as pd
from db_connection import get_connection

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- AUTH FUNCTIONS ----------
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

# ---------- LOGIN / SIGNUP ----------
if not st.session_state.logged_in:
    st.set_page_config(page_title="Online Shopping System", layout="centered")
    st.markdown(
        """
        <div style='background-color: #c4b5fd; padding: 30px; border-radius: 15px; text-align: center;'>
            <h1 style='color: #4c1d95;'>Online Shopping System</h1>
            <p style='font-size: 18px; color: #5b21b6;'>DBMS Mini Project Login</p>
        </div>
        """, unsafe_allow_html=True
    )

    option = st.radio("Choose Option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials.")
    else:
        if st.button("Sign Up"):
            if signup_user(username, password):
                st.success("✅ Account created. Please log in.")
            else:
                st.warning("⚠️ Username already exists.")
else:
    # ---------- MAIN APP AFTER LOGIN ----------
    st.set_page_config(page_title="Online Shopping System", layout="wide")

    # Header
    st.markdown(
        """
        <div style='background-color: #c4b5fd; padding: 20px; border-radius: 15px; text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
            <h1 style='color: #4c1d95;'>Online Shopping System</h1>
            <p style='font-size: 18px; color: #5b21b6;'>DBMS Mini Project Showcase</p>
        </div>
        """, unsafe_allow_html=True
    )

    menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer", "Logout"]
    choice = st.sidebar.radio("📋 Select Operation", menu)

    # Add Customer
    if choice == "Add Customer":
        st.header("➕ Add New Customer")
        with st.form("add_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                customer_name = st.text_input("Customer Name", placeholder="e.g. Parnika Nag")
                customer_address = st.text_input("Customer Address", placeholder="e.g. Bengaluru, Karnataka")
            with col2:
                customer_contact = st.text_input("Customer Contact", placeholder="e.g. 9876543210")

            submitted = st.form_submit_button("Add Customer")
            if submitted:
                if customer_name and customer_address and customer_contact:
                    conn = get_connection()
                    cursor = conn.cursor()
                    try:
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

    # View Customers
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

    # Update Customer
    elif choice == "Update Customer":
        st.header("✏️ Update Customer Info")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
            customers = cursor.fetchall()
            customer_dict = {f"{cid} - {name}": cid for cid, name in customers}
            if customers:
                selected = st.selectbox("Select Customer", list(customer_dict.keys()))
                selected_id = customer_dict[selected]

                cursor.execute("SELECT * FROM CUSTOMER WHERE Customer_id = %s", (selected_id,))
                cust = cursor.fetchone()
                if cust:
                    with st.form("update_form"):
                        name = st.text_input("Name", value=cust[1])
                        address = st.text_input("Address", value=cust[2])
                        contact = st.text_input("Contact", value=cust[3])
                        update_btn = st.form_submit_button("Update")
                        if update_btn:
                            cursor.execute(
                                "UPDATE CUSTOMER SET Customer_name=%s, Customer_address=%s, Customer_contact=%s WHERE Customer_id=%s",
                                (name, address, contact, selected_id)
                            )
                            conn.commit()
                            st.success("✅ Customer updated successfully!")
            else:
                st.info("ℹ️ No customers available.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # Delete Customer
    elif choice == "Delete Customer":
        st.header("🗑️ Delete Customer")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
            customers = cursor.fetchall()
            if customers:
                customer_dict = {f"{cid} - {name}": cid for cid, name in customers}
                selected = st.selectbox("Select Customer to Delete", list(customer_dict.keys()))
                selected_id = customer_dict[selected]

                if st.button("Delete Customer"):
                    cursor.execute("DELETE FROM CUSTOMER WHERE Customer_id = %s", (selected_id,))
                    conn.commit()
                    st.success("✅ Customer deleted successfully!")
            else:
                st.info("ℹ️ No customers found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()

    # Logout
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    # Footer
    st.markdown(
        """
        <hr style="margin-top: 40px; border: 1px solid #ddd;">
        <div style='text-align: center; color: gray; font-size: 14px; padding: 10px;'>
            Made By Neha P, Niharika TN, Parnika Nag, Reshika Hima Gowda
        </div>
        """,
        unsafe_allow_html=True
    )
