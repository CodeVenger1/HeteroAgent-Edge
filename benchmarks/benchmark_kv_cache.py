import sys
import os
import time
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Suppress debug logs during benchmarking
logging.getLogger("HeteroEdgeEngine").setLevel(logging.ERROR)

from hetero_edge.engine import HeteroEdgeEngine

def run_kv_cache_benchmark():
    print("=========================================================")
    print("       HeteroAgent-Edge: KV-Cache Allocation Benchmark   ")
    print("=========================================================\n")

    engine = HeteroEdgeEngine()
    
    # Benchmark Parameters
    num_allocations = 10_000
    pages_per_alloc = 16
    page_size_kb = 64
    
    total_pages = num_allocations * pages_per_alloc
    total_data_mb = (total_pages * page_size_kb) / 1024.0

    print(f"[Benchmark Configuration]")
    print(f"  ├─ Iterations         : {num_allocations:,}")
    print(f"  ├─ Pages / Iteration  : {pages_per_alloc}")
    print(f"  ├─ Page Size          : {page_size_kb} KB")
    print(f"  ├─ Total Pages        : {total_pages:,}")
    print(f"  └─ Total Simulated MB : {total_data_mb:.2f} MB\n")

    print("Executing benchmark runs...")
    
    start_time = time.perf_counter()
    successful_allocs = 0

    for _ in range(num_allocations):
        if engine.allocate_kv_cache_pages(num_pages=pages_per_alloc, page_size_kb=page_size_kb):
            successful_allocs += 1

    end_time = time.perf_counter()
    
    total_time_sec = end_time - start_time
    time_per_alloc_us = (total_time_sec / num_allocations) * 1_000_000
    throughput_pages_per_sec = total_pages / total_time_sec
    throughput_mb_per_sec = total_data_mb / total_time_sec

    print("\n[Benchmark Results]")
    print(f"  ├─ Successful Allocs  : {successful_allocs:,} / {num_allocations:,}")
    print(f"  ├─ Total Time Elapsed : {total_time_sec * 1000:.2f} ms")
    print(f"  ├─ Mean Latency/Alloc : {time_per_alloc_us:.3f} µs")
    print(f"  ├─ Page Throughput    : {throughput_pages_per_sec:,.2f} pages/sec")
    print(f"  └─ Bandwidth Rate     : {throughput_mb_per_sec:,.2f} MB/sec")
    print("=========================================================\n")

if __name__ == "__main__":
    run_kv_cache_benchmark()