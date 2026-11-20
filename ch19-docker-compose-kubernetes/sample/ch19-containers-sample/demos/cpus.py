"""What Python sees inside a container with CPU limits."""

import os
from pathlib import Path

v2 = Path("/sys/fs/cgroup/cpu.max")
v1 = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
if v2.exists():
    quota, period = v2.read_text().split()
else:
    quota = v1.read_text().strip()
    period = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text().strip()
print(f"os.cpu_count()={os.cpu_count()} os.process_cpu_count()={os.process_cpu_count()}"
      f" cgroup quota={quota} period={period}")
