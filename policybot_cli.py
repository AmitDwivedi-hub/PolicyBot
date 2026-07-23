"""
CLI tool for interacting with PolicyBot.

Just start typing questions. The bot remembers prior turns automatically.
Type 'exit' or '0' at any point to end the session and print the full
conversation as JSON (RAGAS / DeepEval ready). The conversation is also
saved to conversation.md in the same directory.

Usage:
    python policybot_cli.py
    python policybot_cli.py --url http://localhost:8001
    python policybot_cli.py --timeout 90
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

POLICYBOT_URL = "http://localhost:8001"
DEFAULT_TIMEOUT = 60
EXIT_TOKENS = {"exit", "0"}
MARKDOWN_PATH = Path(__file__).resolve().parent / "conversation.md"

SEPARATOR = "─" * 60


def _ask(base_url: str, question: str, session_id: Optional[str], timeout: int) -> dict:
    payload: dict = {"question": question}
    if session_id:
        payload["session_id"] = session_id
    r = requests.post(f"{base_url}/query", json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _check_health(base_url: str) -> None:
    try:
        r = requests.get(f"{base_url}/health", timeout=10)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"\n[ERROR] Cannot reach backend at {base_url}")
        print("        Make sure the server is running: python run.py")
        sys.exit(1)
    except Exception as exc:
        print(f"\n[WARN] Health check failed: {exc}")


def _extract_contexts(turn_data: dict) -> list[str]:
    return [chunk["text"] for chunk in turn_data.get("context", [])]


def _print_answer(answer: str) -> None:
    print(f"\nBot: {answer}")



def _write_markdown(turns: list[dict], session_id: Optional[str], timestamp: str) -> None:
    msg_lines = []
    if len(turns) == 1:
        ai_content = turns[0]["answer"].replace('"', '\\"')
        msg_lines.append(f'"{ai_content}"')
    else:
        for t in turns:
            human_content = t["question"].replace('"', '\\"')
            ai_content = t["answer"].replace('"', '\\"')
            msg_lines.append(f'HumanMessage(')
            msg_lines.append(f'    content="{human_content}"')
            msg_lines.append(f'),')
            msg_lines.append(f'AIMessage(')
            msg_lines.append(f'    content="{ai_content}"')
            msg_lines.append(f'),')

    last_contexts = turns[-1]["retrieved_contexts"] if turns else []
    items = ', '.join(f'"{ctx.replace(chr(10), " ").strip()}"' for ctx in last_contexts)
    context_sections = [f"[{items}]", ""]

    last_ground_truth = turns[-1]["ground_truth"] if turns else ""

    is_multi_turn = len(turns) > 1

    deepeval_lines = []
    if is_multi_turn:
        deepeval_lines.append("convo = ConversationalTestCase(")
        deepeval_lines.append("    turns=[")
        for t in turns:
            inp = t["question"].replace('"', '\\"')
            out = t["answer"].replace('"', '\\"')
            ctx_items = ', '.join(
                f'"{c.replace(chr(10), " ").strip()}"' for c in t["retrieved_contexts"]
            )
            deepeval_lines.append(f'        Turn(role="user", content="{inp}"),')
            deepeval_lines.append(f'        Turn(role="assistant",')
            deepeval_lines.append(f'             content="{out}",')
            deepeval_lines.append(f'             retrieval_context=[{ctx_items}]),')
        deepeval_lines.append("    ],")
        deepeval_lines.append(")")
    else:
        for t in turns:
            inp = t["question"].replace('"', '\\"')
            out = t["answer"].replace('"', '\\"')
            gt = t["ground_truth"].replace('"', '\\"')
            ctx_items = ', '.join(
                f'"{c.replace(chr(10), " ").strip()}"' for c in t["retrieved_contexts"]
            )
            deepeval_lines.append(f'LLMTestCase(')
            deepeval_lines.append(f'    input="{inp}",')
            deepeval_lines.append(f'    actual_output="{out}",')
            deepeval_lines.append(f'    retrieval_context=[{ctx_items}],')
            deepeval_lines.append(f'    expected_output="{gt}",')
            deepeval_lines.append(f'),')

    lines = [
        "# PolicyBot Conversation",
        "",
        f"**Session ID:** `{session_id}`  ",
        f"**Date:** {timestamp}  ",
        f"**Turns:** {len(turns)}  ",
        "",
        "---",
        "",
        "## RAGAS — Conversation (HumanMessage / AIMessage)" if len(turns) > 1 else "## RAGAS — Response",
        "",
        *msg_lines,
        "",
        "---",
        "",
        "## Retrieved Contexts (last turn)",
        "",
        *context_sections,
        "---",
        "",
        "## Ground Truth (last turn)",
        "",
        last_ground_truth,
        "",
        "---",
        "",
        "## DeepEval — ConversationalTestCase (multi-turn)" if is_multi_turn else "## DeepEval — LLMTestCase per Turn",
        "",
        *deepeval_lines,
        "",
        "---",
        "",
        "*Exported for RAGAS / DeepEval evaluation*",
    ]

    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nConversation saved to: {MARKDOWN_PATH}")


def run(base_url: str, timeout: int) -> None:
    print(f"\n{SEPARATOR}")
    print("  Ask your questions below. Prior turns are remembered.")
    print("  Type 'exit' or '0' at any time to end the conversation.")
    print(f"{SEPARATOR}\n")

    session_id: Optional[str] = None
    turns: list[dict] = []
    timestamp = datetime.now(timezone.utc).isoformat()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not question:
            continue
        if question.lower() in EXIT_TOKENS:
            break

        print("\nThinking…")
        try:
            data = _ask(base_url, question, session_id=session_id, timeout=timeout)
        except requests.HTTPError as exc:
            print(f"[ERROR] Server returned {exc.response.status_code}: {exc.response.text}")
            continue
        except Exception as exc:
            print(f"[ERROR] {exc}")
            continue

        session_id = data.get("session_id", session_id)

        _print_answer(data["answer"])
        print("\n(Type 'exit' or '0' to end the conversation.)\n")

        turns.append({
            "question": question,
            "answer": data["answer"],
            "ground_truth": data.get("ground_truth", ""),
            "source_doc": data.get("source_doc", ""),
            "page": data.get("page", 0),
            "is_flawed": data.get("is_flawed", False),
            "retrieved_contexts": _extract_contexts(data),
        })

    if not turns:
        print("No turns recorded. Exiting.")
        return

    _write_markdown(turns, session_id, timestamp)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PolicyBot CLI – conversational Q&A with JSON export",
    )
    parser.add_argument(
        "--url",
        default=POLICYBOT_URL,
        help=f"Backend base URL (default: {POLICYBOT_URL})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    args = parser.parse_args()

    print(f"\n{'═' * 60}")
    print("  PolicyBot CLI")
    print(f"{'═' * 60}")
    print(f"  Backend : {args.url}")
    _check_health(args.url)
    print(f"{'═' * 60}")

    run(args.url, args.timeout)


if __name__ == "__main__":
    main()
