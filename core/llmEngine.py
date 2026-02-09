from ctransformers import AutoModelForCausalLM
import threading

class ScriptEaseLLM:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.llm = None

    def load(self):
        if self.llm is None:
            print("[ScriptEase] Loading local LLM...")
            self.llm = AutoModelForCausalLM.from_pretrained(
                "models",
                model_file="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
                model_type="mistral",
                context_length=4096,
                threads=8
            )
            print("[ScriptEase] LLM loaded.")

    def generate(self, prompt, max_tokens=200):
        self.load()
        return self.llm(prompt, max_new_tokens=max_tokens)

def get_llm():
    if ScriptEaseLLM._instance is None:
        with ScriptEaseLLM._lock:
            if ScriptEaseLLM._instance is None:
                ScriptEaseLLM._instance = ScriptEaseLLM()
    return ScriptEaseLLM._instance
