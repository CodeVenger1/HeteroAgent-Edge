#include "scheduler.hpp"

namespace hetero_edge {

HardwareAwareScheduler::HardwareAwareScheduler(PolicyThresholds thresholds)
    : thresholds_(thresholds) {}

PrecisionMode HardwareAwareScheduler::determine_precision(const HardwareMetrics& metrics) const {
    double ram_usage_pct = (metrics.total_ram_gb > 0) 
        ? (metrics.used_ram_gb / metrics.total_ram_gb) 
        : 0.0;

    // Rule 1: Under heavy thermal throttling or severe RAM pressure, drop to INT4
    if (metrics.thermal_pressure_level >= 2 || ram_usage_pct >= 0.90) {
        return PrecisionMode::INT4;
    }

    // Rule 2: Under moderate thermal or elevated RAM pressure, drop to INT8
    if (metrics.thermal_pressure_level >= thresholds_.max_thermal_level || 
        ram_usage_pct >= thresholds_.max_ram_usage_pct) {
        return PrecisionMode::INT8;
    }

    // Default to full FP16 speed/quality balance
    return PrecisionMode::FP16;
}

std::string HardwareAwareScheduler::precision_to_string(PrecisionMode mode) {
    switch (mode) {
        case PrecisionMode::FP16: return "FP16 (Unquantized)";
        case PrecisionMode::INT8: return "INT8 (Medium Compression)";
        case PrecisionMode::INT4: return "INT4 (High Compression)";
    }
    return "FP16";
}

}