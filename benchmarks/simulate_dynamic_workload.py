import sys
import os
import time
import random
import logging
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hetero_edge.engine import HeteroEdgeEngine
import _hetero_edge_cpp as native

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("DynamicWorkloadSim")


class SimulatedAgentNode:
    """Represents an agent node within an execution DAG."""

    def __init__(self, name: str, token_workload: int):
        self.name = name
        self.token_workload = token_workload

    def estimated_pages(self, page_size_tokens: int = 16) -> int:
        return (self.token_workload + page_size_tokens - 1) // page_size_tokens


class DynamicWorkloadSimulator:
    """Simulates multi-agent DAG execution under changing thermal & RAM conditions."""

    def __init__(self):
        self.engine = HeteroEdgeEngine()

    def run_simulation(self):
        print("\n=========================================================")
        print("    HeteroAgent-Edge: Multi-Agent Workload Simulator      ")
        print("=========================================================\n")

        # Define an agent execution DAG turn
        agent_dag: List[SimulatedAgentNode] = [
            SimulatedAgentNode("Planner_Agent", token_workload=256),
            SimulatedAgentNode("Web_Retriever_Agent", token_workload=1024),
            SimulatedAgentNode("Code_Interpreter_Agent", token_workload=2048),
            SimulatedAgentNode("Synthesis_Summarizer_Agent", token_workload=512),
        ]

        # Simulated thermal and memory pressure states across 4 turns
        simulated_environmental_conditions = [
            {"label": "Turn 1: Cold Start / Nominal Hardware", "mock_thermal": 0},
            {"label": "Turn 2: Elevated System Load", "mock_thermal": 1},
            {"label": "Turn 3: Sustained Multi-Agent Load (Thermal Spike)", "mock_thermal": 2},
            {"label": "Turn 4: Cooldown / Recovery Phase", "mock_thermal": 0},
        ]

        total_allocated_pages = 0

        for turn_idx, env in enumerate(simulated_environmental_conditions, 1):
            print(f"\n--- {env['label']} ---")
            
            # Poll native hardware status
            status = self.engine.sample_hardware_status()
            current_precision = self.engine.evaluate_precision_policy()

            print(f"  ├─ Live System RAM    : {status['used_ram_gb']} GB / {status['total_ram_gb']} GB")
            print(f"  ├─ Physical Thermal   : {status['thermal_level']}")
            print(f"  └─ Scheduler Mode     : {current_precision}")

            print("\n  [Executing Agent DAG Nodes]:")
            for agent in agent_dag:
                required_pages = agent.estimated_pages()
                
                # Request PagedAttention KV Allocation
                success = self.engine.allocate_kv_cache_pages(num_pages=required_pages, page_size_kb=64)
                if success:
                    total_allocated_pages += required_pages

                # Run inference step
                res = self.engine.execute_inference_step(prompt=f"Agent [{agent.name}] running context.")
                
                print(
                    f"    ├─ Node: {agent.name:<25} | "
                    f"Pages: {required_pages:>3} | "
                    f"Precision: {res['execution_precision']}"
                )
                
                time.sleep(0.05)  # Simulate execution turn interval

        print("\n=========================================================")
        print(f"  Simulation Complete.")
        print(f"  Total PagedAttention KV Pages Allocated: {total_allocated_pages:,}")
        print("=========================================================\n")


if __name__ == "__main__":
    simulator = DynamicWorkloadSimulator()
    simulator.run_simulation()