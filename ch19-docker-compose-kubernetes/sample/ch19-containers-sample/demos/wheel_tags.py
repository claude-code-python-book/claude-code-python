"""Which wheel can pip or uv install? It depends on the C library's platform tags."""

from packaging import tags
from packaging.utils import parse_wheel_filename

glibc = set(tags.cpython_tags((3, 13)))  # this machine: glibc (Debian-like)
musl = set(tags.cpython_tags((3, 13), platforms=["musllinux_1_2_x86_64",
                                                 "musllinux_1_1_x86_64"]))  # Alpine

wheels = [
    "pydantic_core-2.46.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "pydantic_core-2.46.5-cp313-cp313-musllinux_1_1_x86_64.whl",
]
for name in wheels:
    wheel_tags = parse_wheel_filename(name)[3]
    print(name.split("-", 4)[-1].removesuffix(".whl"))
    print(f"    glibc (slim): {bool(wheel_tags & glibc)}   musl (alpine): {bool(wheel_tags & musl)}")
