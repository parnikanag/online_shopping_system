import streamlit as st
import pandas as pd
from db_connection import get_connection

st.set_page_config(page_title="Online Shopping System", layout="wide")
st.title("🛒 Online Shopping System")
# Custom background color - light purple
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #f3e8ff90;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Header styling */
    h1, h2, h3 {
        color: #5b21b6;
        text-shadow: 1px 1px 1px #ddd;
    }

    /* Form containers */
    .block-container {
        padding: 2rem;
    }

    /* Stylish input boxes */
    input, textarea {
        border: 1px solid #d8b4fe !important;
        border-radius: 8px !important;
        background-color: #faf5ff !important;
        padding: 10px !important;
    }

    /* Buttons */
    button {
        background-color: #8b5cf6 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    button:hover {
        background-color: #7c3aed !important;
        transform: scale(1.03);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #e9d5ff;
        color: black;
        font-size: 16px;
    }

    /* Table styling */
    .stDataFrame {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    /* Success & error messages */
    .stAlert {
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer"]
choice = st.sidebar.radio("📋 Select Operation", menu)

# Add Customer
if choice == "Add Customer":
    st.header("➕ Add New Customer")
    with st.form("add_customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name", placeholder="e.g. Parnika Nag")
            customer_address = st.text_input("Customer Address", placeholder="e.g. Bengaluru,Karnataka")
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
    st.header("✏️ Update Customer")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Customer_id, Customer_name FROM CUSTOMER")
        customer_list = cursor.fetchall()
        customer_dict = {f"{cid} - {name}": cid for cid, name in customer_list}
        if customer_list:
            selected = st.selectbox("Select Customer", list(customer_dict.keys()))
            selected_id = customer_dict[selected]

            cursor.execute("SELECT * FROM CUSTOMER WHERE Customer_id = %s", (selected_id,))
            customer = cursor.fetchone()
            if customer:
                with st.form("update_form"):
                    name = st.text_input("Customer Name", value=customer[1])
                    address = st.text_input("Customer Address", value=customer[2])
                    contact = st.text_input("Customer Contact", value=customer[3])
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
            st.info("ℹ️ No customers available.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()
