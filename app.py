import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Kafka Says ?")

st.header("Get a Random Quote")
category = st.text_input("Category (optional)")
if st.button("Get Quote"):
    endpoint = f"{API_URL}/quote"
    if category:
        endpoint += f"?category={category}"
    response = requests.get(endpoint)
    if response.status_code == 404:
        st.error("No quote found for that category.")

if st.checkbox("Show all quotes"):
    response = requests.get(f"{API_URL}/quotes")
    if response.status_code == 200:
        st.subheader("All Quotes:")
        for q in response.json():
            st.markdown(f'> "{q["quote"]}" — ({q["category"]})')

st.header("Add a New Quote")
with st.form("add_quote_form"):
    text = st.text_area("Quote")
    category = st.text_input("Category")
    submitted = st.form_submit_button("Add Quote")
    if submitted:
        payload = {"quote": text, "category": category}
        response = requests.post(f"{API_URL}/quote", json=payload)
        if response.status_code == 200:
            st.success("Quote added successfully!")
        else:
            st.error("Failed to add quote.")

# Delete a quote
st.header("Delete a Quote")
quote_id = st.number_input("Enter quote ID to delete", min_value=1, step=1)
if st.button("Delete Quote"):
    response = requests.delete(f"{API_URL}/quote/{quote_id}")
    if response.status_code == 200:
        st.success("Quote deleted")
    else:
        st.error("Quote not found")
