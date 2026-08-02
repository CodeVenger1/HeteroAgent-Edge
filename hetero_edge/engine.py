import logging
from typing import Dict, Any, Optional
import _hetero_edge_cpp as native

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("HeteroEdgeEngine")

class HeteroEdgeEngine:
    """
    High-level Python wrapper integrating C++ native macOS telemetry,
    hardware-aware scheduling policies, and dynamic MLX KV-cache management.
    """

    def __init__(self, policy_thresholds: Optional[native.PolicyThresholds] = None):
        logger.info("Initializing HeteroEdgeEngine...")
        
        # Instantiate native C++ telemetry & scheduler
        self.telemetry = native.TelemetryEngine()
        self.thresholds = policy_thresholds if policy_thresholds is not None else native.PolicyThresholds()
        self.scheduler = native.HardwareAwareScheduler(self.thresholds)
        
        # State tracking
        self.current_precision = "FP16"
        self.active_kv_pages = 0
        
        logger.info("HeteroEdgeEngine successfully initialized with native C++ bridge.")

    def sample_hardware_status(self) -> Dict[str, Any]:
        """Queries native C++ telemetry for real-time Unified Memory & thermal metrics."""
        metrics = self.telemetry.sample_metrics()
        thermal_str = native.TelemetryEngine.thermal_level_to_string(metrics.thermal_pressure_level)
        
        return {
            "total_ram_gb": round(metrics.total_ram_gb, 2),
            "free_ram_gb": round(metrics.free_ram_gb, 2),
            "used_ram_gb": round(metrics.used_ram_gb, 2),
            "thermal_level": thermal_str
        }

    def evaluate_precision_policy(self) -> str:
        """Evaluates hardware pressure via C++ scheduler and determines execution precision."""
        metrics = self.telemetry.sample_metrics()
        recommended_enum = self.scheduler.determine_precision(metrics)
        precision_str = native.HardwareAwareScheduler.precision_to_string(recommended_enum)
        
        if precision_str != self.current_precision:
            logger.warning(
                f"Precision shift trigger: {self.current_precision} ➔ {precision_str} "
                f"(Free RAM: {metrics.free_ram_gb:.2f}GB)"
            )
            self.current_precision = precision_str
            
        return precision_str

    def allocate_kv_cache_pages(self, num_pages: int, page_size_kb: int = 64) -> bool:
        """Simulates zero-copy PagedAttention KV-cache allocation with telemetry checks."""
        status = self.sample_hardware_status()
        required_mb = (num_pages * page_size_kb) / 1024.0
        
        logger.info(f"Requesting allocation: {num_pages} KV pages (~{required_mb:.2f} MB)")
        
        # Safety check: Prevent allocation if free RAM is critically low (< 1.5 GB)
        if status["free_ram_gb"] < 1.5:
            logger.error("Allocation denied: Available Unified Memory below safety threshold!")
            return False
            
        self.active_kv_pages += num_pages
        logger.info(f"Allocation granted. Active KV pages: {self.active_kv_pages}")
        return True

    def execute_inference_step(self, prompt: str) -> Dict[str, Any]:
        """Runs a hardware-conditioned inference step with dynamic precision resolution."""
        precision = self.evaluate_precision_policy()
        status = self.sample_hardware_status()
        
        return {
            "status": "SUCCESS",
            "prompt": prompt,
            "execution_precision": precision,
            "system_thermal_state": status["thermal_level"],
            "free_ram_gb": status["free_ram_gb"]
        }