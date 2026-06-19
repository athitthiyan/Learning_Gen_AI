"""
Streamlit app: Researcher -> Supervisor -> Writer (LangGraph)
=============================================================

Deploys the multi-agent graph with a human-in-the-loop breakpoint:
the supervisor routes work, the researcher searches with Tavily, the
writer drafts a report with Groq -- and the app PAUSES after research
so you can review before the writer runs.

Run locally:
    pip install -r requirements_streamlit.txt
    streamlit run app.py

Deploy on Streamlit Community Cloud: push this file + requirements to a
public GitHub repo, create an app pointing at app.py, and add
GROQ_API_KEY and TAVILY_API_KEY under the app's "Secrets".
"""

import operator
import os
import uuid
from typing import Annotated, List, Literal, TypedDict

import streamlit as st
from pydantic import BaseModel, Field

st.set_page_config(page_title="Researcher → Writer", page_icon="🧠", layout="centered")
st.title("🧠 Researcher → Supervisor → Writer")
st.caption("LangGraph multi-agent demo (Groq + Tavily) with a human-in-the-loop pause.")


# ----------------------------------------------------------------------------- #
# API keys: from Streamlit Secrets when deployed, or the sidebar when local.
# ----------------------------------------------------------------------------- #
def _secret(name: str) -> str:
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


with st.sidebar:
    st.header("API keys")
    groq_key = st.text_input("GROQ_API_KEY", type="password", value=_secret("GROQ_API_KEY"))
    tavily_key = st.text_input("TAVILY_API_KEY", type="password", value=_secret("TAVILY_API_KEY"))
    st.markdown("[Get a Groq key](https://console.groq.com) · [Get a Tavily key](https://tavily.com)")

if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key
if tavily_key:
    os.environ["TAVILY_API_KEY"] = tavily_key

if not (os.environ.get("GROQ_API_KEY") and os.environ.get("TAVILY_API_KEY")):
    st.info("Enter your Groq and Tavily API keys in the sidebar to begin.")
    st.stop()


# ----------------------------------------------------------------------------- #
# Graph definition (built once per session so the checkpointer survives reruns)
# ----------------------------------------------------------------------------- #
class AgentState(TypedDict):
    task: str
    research_notes: Annotated[List[str], operator.add]
    draft: str
    next_node: str
    retry_count: int
    revision_feedback: str


class Router(BaseModel):
    """Decide which worker to call next."""
    next_worker: Literal["researcher", "writer", "FINISH"] = Field(description="The next node to act")
    instructions: str = Field(description="Specific instructions for the worker")
    is_critical: bool = Field(description="If True, pause for human review")


def build_graph():
    from langchain_groq import ChatGroq
    from langchain_tavily import TavilySearch
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    search_tool = TavilySearch(max_results=2)

    def researcher(state: AgentState):
        results = search_tool.invoke({"query": state["task"]})
        return {"research_notes": [str(results)], "retry_count": 0}

    def writer(state: AgentState):
        context = "\n".join(state["research_notes"])
        res = llm.invoke(
            f"Write a clear, well-structured report on '{state['task']}' using these notes:\n{context}"
        )
        return {"draft": res.content}

    def supervisor(state: AgentState):
        structured_llm = llm.with_structured_output(Router)
        n_notes = len(state.get("research_notes", []))
        has_draft = bool(state.get("draft"))
        prompt = f"""
        You are a supervisor coordinating a researcher and a writer.
        Rules:
        - No research notes yet -> next_worker = "researcher".
        - Notes exist but no draft yet -> next_worker = "writer".
        - A draft already exists -> next_worker = "FINISH".

        Task: {state['task']}
        Research notes collected: {n_notes}
        Draft already written: {"yes" if has_draft else "no"}
        """
        decision = structured_llm.invoke(prompt)
        next_worker = decision.next_worker
        if has_draft:                       # guard: writer can never loop forever
            next_worker = "FINISH"
        return {"next_node": next_worker, "revision_feedback": decision.instructions}

    builder = StateGraph(AgentState)
    builder.add_node("supervisor", supervisor)
    builder.add_node("researcher", researcher)
    builder.add_node("writer", writer)
    builder.set_entry_point("supervisor")
    builder.add_conditional_edges(
        "supervisor",
        lambda x: x["next_node"],
        {"researcher": "researcher", "writer": "writer", "FINISH": END},
    )
    builder.add_edge("researcher", "supervisor")
    builder.add_edge("writer", "supervisor")
    return builder.compile(checkpointer=MemorySaver(), interrupt_before=["writer"])


if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.phase = "idle"   # idle -> paused -> done


def _config():
    return {"configurable": {"thread_id": st.session_state.thread_id}}


# ----------------------------------------------------------------------------- #
# Optional: show the architecture diagram
# ----------------------------------------------------------------------------- #
with st.expander("Show graph architecture"):
    try:
        st.image(st.session_state.graph.get_graph().draw_mermaid_png())
    except Exception:
        st.code(st.session_state.graph.get_graph().draw_mermaid(), language="text")


# ----------------------------------------------------------------------------- #
# UI flow
# ----------------------------------------------------------------------------- #
if st.session_state.phase == "idle":
    task = st.text_input("Research task", value="Impact of LPU architecture on AI inference speeds")
    if st.button("🚀 Start research", type="primary"):
        with st.spinner("Supervisor routing → researcher searching…"):
            g, cfg = st.session_state.graph, _config()
            init = {"task": task, "research_notes": [], "retry_count": 0, "draft": ""}
            for _ in g.stream(init, cfg, stream_mode="values"):
                pass
        st.session_state.phase = "paused"
        st.rerun()

elif st.session_state.phase == "paused":
    state = st.session_state.graph.get_state(_config()).values
    st.subheader("⏸️ Paused for review")
    st.write(f"**Supervisor feedback:** {state.get('revision_feedback', '')}")
    st.subheader("Research notes")
    for i, note in enumerate(state.get("research_notes", []), 1):
        with st.expander(f"Note {i}"):
            st.write(note)
    col1, col2 = st.columns(2)
    if col1.button("✍️ Approve & write report", type="primary"):
        with st.spinner("Writer composing…"):
            g, cfg = st.session_state.graph, _config()
            for _ in g.stream(None, cfg, stream_mode="values"):
                pass
        st.session_state.phase = "done"
        st.rerun()
    if col2.button("🔄 Start over"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.phase = "idle"
        st.rerun()

elif st.session_state.phase == "done":
    state = st.session_state.graph.get_state(_config()).values
    st.subheader("✅ Final report")
    st.markdown(state.get("draft", "_(no draft produced)_"))
    if st.button("🔄 New task"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.phase = "idle"
        st.rerun()