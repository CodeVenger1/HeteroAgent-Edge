import mlx.core as mx
from mlx_lm import load, generate

def bytes_to_mb(b):
    return round(b/(1024*1024),2)

def print_memory_stats(stage):
    active = bytes_to_mb(mx.get_active_memory())
    peak = bytes_to_mb(mx.get_peak_memory())
    print(f"[{stage}] Active Memory: {active} MB | Peak Memory: {peak} MB")

mx.reset_peak_memory()
print_memory_stats("Initial State")

model_name = "mlx-community/Llama-3.2-1B-Instruct-4bit"
print(f"\nLoading {model_name}...")
model, tokenizer = load(model_name)
print_memory_stats("Post-Model-Load")

prompt = "Explain why unified memory is useful for multi-agent LLM systems in two sentences."
messages = [{"role": "user", "content": prompt}]
formatted_prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

print("\n--- Generating Response ---")
mx.reset_peak_memory()
response = generate(model, tokenizer, prompt=formatted_prompt, max_tokens=80, verbose=False)
mx.synchronize()

print(response.strip())

print_memory_stats("Post-Generation Delta")