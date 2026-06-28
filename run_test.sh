#!/usr/bin/env bash
# probe_bedrock_thinking.sh
#
# Runs the full matrix of Bedrock Converse-Stream thinking probes against
# Claude Opus 4.6 / 4.7 / 4.8 in ap-southeast-2 (apac inference profile).
#
# Each probe exercises a single (model, mode, effort_or_budget) tuple and prints
# a SUMMARY block showing reasoning text / signature / redacted / answer text
# counts. Driven by main.py (the Python boto3 probe).
#
# Empirical results from the original run that informed Kovar's profile config:
#
#   | Model | Mode      | Knob   | Reasoning text | Reasoning sig | Notes                          |
#   |-------|-----------|--------|----------------|---------------|--------------------------------|
#   | 4.6   | adaptive  | high   | 91 chars       | 1             | visible thinking               |
#   | 4.6   | enabled   | 8000   | 91 chars       | 1             | visible thinking (budget mode) |
#   | 4.7   | adaptive  | xhigh  | 0              | 1             | signature only (encrypted)     |
#   | 4.7   | adaptive  | high   | 0              | 0             | no thinking block emitted      |
#   | 4.7   | enabled   | 8000   | —              | —             | HTTP 400 — not supported       |
#   | 4.8   | adaptive  | xhigh  | 0              | 1             | signature only (encrypted)     |
#   | 4.8   | adaptive  | high   | 0              | 1             | signature only (encrypted)     |
#   | 4.8   | enabled   | 8000   | —              | —             | HTTP 400 — not supported       |
#
# Conclusion: Opus 4.7/4.8 over Bedrock cannot return visible reasoning text in
# any mode/effort combination. Opus 4.6 returns it for both adaptive and budget
# modes.
#
# Requirements:
#   - main.py in the working directory (the boto3 Converse-Stream probe)
#   - uv installed (https://docs.astral.sh/uv/)
#   - AWS credentials with bedrock-runtime access (e.g. via AWS_PROFILE)
#   - Region: ap-southeast-2
#
# Usage:
#   ./probe_bedrock_thinking.sh                # run the full matrix
#   ./probe_bedrock_thinking.sh 4.7            # only Opus 4.7 probes
#   ./probe_bedrock_thinking.sh 4.6 adaptive   # only 4.6 adaptive probes

set -u

MODEL_46="us.anthropic.claude-opus-4-6-v1"   # 4.6 accepts -v1 (older model)
MODEL_47="us.anthropic.claude-opus-4-7"
MODEL_48="us.anthropic.claude-opus-4-8"

MODEL_FILTER="${1:-}"
MODE_FILTER="${2:-}"

run_probe() {
    local model="$1" mode="$2" knob="$3" label="$4"
    if [[ -n "$MODEL_FILTER" && "$model" != *"$MODEL_FILTER"* ]]; then return; fi
    if [[ -n "$MODE_FILTER"  && "$mode"  != "$MODE_FILTER" ]]; then return; fi

    echo
    echo "##############################################################"
    echo "# $label"
    echo "##############################################################"
    uv run main.py "$model" "$mode" "$knob"
}

run_probe "$MODEL_46" "adaptive" "high"  "Opus 4.6 — adaptive / high   (expect: visible thinking)"
run_probe "$MODEL_46" "enabled"  "8000"  "Opus 4.6 — enabled / 8000    (expect: visible thinking via budget)"
run_probe "$MODEL_47" "adaptive" "xhigh" "Opus 4.7 — adaptive / xhigh  (expect: signature only)"
run_probe "$MODEL_47" "adaptive" "high"  "Opus 4.7 — adaptive / high   (expect: no thinking block)"
run_probe "$MODEL_47" "enabled"  "8000"  "Opus 4.7 — enabled / 8000    (expect: HTTP 400)"
run_probe "$MODEL_48" "adaptive" "xhigh" "Opus 4.8 — adaptive / xhigh  (expect: signature only)"
run_probe "$MODEL_48" "adaptive" "high"  "Opus 4.8 — adaptive / high   (expect: signature only)"
run_probe "$MODEL_48" "enabled"  "8000"  "Opus 4.8 — enabled / 8000    (expect: HTTP 400)"

echo
echo "##############################################################"
echo "# Done. Compare SUMMARY blocks against the expectations above."
echo "##############################################################"

