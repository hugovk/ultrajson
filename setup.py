import platform
import shlex
from glob import glob
from os import environ, pathsep

from setuptools import Extension, setup

dconv_includes = [
    dir
    for dir in environ.get(
        "UJSON_BUILD_DC_INCLUDES",
        "./src/_vendor/double-conversion/double-conversion",
    ).split(pathsep)
    if dir
]
dconv_libs = shlex.split(environ.get("UJSON_BUILD_DC_LIBS", ""))
dconv_source_files = []
if not dconv_libs:
    dconv_source_files.extend(
        glob("./src/_vendor/double-conversion/double-conversion/*.cc")
    )
dconv_source_files.append("./src/lib/dconv_wrapper.cc")

if platform.system() == "Linux" and environ.get("UJSON_BUILD_NO_STRIP", "0") not in (
    "1",
    "True",
):
    strip_flags = ["-Wl,--strip-all"]
else:
    strip_flags = []

module1 = Extension(
    "ujson",
    sources=dconv_source_files
    + [
        "./src/python/ujson.c",
        "./src/python/objToJSON.c",
        "./src/python/JSONtoObj.c",
        "./src/lib/ultrajsonenc.c",
        "./src/lib/ultrajsondec.c",
    ],
    include_dirs=["./src/python", "./src/lib"] + dconv_includes,
    extra_compile_args=["-D_GNU_SOURCE"],
    extra_link_args=["-lstdc++", "-lm"] + dconv_libs + strip_flags,
)

with open("src/python/version_template.h") as f:
    version_template = f.read()


setup(
    ext_modules=[module1],
)
