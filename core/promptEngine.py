class PromptEngine:
    def __init__(self):
        self.prompts = {
            "rewrite": self._rewrite_prompt,
            "summarize": self._summarize_prompt,
            "improve": self._improve_prompt
        }

    def build(self, task: str, text: str) -> str:
        if task not in self.prompts:
            raise ValueError(f"Unknown task: {task}")
        return self.prompts[task](text)

    # -------- PROMPT TEMPLATES -------- #

    def _rewrite_prompt(self, text: str) -> str:
        return f"""
You are a rewriting assistant.

TASK:
Rewrite the given text ONLY.
Do NOT continue the message.
Do NOT add new sentences.
Do NOT assume missing context.
If the input is short, keep the output equally short.

Fix grammar, spelling, and clarity only.
Preserve the original tone and intent.

Return ONLY the rewritten text.
Nothing else.

INPUT:
{text}

OUTPUT:
"""

    def _summarize_prompt(self, text: str) -> str:
        return f"""
You are a summarization assistant.

TASK:
Summarize ONLY the given text.
Do NOT add new information.
Do NOT include examples or explanations.
Do NOT continue beyond the content provided.

If the input is short, produce a very short summary.
Limit the summary to 1–2 sentences maximum.

Return ONLY the summary.
Nothing else.

INPUT:
{text}

OUTPUT:
"""

    def _improve_prompt(self, text: str) -> str:
        return f"""
You are a writing improvement assistant.

TASK:
Improve the given text ONLY.
Do NOT add new ideas.
Do NOT expand the message.
Do NOT continue beyond the provided content.

Improve clarity, grammar, and flow
while preserving the original meaning and tone.

Return ONLY the improved text.
Nothing else.

INPUT:
{text}

OUTPUT:
"""
