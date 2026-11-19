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


def show_cover(url, fallback_url=None):
    for candidate in dict.fromkeys((url, fallback_url)):
        cover = load_cover(candidate)
        if cover:
            try:
                st.image(cover, width=144)
                return
            except Exception:
                # Invalid image data should use the next available cover.
                continue
    st.image(str(DEFAULT_COVER), width=144)


def show_home():
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
        return
    if not subscriptions:
        st.info("Add a podcast using its RSS feed URL to get started.")
    for podcast in subscriptions:
        with st.container(border=True):
            show_cover(podcast["cover_url"])
            st.subheader(podcast["title"])
            st.text(podcast["description"] or "No description available")
            if st.button("See Episodes", key=f'episodes_{podcast["id"]}'):
                st.session_state.selected_podcast = podcast
                st.rerun()


def show_episodes():
    if st.button("Back to Podcasts"):
        del st.session_state.selected_podcast
        st.rerun()
    podcast = st.session_state.selected_podcast
    st.header(podcast["title"])
    st.button("Reload Episodes")
    st.caption("Up to 20 episodes in feed order")
    try:
        with st.spinner("Loading episodes..."):
            episodes = service.list_episodes(podcast["id"])
    except service.SubscriptionError as exc:
        st.error(str(exc))
        return
    if not episodes:
        st.info("No episodes available")
    for episode in episodes:
        with st.container(border=True):
            show_cover(episode["cover_url"], podcast["cover_url"])
            st.subheader(episode["title"])
            st.caption(episode["date"] or "Date unavailable")
            st.text(episode["description"] or "No description available")


if "selected_podcast" in st.session_state:
    show_episodes()
else:
    show_home()
