import sys
import os
import time
from typing import List, Tuple
import mlx.core as mx
from mlx_lm import load, generate

# Ensure project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hetero_edge.profiler import MetalMemoryTracker


class LLMEngine:
    """Encapsulates the MLX model, tokenizer lifecycle, and execution stream."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load_model(self) -> None:
        """Loads model weights and tokenizer into unified memory."""
        print(f"Loading {self.model_name}...")
        self.model, self.tokenizer = load(self.model_name)

    def generate_response(self, prompt: str, max_tokens: int = 32) -> Tuple[str, float]:
        """Runs generation and synchronizes the GPU stream for accurate timing."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        start_time = time.perf_counter()
        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            verbose=False
        )
        mx.synchronize()  # Force GPU stream synchronization
        elapsed_time = time.perf_counter() - start_time

        return response, elapsed_time


class ContextScalingBenchmark:
    """Orchestrates memory profiling across varying sequence lengths."""

    def __init__(self, engine: LLMEngine, tracker: MetalMemoryTracker):
        self.engine = engine
        self.tracker = tracker
        self.dummy_filler = "Agent reasoning step processing shared context information. "

    def _build_prompt_of_length(self, target_tokens: int) -> str:
        """Constructs an exact prompt matching the target token length."""
        tokens: List[int] = []
        raw_text = ""

        while len(tokens) < target_tokens:
            raw_text += self.dummy_filler
            tokens = self.engine.tokenizer.encode(raw_text)

        exact_tokens = tokens[:target_tokens]
        return self.engine.tokenizer.decode(exact_tokens)

    def run(self, context_lengths: List[int]) -> None:
        """Executes the scaling benchmark suite."""
        self.engine.load_model()

        print("\n--- Day 2: KV Cache Memory Scaling Profile ---")
        for length in context_lengths:
            prompt = self._build_prompt_of_length(length)

            # Reset hardware tracking right before the prefill pass
            self.tracker.reset()

            _, elapsed = self.engine.generate_response(prompt, max_tokens=32)
            snapshot = self.tracker.capture()

            print(f"\n[Context Length: {length} tokens]")
            print(f"  └─ Prefill + 32 Tokens Time : {elapsed:.2f}s")
            print(f"  └─ Active Memory            : {snapshot.active_mb} MB")
            print(f"  └─ Peak Memory              : {snapshot.peak_mb} MB")

        print("\n----------------------------------------------")


if __name__ == "__main__":
    # Dependency Injection
    tracker_service = MetalMemoryTracker()
    engine_service = LLMEngine("mlx-community/Llama-3.2-1B-Instruct-4bit")

    benchmark = ContextScalingBenchmark(
        engine=engine_service,
        tracker=tracker_service
    )

    benchmark.run(context_lengths=[256, 1024, 2048])