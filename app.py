import pandas as pd
import streamlit as st
from src.config.settings import settings
from src.database.database_manager import DatabaseManager
from src.database.db_initializer import DatabaseInitializer
from src.services.sql_service import SQLService
from src.utils.exceptions import SQLAssistantError
from src.utils.logger import logger

EXAMPLE_QUESTIONS = [
    "How many customers are there?",
    "Which customers bought a Laptop?",
    "Which product generated the highest revenue?",
    "What is the total revenue per city?",
    "How many orders were placed in 2024?"
]

st.set_page_config(
    page_title="SQL AI Assistant",
    page_icon="🗄️",
    layout="wide"
)


@st.cache_resource(show_spinner="Starting the SQL assistant...")
def load_resources() -> tuple[SQLService, DatabaseManager]:

    logger.info("Starting SQL AI Assistant UI...")

    DatabaseInitializer().initialize()

    return SQLService(), DatabaseManager()


def fetch_result_table(database: DatabaseManager, query: str | None) -> pd.DataFrame | None:

    if not query:
        return None

    try:
        columns, rows = database.run_query(query)
    except Exception as e:
        logger.warning(f"Unable to load result table: {e}")
        return None

    return pd.DataFrame(rows, columns=columns)


def render_assistant_message(message: dict):

    if message.get("error"):
        st.error(message["content"])
        return

    st.markdown(message["content"])

    queries = message.get("queries") or []
    table = message.get("table")

    if queries:
        with st.expander("Generated SQL", expanded=False):
            for query in queries:
                st.code(query, language="sql")

    if table is not None and not table.empty:
        with st.expander(f"Query result ({len(table)} rows)", expanded=False):
            st.dataframe(table, width="stretch", hide_index=True)

    if message.get("elapsed_time"):
        st.caption(f"Answered in {message['elapsed_time']:.1f}s")


def render_sidebar(database: DatabaseManager, busy: bool):

    with st.sidebar:
        st.header("Database")
        st.caption(f"Model: `{settings.openai_model}`")

        for table, columns in database.get_schema().items():
            with st.expander(f"📋 {table}"):
                st.dataframe(
                    pd.DataFrame(columns),
                    width="stretch",
                    hide_index=True
                )

        st.header("Try asking")

        for question in EXAMPLE_QUESTIONS:
            if st.button(question, width="stretch", disabled=busy):
                st.session_state.pending_question = question

        st.divider()

        if st.button("Clear conversation", width="stretch", type="secondary", disabled=busy):
            st.session_state.messages = []
            st.rerun()


def answer_question(service: SQLService, database: DatabaseManager, question: str) -> dict:

    try:
        response = service.ask(question)
    except SQLAssistantError as e:
        return {"role": "assistant", "content": str(e), "error": True}
    except Exception as e:
        logger.error(f"Unexpected error while answering: {e}")
        return {"role": "assistant", "content": "Something went wrong. Please try again.", "error": True}

    return {
        "role": "assistant",
        "content": response.answer,
        "queries": response.queries,
        "table": fetch_result_table(database, response.final_query),
        "elapsed_time": response.elapsed_time
    }


def main():

    try:
        service, database = load_resources()
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        st.error(f"The assistant could not start: {e}")
        st.stop()

    st.session_state.setdefault("messages", [])

    messages = st.session_state.messages
    busy = bool(messages) and messages[-1]["role"] == "user"

    render_sidebar(database, busy)

    st.title("🗄️ SQL AI Assistant")
    st.caption("Ask questions about the sales database in plain language.")

    for message in messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                render_assistant_message(message)

    question = st.chat_input("Ask a question about your data...", disabled=busy)
    question = question or st.session_state.pop("pending_question", None)

    if question and not busy:
        messages.append({"role": "user", "content": question})
        st.rerun()

    if not busy:
        return

    with st.chat_message("assistant"):
        with st.spinner("Querying the database..."):
            message = answer_question(service, database, messages[-1]["content"])

    messages.append(message)
    st.rerun()

main()
