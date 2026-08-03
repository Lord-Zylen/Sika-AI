"""Sika AI orchestrator — core agent loop with tool dispatch and RAG."""

import json
from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL, MODEL_NAME, SKILLS_DIR
from system_prompt import SYSTEM_PROMPT
from tools import TOOLS_SCHEMA, TOOL_MAP
from rag.retriever import build_context
from skills.loader import get_skill_summary

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

MAX_TOOL_ROUNDS = 6


def build_system_message(user_query: str = "") -> str:
    """Build the full system message with prompt, skills, and RAG context."""
    parts = [SYSTEM_PROMPT]

    # Load skill summaries (compact — full content loaded via load_skill tool)
    skills_section = get_skill_summary(SKILLS_DIR)
    if skills_section:
        parts.append(skills_section)

    # Retrieve relevant RAG context for the query
    if user_query:
        rag_context = build_context(user_query)
        if rag_context:
            parts.append(f"## Relevant Knowledge Base Context\n\n{rag_context}")

    return "\n\n".join(parts)


def _execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute a tool by name with the given arguments and return the result string."""
    fn = TOOL_MAP.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    try:
        result = fn(**arguments)
        return result if isinstance(result, str) else json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Tool {tool_name} failed: {str(e)}"})


def chat(user_message: str, history: list[dict] | None = None) -> tuple[str, list[dict]]:
    """Run one turn of the agent conversation.

    Args:
        user_message: The user's new message.
        history: Previous conversation messages (excluding system).

    Returns:
        (assistant_reply, updated_history)
    """
    if history is None:
        history = []

    # Build messages
    system_msg = build_system_message(user_message)
    messages = [{"role": "system", "content": system_msg}] + history + [
        {"role": "user", "content": user_message}
    ]

    for _ in range(MAX_TOOL_ROUNDS):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
            )
        except Exception as e:
            # Groq returns 400 if the model hallucinates a tool name not in
            # our schema.  Retry once without tools so the model answers
            # from RAG / built-in knowledge instead of crashing.
            if "tool" in str(e).lower():
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                )
            else:
                raise

        choice = response.choices[0]
        msg = choice.message

        # If no tool calls, we're done
        if not msg.tool_calls:
            assistant_text = msg.content or ""
            updated_history = history + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_text},
            ]
            return assistant_text, updated_history

        # Process tool calls
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ],
        })

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            try:
                fn_args = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                fn_args = {}

            result = _execute_tool(fn_name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    # Fallback if we hit the tool round limit
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages + [{"role": "user", "content": "Please give your final answer now."}],
    )
    assistant_text = final_response.choices[0].message.content or ""
    updated_history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assistant_text},
    ]
    return assistant_text, updated_history
