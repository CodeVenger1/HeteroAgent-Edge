#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "../csrc/include/telemetry.hpp"
#include "../csrc/include/scheduler.hpp"

namespace py = pybind11;
using namespace hetero_edge;

PYBIND11_MODULE(_hetero_edge_cpp, m) {
    m.doc() = "C++ Core Engine bindings for HeteroAgent-Edge";

    // 1. Expose HardwareMetrics Struct
    py::class_<HardwareMetrics>(m, "HardwareMetrics")
        .def(py::init<>())
        .def_readwrite("total_ram_gb", &HardwareMetrics::total_ram_gb)
        .def_readwrite("free_ram_gb", &HardwareMetrics::free_ram_gb)
        .def_readwrite("used_ram_gb", &HardwareMetrics::used_ram_gb)
        .def_readwrite("thermal_pressure_level", &HardwareMetrics::thermal_pressure_level)
        .def("__repr__", [](const HardwareMetrics& m) {
            return "<HardwareMetrics Total RAM=" + std::to_string(m.total_ram_gb) +
                   "GB, Used=" + std::to_string(m.used_ram_gb) +
                   "GB, Thermal=" + std::to_string(m.thermal_pressure_level) + ">";
        });

    // 2. Expose TelemetryEngine Class
    py::class_<TelemetryEngine>(m, "TelemetryEngine")
        .def(py::init<>())
        .def("sample_metrics", &TelemetryEngine::sample_metrics)
        .def_static("thermal_level_to_string", &TelemetryEngine::thermal_level_to_string);

    // 3. Expose PrecisionMode Enum
    py::enum_<PrecisionMode>(m, "PrecisionMode")
        .value("FP16", PrecisionMode::FP16)
        .value("INT8", PrecisionMode::INT8)
        .value("INT4", PrecisionMode::INT4)
        .export_values();

    // 4. Expose PolicyThresholds Struct
    py::class_<PolicyThresholds>(m, "PolicyThresholds")
        .def(py::init<>())
        .def_readwrite("max_ram_usage_pct", &PolicyThresholds::max_ram_usage_pct)
        .def_readwrite("max_thermal_level", &PolicyThresholds::max_thermal_level);

    // 5. Expose HardwareAwareScheduler Class
    py::class_<HardwareAwareScheduler>(m, "HardwareAwareScheduler")
        .def(py::init<PolicyThresholds>(), py::arg("thresholds") = PolicyThresholds())
        .def("determine_precision", &HardwareAwareScheduler::determine_precision)
        .def_static("precision_to_string", &HardwareAwareScheduler::precision_to_string);
}