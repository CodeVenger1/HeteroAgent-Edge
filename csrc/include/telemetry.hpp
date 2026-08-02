#ifndef HETERO_EDGE_TELEMETRY_HPP
#define HETERO_EDGE_TELEMETRY_HPP

#include <cstdint>
#include <string>

namespace hetero_edge {

struct HardwareMetrics {
    double total_ram_gb;
    double free_ram_gb;
    double used_ram_gb;
    int32_t thermal_pressure_level; // 0: Nominal, 1: Moderate, 2: Heavy, 3: Trapping
};

class TelemetryEngine {
public:
    TelemetryEngine();
    ~TelemetryEngine() = default;

    // Queries Apple Silicon hardware metrics via Mach and sysctl APIs
    HardwareMetrics sample_metrics();
    
    // Helper to map integer level to string representation
    static std::string thermal_level_to_string(int32_t level);
};

}

#endif