import streamlit as st
from db_connection import get_connection

st.title("🛒 Online Shopping System")

menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Customer":
    st.subheader("Add New Customer")
    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        customer_address = st.text_input("Customer Address")
    with col2:
        customer_contact = st.text_input("Customer Contact")

    if st.button("Add Customer"):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO CUSTOMER (Customer_name, Customer_address, Customer_contact) VALUES (%s, %s, %s)"
        values = (customer_name, customer_address, customer_contact)
        try:
            cursor.execute(query, values)
            conn.commit()
            st.success("✅ Customer added successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()
    # Add insert form here
elif choice == "View Customers":
    st.subheader("Customer List")
    
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM CUSTOMER"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Convert the result into a DataFrame for easy display
        import pandas as pd
        customer_df = pd.DataFrame(result, columns=["Customer ID", "Customer Name", "Customer Address", "Customer Contact"])
        
        # Display the DataFrame in Streamlit
        st.dataframe(customer_df)
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

    # Add select logic here
elif choice == "Update Customer":
    st.subheader("Update Customer Info")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Fetch customers for selection
    query = "SELECT Customer_id, Customer_name FROM CUSTOMER"
    cursor.execute(query)
    customers = cursor.fetchall()
    
    # Create a selectbox for customer selection
    customer_options = [f"{customer[1]} (ID: {customer[0]})" for customer in customers]
    selected_customer = st.selectbox("Select Customer to Update", customer_options)
    
    if selected_customer:
        # Extract customer ID from selected option
        selected_customer_id = int(selected_customer.split(" (ID: ")[-1][:-1])
        
        # Fetch customer details
        query = f"SELECT * FROM CUSTOMER WHERE Customer_id = {selected_customer_id}"
        cursor.execute(query)
        customer_details = cursor.fetchone()
        
        # Display the current customer information in text inputs
        customer_name = st.text_input("Customer Name", customer_details[1])
        customer_address = st.text_input("Customer Address", customer_details[2])
        customer_contact = st.text_input("Customer Contact", customer_details[3])
        
        # Update button
        if st.button("Update Customer"):
            update_query = """UPDATE CUSTOMER
                              SET Customer_name = %s, Customer_address = %s, Customer_contact = %s
                              WHERE Customer_id = %s"""
            update_values = (customer_name, customer_address, customer_contact, selected_customer_id)
            
            try:
                cursor.execute(update_query, update_values)
                conn.commit()
                st.success("✅ Customer updated successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()

    # Add update logic here
elif choice == "Delete Customer":
    st.subheader("Delete a Customer")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Fetch customers for selection
    query = "SELECT Customer_id, Customer_name FROM CUSTOMER"
    cursor.execute(query)
    customers = cursor.fetchall()
    
    # Create a selectbox for customer selection
    customer_options = [f"{customer[1]} (ID: {customer[0]})" for customer in customers]
    selected_customer = st.selectbox("Select Customer to Delete", customer_options)
    
    if selected_customer:
        # Extract customer ID from selected option
        selected_customer_id = int(selected_customer.split(" (ID: ")[-1][:-1])
        
        # Display the selected customer's details
        query = f"SELECT * FROM CUSTOMER WHERE Customer_id = {selected_customer_id}"
        cursor.execute(query)
        customer_details = cursor.fetchone()
        
        st.write("Customer Details:")
        st.write(f"Name: {customer_details[1]}")
        st.write(f"Address: {customer_details[2]}")
        st.write(f"Contact: {customer_details[3]}")
        
        # Confirmation checkbox
        confirm_delete = st.checkbox("Confirm Deletion")
        
        if confirm_delete and st.button("Delete Customer"):
            delete_query = "DELETE FROM CUSTOMER WHERE Customer_id = %s"
            try:
                cursor.execute(delete_query, (selected_customer_id,))
                conn.commit()
                st.success("✅ Customer deleted successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                conn.close()

    # Add delete logic here
