import streamlit as st
from get_character_info import filter_Data

st.set_page_config(
    page_title="Character Info Extractor",
    layout="centered"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-family: 'Arial', sans-serif;
        font-size: 32px;
        color: #4a4a4a;
        text-align: center;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 12px;
        color: #808080;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="header-title">Character Info Extractor</h1>', unsafe_allow_html=True)

with st.container():
    st.markdown("### Enter the Character Name")
    name = st.text_input("Character Name:", placeholder="Type the character name here...")

if st.button("Extract Information"):
    if not name.strip():
        st.warning("Please enter a character name before proceeding.")
    else:
        with st.spinner("Fetching character information..."):
            result = filter_Data(name)
        st.markdown("### Extracted Information")
        st.code(result, language='json')
