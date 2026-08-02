from dataclasses import dataclass
import mlx.core as mx


@dataclass
class MemorySnapshot:
    """Value object holding hardware memory state in Megabytes."""
    active_mb: float
    peak_mb: float


class MetalMemoryTracker:
    """Encapsulates Metal API memory telemetry on Apple Silicon."""

    @staticmethod
    def _bytes_to_mb(bytes_val: int) -> float:
        return round(bytes_val / (1024 * 1024), 2)

    def reset(self) -> None:
        """Resets the peak memory hardware counter."""
        mx.reset_peak_memory()

    def capture(self) -> MemorySnapshot:
        """Captures active and peak memory snapshots from the Metal API."""
        return MemorySnapshot(
            active_mb=self._bytes_to_mb(mx.get_active_memory()),
            peak_mb=self._bytes_to_mb(mx.get_peak_memory())
        )