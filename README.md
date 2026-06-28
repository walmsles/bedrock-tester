# Bedrock Tester

This repo is used to run various claude models to determine how well thinking modes are handled by Amazon Bedrock.  This repo was built as I have noticed that Anthropic CLaude OPus 4.7 and 4.8 are not returning any useful thinking on invoke.  This script tests various models 4.6 - 4.8 and makes a simple request and expects to have thinking returned by Amazon Bedrock interaction.

Current results as of June 28 2026 - Bedrock is not returning meaningful thining text as part of the COnverse API inference interaction.

### Test Results

The test results cabn be achieved by running the script.  The current script runs models against us-east-1 but have also tested in my home region of ap-southeast-2.
 
```bash
##############################################################
# Opus 4.6 — adaptive / high   (expect: visible thinking)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-6-v1 mode=adaptive effort=high
[REQUEST] additionalModelRequestFields={"thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---
[REASON TEXT] 17[REASON TEXT]  * 23[REASON TEXT] 

I[REASON TEXT]  can[REASON TEXT]  break[REASON TEXT]  this down:
17 * [REASON TEXT] 23 = 17 * ([REASON TEXT] 20 + 3)[REASON TEXT]  = 17 * 20 [REASON TEXT] + 17 * 3 [REASON TEXT] = 340 + 51 [REASON TEXT] = 391[REASON TEXT] 
[REASON SIG] 396 chars

--- contentBlockStop idx=0 ---
## Step-by-step solution

I'll break this multiplication into simpler parts:

**17 × 23 = 17 × (20 + 3)**

1. 17 × 20 = 340
2. 17 × 3 = 51

**Adding the results:**
340 + 51 = **391**
--- contentBlockStop idx=1 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 26, 'outputTokens': 158, 'totalTokens': 184} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-6-v1 (adaptive):
  reasoning text: 13 chunks, 91 chars
  reasoning sig:  1
  reasoning redacted: 0
  answer text:    22 chunks, 182 chars
==================================================

##############################################################
# Opus 4.6 — enabled / 8000    (expect: visible thinking via budget)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-6-v1 mode=enabled budget_tokens=8000
[REQUEST] additionalModelRequestFields={"thinking": {"type": "enabled", "budget_tokens": 8000}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---
[REASON TEXT] 17[REASON TEXT]  * 23[REASON TEXT] 

I[REASON TEXT]  can[REASON TEXT]  break[REASON TEXT]  this down:
17 * [REASON TEXT] 23 = 17 * ([REASON TEXT] 20 + 3)[REASON TEXT]  = 17 * 20 [REASON TEXT] + 17 * 3 [REASON TEXT] = 340 + 51 [REASON TEXT] = 391[REASON TEXT] 
[REASON SIG] 396 chars

--- contentBlockStop idx=0 ---
## Calculating 17 × 23

I'll break this multiplication into simpler parts:

**Step 1:** Break 23 into (20 + 3)

**Step 2:** Multiply each part by 17
- 17 × 20 = 340
- 17 × 3 = 51

**Step 3:** Add the results
- 340 + 51 = **391**

The answer is **391**.
--- contentBlockStop idx=1 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 55, 'outputTokens': 173, 'totalTokens': 228} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-6-v1 (enabled):
  reasoning text: 13 chunks, 91 chars
  reasoning sig:  1
  reasoning redacted: 0
  answer text:    24 chunks, 252 chars
==================================================

##############################################################
# Opus 4.7 — adaptive / xhigh  (expect: signature only)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-7 mode=adaptive effort=xhigh
[REQUEST] additionalModelRequestFields={"thinking": {"type": "adaptive"}, "output_config": {"effort": "xhigh"}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---

[REASON SIG] 328 chars

--- contentBlockStop idx=0 ---
# Calculating 17 × 23

I'll break this down step by step using the distributive property:

**Step 1:** Split 23 into 20 + 3
- 17 × 23 = 17 × (20 + 3)

**Step 2:** Multiply each part
- 17 × 20 = 340
- 17 × 3 = 51

**Step 3:** Add the results
- 340 + 51 = **391**

So, **17 × 23 = 391**
--- contentBlockStop idx=1 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 31, 'outputTokens': 199, 'totalTokens': 230} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-7 (adaptive):
  reasoning text: 0 chunks, 0 chars
  reasoning sig:  1
  reasoning redacted: 0
  answer text:    24 chunks, 284 chars
==================================================

##############################################################
# Opus 4.7 — adaptive / high   (expect: no thinking block)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-7 mode=adaptive effort=high
[REQUEST] additionalModelRequestFields={"thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---
To calculate 17 × 23, I'll break it down step by step:

**Step 1:** Break 23 into 20 + 3
- 17 × 23 = 17 × (20 + 3)

**Step 2:** Multiply each part
- 17 × 20 = 340
- 17 × 3 = 51

**Step 3:** Add the results
- 340 + 51 = 391

**Answer: 17 × 23 = 391**
--- contentBlockStop idx=0 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 31, 'outputTokens': 145, 'totalTokens': 176} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-7 (adaptive):
  reasoning text: 0 chunks, 0 chars
  reasoning sig:  0
  reasoning redacted: 0
  answer text:    23 chunks, 249 chars
==================================================

##############################################################
# Opus 4.7 — enabled / 8000    (expect: HTTP 400)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-7 mode=enabled budget_tokens=8000
[REQUEST] additionalModelRequestFields={"thinking": {"type": "enabled", "budget_tokens": 8000}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

[ERROR] ValidationException: The model returned the following errors: "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.

##############################################################
# Opus 4.8 — adaptive / xhigh  (expect: signature only)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-8 mode=adaptive effort=xhigh
[REQUEST] additionalModelRequestFields={"thinking": {"type": "adaptive"}, "output_config": {"effort": "xhigh"}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---

[REASON SIG] 340 chars

--- contentBlockStop idx=0 ---
# Calculating 17 × 23

Let me break this down step by step using the distributive property.

**Step 1:** Split 23 into 20 + 3
$$17 \times 23 = 17 \times (20 + 3)$$

**Step 2:** Multiply each part separately
- $17 \times 20 = 340$
- $17 \times 3 = 51$

**Step 3:** Add the results together
$$340 + 51 = 391$$

## Answer: **391**
--- contentBlockStop idx=1 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 26, 'outputTokens': 196, 'totalTokens': 222} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-8 (adaptive):
  reasoning text: 0 chunks, 0 chars
  reasoning sig:  1
  reasoning redacted: 0
  answer text:    23 chunks, 327 chars
==================================================

##############################################################
# Opus 4.8 — adaptive / high   (expect: signature only)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-8 mode=adaptive effort=high
[REQUEST] additionalModelRequestFields={"thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

--- messageStart role=assistant ---

[REASON SIG] 328 chars

--- contentBlockStop idx=0 ---
To solve 17 × 23, I'll break it down step by step:

**Method: Breaking apart the numbers**

I'll split 23 into 20 + 3:

**Step 1:** Multiply 17 × 20
- 17 × 20 = 340

**Step 2:** Multiply 17 × 3
- 17 × 3 = 51

**Step 3:** Add the results together
- 340 + 51 = 391

**Answer: 17 × 23 = 391**
--- contentBlockStop idx=1 ---

--- messageStop reason=end_turn ---

--- metadata usage={'inputTokens': 26, 'outputTokens': 191, 'totalTokens': 217} ---

==================================================
SUMMARY for us.anthropic.claude-opus-4-8 (adaptive):
  reasoning text: 0 chunks, 0 chars
  reasoning sig:  1
  reasoning redacted: 0
  answer text:    27 chunks, 289 chars
==================================================

##############################################################
# Opus 4.8 — enabled / 8000    (expect: HTTP 400)
##############################################################
[CONFIG] model=us.anthropic.claude-opus-4-8 mode=enabled budget_tokens=8000
[REQUEST] additionalModelRequestFields={"thinking": {"type": "enabled", "budget_tokens": 8000}}
[PROMPT]  What is 17 * 23? Think step by step about it before answering.

[ERROR] ValidationException: The model returned the following errors: "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.

##############################################################
# Done. Compare SUMMARY blocks against the expectations above.
##############################################################

```
