import streamlit as st

st.title("RPA Streamlit Demo")

name = st.text_input("Enter your name:")

if st.button("Greet Me"):
    if name:
        st.success(f"Hello, {name}! Welcome to the RPA Streamlit Demo.") 
    else:
        st.warning("Please enter your name to be greeted.")    
  
