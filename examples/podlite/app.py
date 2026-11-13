from pathlib import Path

import streamlit as st

from podlite import service

DEFAULT_COVER = Path(__file__).resolve().parent / "assets" / "default-cover.svg"


def open_episodes(podcast_id):
    st.session_state.page = "episodes"
    st.session_state.podcast_id = podcast_id
    st.session_state.episodes = []
    st.session_state.visible_episodes = 10
    st.session_state.episodes_loaded = False
    st.session_state.episode_error = None


def back_to_podcasts():
    st.session_state.page = "podcasts"
    st.session_state.podcast_id = None
    st.session_state.episodes = []


def load_more_episodes():
    st.session_state.visible_episodes += 10


def show_episodes():
    st.button("Back to Podcasts", key="back_to_podcasts", on_click=back_to_podcasts)
    try:
        podcasts = service.list_podcasts()
        podcast = next(
            (podcast for podcast in podcasts
             if podcast["id"] == st.session_state.get("podcast_id")),
            None,
        )
        if podcast is None:
            st.error("Podcast not found. Return to your subscriptions.")
            return
    except service.PodcastError as error:
        st.error(str(error))
        return

    st.image(podcast["image_url"] or str(DEFAULT_COVER), width=120)
    st.subheader(podcast["title"])
    st.subheader("Episodes")
    if not st.session_state.episodes_loaded:
        try:
            with st.spinner("Loading episodes…"):
                st.session_state.episodes = service.list_episodes(podcast["id"])
        except service.PodcastError as error:
            st.session_state.episode_error = str(error)
        st.session_state.episodes_loaded = True

    if st.session_state.episode_error:
        st.error(st.session_state.episode_error)
        return
    episodes = st.session_state.episodes
    if not episodes:
        st.info("No episodes available")
        return
    for episode in episodes[:st.session_state.visible_episodes]:
        with st.container(border=True):
            cover, details = st.columns([1, 4])
            with cover:
                st.image(
                    episode.get("image_url") or podcast["image_url"] or str(DEFAULT_COVER),
                    width=120,
                )
            with details:
                st.write(episode["title"])
                date = episode["published_at"]
                st.caption(date.strftime("%Y-%m-%d %H:%M UTC") if date else "Date unavailable")
                st.text(episode["description"])
    if st.session_state.visible_episodes < len(episodes):
        st.button("Load more", key="load_more", on_click=load_more_episodes)


def show_podcasts():
    with st.form("add_podcast"):
        url = st.text_input("Podcast RSS URL", placeholder="https://example.com/feed.xml")
        submitted = st.form_submit_button("Add podcast")

    if submitted:
        try:
            with st.spinner("Adding podcast…"):
                title = service.add_podcast(url)
            st.success(f"Added: {title}")
        except service.PodcastError as error:
            st.error(str(error))

    st.subheader("Subscriptions")
    try:
        podcasts = service.list_podcasts()
        if not podcasts:
            st.info("No podcasts yet. Add one using its RSS URL.")
        for podcast in podcasts:
            with st.container(border=True):
                cover, details = st.columns([1, 4])
                with cover:
                    st.image(podcast["image_url"] or str(DEFAULT_COVER), width=120)
                with details:
                    st.write(podcast["title"])
                    st.text(podcast["description"] or "No description available")
                    st.button(
                        "See Episodes", key=f"see_episodes_{podcast['id']}",
                        on_click=open_episodes, args=(podcast["id"],),
                    )
    except service.PodcastError as error:
        st.error(str(error))


st.title("Podlite")
if st.session_state.get("page") == "episodes":
    show_episodes()
else:
    show_podcasts()
