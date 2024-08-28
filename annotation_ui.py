import streamlit as st
from lorem_text import lorem
import pandas as pd
from loguru import logger
from annotations import db

st.set_page_config(page_title="Pesquise os diários da Assembleia Constituinte (1987-1988)", layout="wide")


sent_db = db.Sentence()

if "sent_ids" not in st.session_state.keys():
    st.session_state['sent_ids'] = sent_db.list_ids()

if "item_n" not in st.session_state.keys():
    st.session_state['item_n'] = 1

clicked = st.button(f"Próximo item > {st.session_state['item_n'] + 1}")
if clicked:
    st.session_state['item_n'] = st.session_state['item_n'] + 1
    logger.info("item_n is now {}".format(st.session_state['item_n']))
    st.rerun()


current_sent = sent_db.fetch(_id=st.session_state['item_n'])

col1, col2 = st.columns(2)

with col1:
    st.text_area(str(current_sent[0]), current_sent[1], height=400)

with col2:
    updated_text = st.text_area(str(current_sent[0])+"_annotated", current_sent[1], height=400)

if current_sent[1] != updated_text:
    sent_db.update(
            _id=current_sent[0],
            revised_sentence=updated_text
            )
    logger.info("Updated sentence with id {}".format(current_sent[0]))
    


