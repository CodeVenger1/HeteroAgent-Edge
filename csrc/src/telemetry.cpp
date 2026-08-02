#include "telemetry.hpp"

#include <mach/mach.h>
#include <mach/mach_host.h>
#include <sys/sysctl.h>
#include <unistd.h>
#include <iostream>

namespace hetero_edge {

TelemetryEngine::TelemetryEngine() {}

HardwareMetrics TelemetryEngine::sample_metrics() {
    HardwareMetrics metrics{0.0, 0.0, 0.0, 0};

    // 1. Query Total Physical RAM via sysctl
    int mib[2] = {CTL_HW, HW_MEMSIZE};
    int64_t total_bytes = 0;
    size_t length = sizeof(total_bytes);
    if (sysctl(mib, 2, &total_bytes, &length, nullptr, 0) == 0) {
        metrics.total_ram_gb = static_cast<double>(total_bytes) / (1024.0 * 1024.0 * 1024.0);
    }

    // 2. Query Free and Active RAM via Mach VM statistics
    mach_port_t host_port = mach_host_self();
    mach_msg_type_number_t host_size = sizeof(vm_statistics64_data_t) / sizeof(integer_t);
    vm_statistics64_data_t vm_stat;

    if (host_statistics64(host_port, HOST_VM_INFO64, (host_info64_t)&vm_stat, &host_size) == KERN_SUCCESS) {
        int64_t page_size = sysconf(_SC_PAGESIZE);
        int64_t free_pages = vm_stat.free_count + vm_stat.inactive_count;
        metrics.free_ram_gb = static_cast<double>(free_pages * page_size) / (1024.0 * 1024.0 * 1024.0);
        metrics.used_ram_gb = metrics.total_ram_gb - metrics.free_ram_gb;
    }

    // 3. Query Apple Silicon Thermal Pressure Level
    int thermal_level = 0;
    size_t thermal_len = sizeof(thermal_level);
    if (sysctlbyname("machdep.xcpm.cpu_thermal_level", &thermal_level, &thermal_len, nullptr, 0) == 0) {
        metrics.thermal_pressure_level = thermal_level;
    } else {
        // Fallback default: Nominal
        metrics.thermal_pressure_level = 0;
    }

    return metrics;
}

std::string TelemetryEngine::thermal_level_to_string(int32_t level) {
    switch (level) {
        case 0: return "NOMINAL";
        case 1: return "MODERATE";
        case 2: return "HEAVY";
        case 3: return "CRITICAL/TRAPPING";
        default: return "UNKNOWN";
    }
}

} 