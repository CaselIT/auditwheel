import os
import subprocess

from setuptools import Extension, setup

cmd = "gcc -fPIC -shared -o b/libb.so b/b.c"
subprocess.check_call(cmd.split())
cmd = (
    "gcc -fPIC -shared -o a/liba.so "
    "-Wl,{dtags_flag} -Wl,-rpath=$ORIGIN/../b "
    "-Ib a/a.c -Lb -lb"
).format(
    dtags_flag=(
        "--enable-new-dtags"
        if os.getenv("DTAG") == "runpath"
        else "--disable-new-dtags"
    )
)
subprocess.check_call(cmd.split())

setup(
    name="testrpath",
    version="0.0.1",
    packages=["testrpath"],
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            "testrpath/testrpath",
            sources=["src/testrpath/testrpath.c"],
            include_dirs=["a"],
            libraries=["a"],
            library_dirs=["a"],
        )
    ],
)
