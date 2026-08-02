import sys
import os

# Ensure project root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_native_bindings():
    print("\n--- Stage 4: Testing Compiled C++ Pybind11 Extension ---")
    try:
        import _hetero_edge_cpp as native
    except ImportError as e:
        print(f"❌ Failed to import compiled C++ extension: {e}")
        print("💡 Hint: Ensure `pip install -e . --no-build-isolation` completed successfully.")
        return

    # 1. Test TelemetryEngine in C++
    telemetry = native.TelemetryEngine()
    metrics = telemetry.sample_metrics()
    
    print("\n[Native C++ Telemetry Output]")
    print(f"  ├─ Total System RAM : {metrics.total_ram_gb:.2f} GB")
    print(f"  ├─ Free System RAM  : {metrics.free_ram_gb:.2f} GB")
    print(f"  ├─ Used System RAM  : {metrics.used_ram_gb:.2f} GB")
    print(f"  └─ Thermal Level    : {native.TelemetryEngine.thermal_level_to_string(metrics.thermal_pressure_level)}")

    # 2. Test HardwareAwareScheduler in C++
    thresholds = native.PolicyThresholds()
    scheduler = native.HardwareAwareScheduler(thresholds)
    recommended_precision = scheduler.determine_precision(metrics)

    print("\n[Native C++ Precision Policy Recommendation]")
    print(f"  └─ Decision : {native.HardwareAwareScheduler.precision_to_string(recommended_precision)}")

    print("\n---------------------------------------------------------\n")


if __name__ == "__main__":
    test_native_bindings()
