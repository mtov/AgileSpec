"""Run with: python -m streamlit run app.py."""

from pathlib import Path

import streamlit as st

from podlite import service

DEFAULT_COVER = Path(__file__).resolve().parent / "assets" / "default-cover.svg"

st.set_page_config(page_title="PodLite", layout="centered")
st.title("PodLite")


@st.cache_data(ttl=3600, show_spinner=False)
def load_cover(url):
    return service.get_cover(url)


with st.form("subscribe"):
    url = st.text_input("RSS feed URL")
    submitted = st.form_submit_button("Subscribe")

if submitted:
    try:
        with st.spinner("Subscribing..."):
            podcast = service.subscribe(url)
        st.success(f'Subscribed to {podcast["title"]}.')
    except service.SubscriptionError as exc:
        st.error(str(exc))

st.header("My Podcasts")
try:
    subscriptions = service.list_subscriptions()
except service.SubscriptionError as exc:
    st.error(str(exc))
    subscriptions = None

if subscriptions == []:
    st.info("Add a podcast using its RSS feed URL to get started.")

for podcast in subscriptions or []:
    with st.container(border=True):
        cover = load_cover(podcast["cover_url"])
        if cover:
            try:
                st.image(cover, width=144)
            except Exception:
                # Invalid image bytes should not prevent reading subscriptions.
                st.image(str(DEFAULT_COVER), width=144)
        else:
            st.image(str(DEFAULT_COVER), width=144)
        st.subheader(podcast["title"])
        st.text(podcast["description"] or "No description available")
