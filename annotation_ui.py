from logging import disable
import streamlit as st
from loguru import logger
from annotations import db

st.set_page_config(page_title="Pesquise os diários da Assembleia Constituinte (1987-1988)", layout="wide")


sent_db = db.Sentence()

sent_db.create_table()

if "sent_ids" not in st.session_state.keys():
    st.session_state['sent_ids'] = sent_db.list_ids(random=True)
    logger.info(st.session_state['sent_ids'][:20])

if "item_n" not in st.session_state.keys():
    st.session_state['item_n'] = 1

if "last_annotation" not in st.session_state.keys():
    st.session_state['last_annotation'] = None

header_col_1, header_col_2 = st.columns(2)

with header_col_1:
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        previous = st.button(f"< Último Item - {st.session_state['item_n'] - 1}", disabled=(st.session_state['item_n'] == 1), use_container_width=True)

    with button_col2:
        next = st.button(f"Próximo item > {st.session_state['item_n'] + 1}", use_container_width=True)

    if previous:
        st.session_state['item_n'] = st.session_state['item_n'] - 1
        logger.info("item_n is now {}".format(st.session_state['item_n']))
        st.rerun()

    if next:
        st.session_state['item_n'] = st.session_state['item_n'] + 1
        logger.info("item_n is now {}".format(st.session_state['item_n']))
        st.rerun()

with header_col_2:
    st.write("Você já anotou {} frases.".format(sent_db.count_rows_w_annotations()))

current_sent = sent_db.fetch(_id=st.session_state['sent_ids'][st.session_state['item_n']])

col1, col2 = st.columns(2)

with col1:
    st.text_area(str(current_sent[0]), current_sent[1], height=400)

with col2:
    updated_text = st.text_area(str(current_sent[0])+"_annotated", current_sent[1] if not current_sent[2] else current_sent[2], height=400)

if (current_sent[1] != updated_text) and (updated_text != st.session_state["last_annotation"]):
    sent_db.update(
            _id=current_sent[0],
            revised_sentence=updated_text
            )
    st.session_state["last_annotation"] = updated_text
    logger.info("Updated sentence with id {}".format(current_sent[0]))
    

