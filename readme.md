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
- [x] :zap: Demo on simplified illustration on timing attack on AES[^4].. 
Consider the variable-index array lookup T0[k[0]⊕n[0]] near the beginning of the AES computation. One might speculate that the time for this array lookup depends on the array index; that the time for the whole AES computation is well correlated with the time for this array lookup; that, consequently, the AES timings leak information about k[0] ⊕ n[0]; and that one can deduce the exact value of k[0] from the distribution of AES timings as a function of n[0]. Similar comments apply to k[1] ⊕ n[1], k[2] ⊕ n[2], etc.

Assume, for example, that the attacker
- watches the time taken by the victim to handle many n’s,
- totals the AES times for each possible n[13], and
- observes that the overall AES time is maximum when n[13] is, say, 147.

Assume that the attacker also observes, by carrying out experiments with known keys k on a computer with the same AES software and the same CPU, that the overall AES time is maximum when k[13]⊕n[13] is, say, 8. The attacker concludes that the victim’s k[13] is 147 ⊕ 8 = 155.


[^1]: [demo_delay_by_call_function.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_call_function.py)  
  Delays introduced by calling different functions.
[^2]: [demo_delay_by_conditional_branching.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_conditional_branching.py)  
  Delays introduced by conditional branching.
[^3]: [demo_delay_by_process_condition_breaking.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_delay_by_process_condition_breaking.py)  
  Delays introduced by different processes or instructions.
[^4]: [demo_simplified_timing_attack_on_key_xor_part.py](https://github.com/ursa-mikail/demo_timing_attack/blob/main/demo_simplified_timing_attack_on_key_xor_part.py)  
  Demo on simplified illustration on timing attack on AES.

<hr>

## Avoid table look-ups indexed by secret data

### Problem

The access time of a table element can vary with its index (depending for example on whether a cache-miss has occured). This has for example been exploited in a series of cache-timing attacks on AES.

### Solution

Replace table look-up with sequences of constant-time logical operations, for example by bitslicing look-ups (as used in [NaCl's](http://nacl.cr.yp.to/) [implementation](http://eprint.iacr.org/2009/129.pdf) of AES-CTR, or in [Serpent](https://www.ii.uib.no/~osvik/serpent/).

For AES, constant-time non-bitsliced implementations are also [possible](http://crypto.stackexchange.com/questions/55/known-methods-for-constant-time-table-free-aes-implementation-using-standard/92#92), but are much slower. 

Where design uses a lookup table (called an S-Box) indexed by secret data, which is inherently vulnerable to [cache-timing attacks](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf).

There are workarounds for this AES vulnerability, but they either require hardware acceleration (AES-NI) or a technique called [bitslicing](https://github.com/jedisct1/libsodium/tree/1.0.14/src/libsodium/crypto_stream/aes128ctr/nacl).

The dilemma is often to choose between performance and security. You cannot get fast, constant-time  unless with hardware support, e.g. hardware acceleration.

<hr>

## Avoid secret-dependent loop bounds

### Problem

Loops with a bound derived from a secret value directly expose a program to timing attacks.

### Solution

Make sure that all loops are bounded by a constant (or at least a non-secret variable).

Ensure, as far as possible, that loop bounds and their potential underflow or overflow are independent of user-controlled input (> Caveat: [Heartbleed bug](http://heartbleed.com/)).


<hr>
