# cc-P690: the whole swapped world, played through (SoS swap S17)

Iron Golem, 2026-10-30 03:39. Both work copies on `golem/Iron/P690` (main at the P688 merge). Nothing changed, built
or run: stopped before starting.

## In plain words

- **The playthrough has not started.** Chases-Tower is still out of memory: Windows' own kernel memory holds 39 GB
  (27.7 GB paged, 11.7 GB nonpaged, up from 32 GB on 10-29), and 0.9 GB was free. The last reboot was 10-26 13:04.
- The run needs a Docker image build, a fresh private world and two game clients at once, several GB in all.
- **For you:** a question on the Golem card (Iron-P690-20261030-033912-f5a0): wait for the reboot, write the plan
  now and run later, or put P690 back in the queue.

## What was checked

| Check | Result |
|---|---|
| Free memory (`Win32_OperatingSystem`) | 1.1 GB of 31.7 GB |
| Kernel pools (`Win32_PerfFormattedData_PerfOS_Memory`) | paged 27.7 GB, nonpaged 11.7 GB, committed 87.5 GB, available 0.9 GB |
| Largest processes | Memory Compression 3.2 GB, vmmemWSL 1.6 GB; nothing large of ours running |
| Last boot | 2026-10-26 13:04 |
| Prompts the playthrough depends on | P691 (Blackthorn into the Fold) not merged; P689 (credits) committed, not yet on main |

Chase's rule on 10-29 (answer Iron-P688-20261029-125544-04f6): on low memory, stop and ask rather than fail. No lock
was taken.

P690 STOPPED: asked Chase (Iron-P690-20261030-033912-f5a0)
