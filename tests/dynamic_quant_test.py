import sys
import os
import time
from dataclasses import dataclass

# Ensure project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hetero_edge.profiler import MetalMemoryTracker


@dataclass
class SimulatedMetrics:
    ram_usage_pct: float
    thermal_level: int  # 0: Nominal, 1: Moderate, 2: Heavy


class PolicyEngine:
    """Python prototype of the C++ HardwareAwareScheduler."""

    def __init__(self, ram_threshold: float = 0.85, thermal_threshold: int = 1):
        self.ram_threshold = ram_threshold
        self.thermal_threshold = thermal_threshold

    def evaluate_precision(self, metrics: SimulatedMetrics) -> str:
        if metrics.thermal_level >= 2 or metrics.ram_usage_pct >= 0.90:
            return "INT4 (Extreme Compression)"
        elif metrics.thermal_level >= self.thermal_threshold or metrics.ram_usage_pct >= self.ram_threshold:
            return "INT8 (Moderate Quantization)"
        return "FP16 (Full Precision)"


def run_day3_benchmark():
    print("\n--- Day 3: Dynamic Quantization & Thermal Policy Validation ---")
    tracker = MetalMemoryTracker()
    policy = PolicyEngine(ram_threshold=0.85, thermal_threshold=1)

    # Simulated runtime scenarios representing dynamic edge conditions
    test_scenarios = [
        ("Ideal Operational State", SimulatedMetrics(ram_usage_pct=0.45, thermal_level=0)),
        ("High Memory Allocation Pressure", SimulatedMetrics(ram_usage_pct=0.87, thermal_level=0)),
        ("Sustained Load / Thermal Rise", SimulatedMetrics(ram_usage_pct=0.75, thermal_level=1)),
        ("Critical Thermal Throttling Event", SimulatedMetrics(ram_usage_pct=0.92, thermal_level=2)),
    ]

    for name, state in test_scenarios:
        tracker.reset()
        precision = policy.evaluate_precision(state)
        time.sleep(0.1)  # Simulate scheduling clock cycle delay

        print(f"\n[Scenario: {name}]")
        print(f"  ├─ RAM Usage           : {state.ram_usage_pct * 100:.1f}%")
        print(f"  ├─ Thermal State Level : {state.thermal_level}")
        print(f"  └─ Selected Precision  : {precision}")

    print("\n--------------------------------------------------------------")


if __name__ == "__main__":
    run_day3_benchmark()