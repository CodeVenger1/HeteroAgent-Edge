#ifndef HETERO_EDGE_SCHEDULER_HPP
#define HETERO_EDGE_SCHEDULER_HPP

#include "telemetry.hpp"

namespace hetero_edge {

enum class PrecisionMode {
    FP16 = 0,
    INT8 = 1,
    INT4 = 2
};

struct PolicyThresholds {
    double max_ram_usage_pct = 0.85;  // Trigger quantization above 85% RAM usage
    int32_t max_thermal_level = 1;     // Trigger INT4 quantization if thermal level >= Moderate
};

class HardwareAwareScheduler {
private:
    PolicyThresholds thresholds_;

public:
    explicit HardwareAwareScheduler(PolicyThresholds thresholds = PolicyThresholds());

    // Evaluates current hardware state and decides appropriate bit-precision
    PrecisionMode determine_precision(const HardwareMetrics& metrics) const;

    static std::string precision_to_string(PrecisionMode mode);
};

} // namespace hetero_edge

#endif