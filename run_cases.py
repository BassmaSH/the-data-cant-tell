"""Run the cases (C01 to C09) on a small and a large Mistral model.

Built Oct 15 from Bassma's first Mistral call; the call itself is hers, the loop and the saving around it are
Claude's (Claude Code). Keys are read from MISTRAL_API_KEY and ANTHROPIC_API_KEY.

    python run_cases.py models            # list the models the key can use, to pick the large one
    python run_cases.py <large-model>     # every case x 2 models, saved under results/<date>/
    python run_cases.py <large-model> C06 --tag v2   # one case only; the tag keeps earlier results
    python run_cases.py <large-model> --no-system    # same calls without the system message (saved as -nosys)
    python run_cases.py <large-model> --premise      # the system message plus her premise sentence (saved as -premise)
    python run_cases.py <large-model> --premise-only # her premise sentence alone (saved as -premiseonly)
    python run_cases.py <large-model> --steps        # her four steps, in place of the system message (saved as -steps)
    python run_cases.py mistral-large-4 C04 --models mistral-large-4,magistral-small-latest   # any list of models
    python run_cases.py mistral-large-4-0 --models mistral-large-4-0 --reasoning high   # reasoning_effort (saved as -rhigh)
    python run_cases.py x C04 --models claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5   # Anthropic models
    python run_cases.py <large-model> C05 --data categories   # reads C05-data-categories.txt (saved as -categories)
"""
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

from mistralai.client import Mistral

HERE = Path(__file__).parent
SMALL = "mistral-small-2603"
SYSTEM = ("Don't say anything that isn't clearly supported by the data. "
          "If you are unable to answer something with the data, say so.")
# Her sentence, Oct 20, after row 2: the question's own observation can be wrong.
PREMISE = ("If the user is making an observation, make sure that observation is true first "
           "and correct it if not.")

# The questions as written in cases/C0*.md (Oct 13 and Oct 15); C01, C02, C03, C05 proposed by Claude and
# validated by her on Oct 20.
QUESTIONS = {
    "C01": "Why are North rentals down on last year since May?",
    "C02": "Why did West revenue fall from April 2026?",
    "C03": "Why did East contract revenue fall from late January 2026?",
    "C04": "Why is there a drop in Tidesend on the week of 2026-06-15?",
    "C05": "Why is the South's average daily rate lower this summer than last summer? We didn't cut prices.",
    "C06": "Why did North revenue drop on the week of 2026-07-13?",
    "C07": "What happened between 2025-11-10 and 2025-11-24 at D11 Lowen Quay?",
    "C08": "Why did rentals drop at Hollin Cross in October 2025?",
    "C09": "Why did walk-in rentals drop at the counter, East region, July 2026?",
}

client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY", ""))
claude = None


def ask_claude(model, system, user):
    """The Anthropic call, written by Claude at her request (Oct 20). Each model at its own defaults: Claude
    models take no temperature setting and think before answering (adaptive thinking, the model's default
    effort). No server-side fallback, so every answer comes from the model named; a refusal shows in stop."""
    global claude
    if claude is None:
        from anthropic import Anthropic
        claude = Anthropic()  # reads ANTHROPIC_API_KEY
    kwargs = {"model": model, "max_tokens": 16000, "messages": [{"role": "user", "content": user}]}
    if system:
        kwargs["system"] = system
    res = claude.messages.create(**kwargs)
    answer = "".join(b.text for b in res.content if b.type == "text")  # thinking blocks dropped
    return answer, res.usage.input_tokens, res.usage.output_tokens, res.stop_reason


if len(sys.argv) < 2:
    sys.exit(__doc__)

if sys.argv[1] == "models":
    for m in client.models.list().data:
        print(m.id)
    sys.exit()

large = sys.argv[1]
args = sys.argv[2:]
tag = ""
system = SYSTEM
if "--no-system" in args:
    system = None
    tag = "-nosys"
    args.remove("--no-system")
if "--premise" in args:
    system = SYSTEM + " " + PREMISE
    tag = "-premise"
    args.remove("--premise")
if "--premise-only" in args:
    system = PREMISE
    tag = "-premiseonly"
    args.remove("--premise-only")
# Her steps, Oct 20, after run 4; they replace the run 1 message, whose point is in step 4.
STEPS = ("Answer in four steps:\n"
         "1. Read the data the question is about.\n"
         "2. Check that the user's observation is true; correct it only if the data says otherwise.\n"
         "3. Check whether the data is enough to answer.\n"
         "4. If it is, answer with what the data shows. If not, say what's missing. Call any guess a guess.")
if "--steps" in args:
    system = STEPS
    tag = "-steps"
    args.remove("--steps")
models = [SMALL, large]
if "--models" in args:
    models = args[args.index("--models") + 1].split(",")
    del args[args.index("--models"):args.index("--models") + 2]
extra = {}
if "--reasoning" in args:  # Mistral's reasoning_effort ("none" or "high"), Oct 20; the docs give no default
    extra["reasoning_effort"] = args[args.index("--reasoning") + 1]
    tag += "-r" + extra["reasoning_effort"]
    del args[args.index("--reasoning"):args.index("--reasoning") + 2]
variant = ""
if "--data" in args:
    variant = "-" + args[args.index("--data") + 1]
    tag += variant
    del args[args.index("--data"):args.index("--data") + 2]
if "--tag" in args:
    tag += "-" + args[args.index("--tag") + 1]
    args = args[:args.index("--tag")]
cases = args or list(QUESTIONS)
out = HERE / "results" / date.today().isoformat()
out.mkdir(parents=True, exist_ok=True)

for case in cases:
    question = QUESTIONS[case]
    data = (HERE / "cases" / "data" / f"{case}-data{variant}.txt").read_text()
    for model in models:
        user = f"data:{data}, question:{question}"
        start = time.perf_counter()
        if model.startswith("claude-"):
            answer, tokens_in, tokens_out, stop = ask_claude(model, system, user)
        else:
            messages = [{"role": "user", "content": user}]
            if system:
                messages.insert(0, {"role": "system", "content": system})
            res = client.chat.complete(model=model, temperature=0, top_p=1, messages=messages, **extra)  # top_p=1: Large 4 requires it with temperature 0 (no effect under greedy sampling)
            answer = res.choices[0].message.content
            if not isinstance(answer, str):  # reasoning answers come in chunks: keep the text, drop the thinking
                answer = "".join(getattr(c, "text", "") for c in answer if getattr(c, "type", "") == "text")
            tokens_in, tokens_out, stop = res.usage.prompt_tokens, res.usage.completion_tokens, res.choices[0].finish_reason
        seconds = time.perf_counter() - start
        record = {"case": case, "model": model, "question": question, "system": system,
                  "prompt_tokens": tokens_in, "completion_tokens": tokens_out, "stop": str(stop),
                  "seconds": round(seconds, 2), "answer": answer}
        (out / f"{case}-{model}{tag}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False))
        print(f"\n=== {case} · {model} · {tokens_in}+{tokens_out} tokens · {seconds:.1f} s\n{answer}")
