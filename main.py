#!/usr/bin/env python3
"""
Direct Bedrock Converse-Stream probe with thinking enabled.

Usage:
    python bedrock_thinking_probe.py <model-id> <mode> [effort_or_budget]

Examples:
    python bedrock_thinking_probe.py au.anthropic.claude-opus-4-7-v1:0 adaptive xhigh
    python bedrock_thinking_probe.py au.anthropic.claude-opus-4-7-v1:0 adaptive high
    python bedrock_thinking_probe.py au.anthropic.claude-opus-4-6-v1:0 enabled 8000
    python bedrock_thinking_probe.py au.anthropic.claude-opus-4-6-v1:0 adaptive high

Per Anthropic/AWS docs:
    - Opus 4.6, Sonnet 3.7: supports both `adaptive` and `enabled` (budget)
    - Opus 4.7, 4.8:        ONLY `adaptive` — `enabled` returns HTTP 400
"""
import sys, json, boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
PROMPT = "What is 17 * 23? Think step by step about it before answering."

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    model_id = sys.argv[1]
    mode = sys.argv[2]           # "adaptive" or "enabled"
    knob = sys.argv[3] if len(sys.argv) > 3 else None

    # Build additionalModelRequestFields based on mode
    if mode == "adaptive":
        effort = knob or "high"
        extra = {
            "thinking": {"type": "adaptive", "display" : "summarized"},
            "output_config": {"effort": effort},
        }
        print(f"[CONFIG] model={model_id} mode=adaptive effort={effort}")
    elif mode == "enabled":
        budget = int(knob) if knob else 8000
        extra = {
            "thinking": {"type": "enabled", "budget_tokens": budget},
        }
        print(f"[CONFIG] model={model_id} mode=enabled budget_tokens={budget}")
    else:
        print(f"unknown mode: {mode}")
        sys.exit(1)

    print(f"[REQUEST] additionalModelRequestFields={json.dumps(extra)}")
    print(f"[PROMPT]  {PROMPT}\n")

    client = boto3.client("bedrock-runtime", region_name=REGION)
    try:
        resp = client.converse_stream(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": PROMPT}]}],
            additionalModelRequestFields=extra,
        )
    except ClientError as e:
        print(f"[ERROR] {e.response['Error']['Code']}: {e.response['Error']['Message']}")
        sys.exit(2)

    # Counters to summarise at the end
    reasoning_text_chunks = 0
    reasoning_text_chars = 0
    reasoning_signatures = 0
    reasoning_redacted = 0
    text_chunks = 0
    text_chars = 0

    for event in resp["stream"]:
        if "messageStart" in event:
            print(f"--- messageStart role={event['messageStart']['role']} ---")
        elif "contentBlockStart" in event:
            start = event["contentBlockStart"].get("start", {})
            idx = event["contentBlockStart"].get("contentBlockIndex")
            print(f"\n--- contentBlockStart idx={idx} start={start} ---")
        elif "contentBlockDelta" in event:
            delta = event["contentBlockDelta"]["delta"]
            if "reasoningContent" in delta:
                rc = delta["reasoningContent"]
                if "text" in rc:
                    reasoning_text_chunks += 1
                    reasoning_text_chars += len(rc["text"])
                    print(f"[REASON TEXT] {rc['text']}", end="", flush=True)
                elif "signature" in rc:
                    reasoning_signatures += 1
                    print(f"\n[REASON SIG] {len(rc['signature'])} chars")
                elif "redactedContent" in rc:
                    reasoning_redacted += 1
                    print(f"\n[REASON REDACTED] {len(rc['redactedContent'])} bytes")
                else:
                    print(f"\n[REASON UNKNOWN] keys={list(rc.keys())}")
            elif "text" in delta:
                text_chunks += 1
                text_chars += len(delta["text"])
                print(f"{delta['text']}", end="", flush=True)
            else:
                print(f"\n[OTHER DELTA] {delta}")
        elif "contentBlockStop" in event:
            idx = event["contentBlockStop"].get("contentBlockIndex")
            print(f"\n--- contentBlockStop idx={idx} ---")
        elif "messageStop" in event:
            print(f"\n--- messageStop reason={event['messageStop']['stopReason']} ---")
        elif "metadata" in event:
            usage = event["metadata"].get("usage", {})
            print(f"\n--- metadata usage={usage} ---")

    print("\n" + "=" * 50)
    print(f"SUMMARY for {model_id} ({mode}):")
    print(f"  reasoning text: {reasoning_text_chunks} chunks, {reasoning_text_chars} chars")
    print(f"  reasoning sig:  {reasoning_signatures}")
    print(f"  reasoning redacted: {reasoning_redacted}")
    print(f"  answer text:    {text_chunks} chunks, {text_chars} chars")
    print("=" * 50)

if __name__ == "__main__":
    main()

