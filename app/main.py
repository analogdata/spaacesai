import streamlit as st
from plugins import index
from plugins import home
from plugins import quo
from plugins import genie
from plugins import spaaces360


# Define a function to navigate between pages
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Check if the session state for the current page is set, otherwise set it to 'Home' # Noqa
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"


# Sidebar navigation
st.sidebar.title("Modules")

st.sidebar.button(
    "Spaaces AI",
    on_click=navigate_to,
    use_container_width=True,
    args=("index",),
)
st.sidebar.button(
    "Spaaces Quo",
    on_click=navigate_to,
    use_container_width=True,
    args=("quo",),
)
st.sidebar.button(
    "Spaaces Genie",
    on_click=navigate_to,
    use_container_width=True,
    args=("genie",),
)
st.sidebar.button(
    "Spaaces 360",
    on_click=navigate_to,
    use_container_width=True,
    args=("spaaces360",),
)
st.sidebar.button(
    "Spaaces Home",
    on_click=navigate_to,
    use_container_width=True,
    args=("Home",),
)

# Display the current page
page = st.session_state.current_page

if page == "index":
    index.show()
elif page == "Home":
    home.show()
elif page == "quo":
    quo.show()
elif page == "genie":
    genie.show()
elif page == "spaaces360":
    spaaces360.show()
