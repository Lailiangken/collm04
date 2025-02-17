import streamlit as st
import logging


class StreamlitHandler(logging.Handler):
    def __init__(self, log_area):
        super().__init__()
        self.log_area = log_area
        self.log_data = ""
        self.log_area = log_area.empty()

    def emit(self, record):
        log_entry = self.format(record)
        self.log_data += log_entry + "\n\n"
        self.log_area.markdown(f"\n{self.log_data}\n")



def render_logging_section():
    st.header("ログ")
    with st.expander("ログを表示/非表示", expanded=False):
        log_display = st.container()
        streamlit_handler = StreamlitHandler(log_display)
        streamlit_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(streamlit_handler)
