import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hetero_edge.engine import HeteroEdgeEngine

def test_engine_orchestration():
    print("\n--- Stage 5: Testing High-Level HeteroEdgeEngine Wrapper ---")
    
    engine = HeteroEdgeEngine()
    
    # 1. Test Hardware Telemetry Sampling
    status = engine.sample_hardware_status()
    print("\n[Engine Telemetry Status]")
    print(f"  ├─ Total Unified Memory : {status['total_ram_gb']} GB")
    print(f"  ├─ Available RAM        : {status['free_ram_gb']} GB")
    print(f"  ├─ Used RAM             : {status['used_ram_gb']} GB")
    print(f"  └─ System Thermal State : {status['thermal_level']}")

    # 2. Test Policy Precision Evaluation
    precision = engine.evaluate_precision_policy()
    print(f"\n[Evaluated Precision Decision]: {precision}")

    # 3. Test PagedAttention KV-Cache Memory Allocation
    print("\n[Simulating PagedAttention KV Allocation]")
    success = engine.allocate_kv_cache_pages(num_pages=512, page_size_kb=128)
    print(f"  └─ Allocation Granted: {success}")

    # 4. Test Hardware-Aware Inference Step
    print("\n[Running Simulated Hardware-Aware Inference Step]")
    result = engine.execute_inference_step("Define hardware-aware LLM scheduling.")
    print(f"  ├─ Prompt: '{result['prompt']}'")
    print(f"  ├─ Precision Selected: {result['execution_precision']}")
    print(f"  └─ Result: {result['status']}")

    print("\n---------------------------------------------------------\n")

if __name__ == "__main__":
    test_engine_orchestration()