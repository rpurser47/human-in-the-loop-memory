from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.pretty import pprint

load_dotenv()

class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state: State) -> None:
    print("--- Step 1 ---")

def human_feedback(state: State) -> None:
    print("--- Human Feedback ---")

def step_3(state: State) -> None:
    print("--- Step 3 ---")

STEP_1 = "step_1"
STEP_HUMAN_FEEDBACK = "human_feedback"
STEP_3 = "step_3"

builder = StateGraph(State)
builder.add_node(STEP_1, step_1)
builder.add_node(STEP_HUMAN_FEEDBACK, human_feedback)
builder.add_node(STEP_3, step_3)

builder.add_edge(START, end_key=STEP_1)
builder.add_edge(start_key=STEP_1, end_key=STEP_HUMAN_FEEDBACK)
builder.add_edge(start_key=STEP_HUMAN_FEEDBACK, end_key=STEP_3)
builder.add_edge(start_key=STEP_3, end_key=END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory, interrupt_before=[STEP_HUMAN_FEEDBACK])

if __name__ == "__main__":
    console = Console()
    console.print(Markdown("# Hello Human in the Loop Memory"))
    console.print(graph.get_graph().draw_ascii())
    thread = {"configurable": {"thread_id": "1"}}
    initial_input = {"input": "hello_world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        pprint(event)

    console.print(Markdown("## State *before* update"))
    pprint(graph.get_state(thread))
    console.print()

    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(thread, {
        "user_feedback": user_input},
        as_node="human_feedback"
    )

    console.print(Markdown("## State *after* update"))
    pprint(graph.get_state(thread))
    console.print()

    for event in graph.stream(None, thread, stream_mode="values"):
        pprint(event)