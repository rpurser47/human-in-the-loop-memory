# Human in the Loop Memory Exercise

I'm learning to use [LangGraph](https://www.langchain.com/langgraph) by taking a [Udemy class](https://www.udemy.com/course/langgraph)

A trivial implementation demonstrating how a LangChain agent can be interrupted to get human input and how the system handles that.   It uses a memory system to retain the state of the agent during the human interaction and restarts the interaction afterwards with full context.

# Human Interaction, Persistence, and Interrupts
LangGraph enables human intervention at any stage of an agent or workflow to review, edit, and approve outputs, correct errors, and guide conversations. LangChain provides tools called [*checkpointers*](https://langchain-ai.github.io/langgraph/concepts/persistence/) to save the state of the conversation to allow for it to be resumed seamlessly.  We're using a basic one called `MemorySaver`. Finally, LangGraph enables the interruption of workflows to allow for human input or review through the interrupt function to pause graph execution at specific points.


## Example
```
Hello Human in the Loop Memory                                                            
```

``` json
{'input': 'hello_world'}
```

```
--- Step 1 ---
```
**State before update**

``` python

StateSnapshot(
   values={'input': 'hello_world'},
   next=('human_feedback',),
   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07b536-c84c-67b1-8001-94e78849fbc0'}},
   metadata={'source': 'loop', 'writes': {'step_1': None}, 'step': 1, 'parents': {}, 'thread_id': '1'},
   created_at='2025-08-17T10:17:48.162859+00:00',
   parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07b536-c84c-67b0-8000-24014a6738b1'}},
   tasks=(
   │   PregelTask(id='378f6834-25e1-cd1d-8036-a95321c75c7a', name='human_feedback', path=('__pregel_pull', 'human_feedback'), error=None, interrupts=(), state=None, result=None),
   ),
   interrupts=()
)
```

``` text 
Tell me how you want to update the state: koko
```
**State after update**
``` python
StateSnapshot(
   values={'input': 'hello_world', 'user_feedback': 'koko'},
   next=('step_3',),
   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07b537-1bf4-6dc0-8002-cabbc78e0d57'}},
   metadata={'source': 'update', 'writes': {'human_feedback': {'user_feedback': 'koko'}}, 'step': 2, 'parents': {}, 'thread_id': '1'},
   created_at='2025-08-17T10:17:56.935008+00:00',
   parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07b536-c84c-67b1-8001-94e78849fbc0'}},
   tasks=(PregelTask(id='31af6f7c-4eb6-c070-e938-8775df2d2e89', name='step_3', path=('__pregel_pull', 'step_3'), error=None, interrupts=(), state=None, result=None),),
   interrupts=()
)
```

``` json
{'input': 'hello_world', 'user_feedback': 'koko'}
```

## LangGraph Graph
``` mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        step_1(step_1)
        human_feedback(human_feedback<hr/><small><em>__interrupt = before</em></small>)
        step_3(step_3)
        __end__([<p>__end__</p>]):::last
        __start__ --> step_1;
        human_feedback --> step_3;
        step_1 --> human_feedback;
        step_3 --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
```

## Notes
Note that you'll need an `.env` file like this:

``` text
LANGCHAIN_API_KEY=<MY_LANGSMITH_API_KEY>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Human in the Loop Memory
```
