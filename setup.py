from setuptools import setup, Extension
import Cython.Build as cb
import platform

from glob import glob
from os.path import splitext, basename

compile_args = ["-O3"] if platform.system() != "Windows" else ["/O2"]
pyx_files = glob("*.pyx")

extensions = [
    Extension(
        name=splitext(basename(pyx_file))[0],
        sources=[pyx_file],
        extra_compile_args=compile_args
    )
    for pyx_file in pyx_files
]

setup(
    name='beck_view_movie_gui',
    version='1.2',
    url='https://github.com/JuPfu/beck-view-movie-gui',
    license='MIT licence',
    author='Juergen Pfundt',
    author_email='juergen.pfundt@gmail.com',
    description='GUI for Beck-View-Movie',
    ext_modules = cb.cythonize(
        extensions,
        compiler_directives={
            "boundscheck": False,
            "wraparound": False,
            "initializedcheck": False,
            "cdivision": True,
            "language_level": 3,
        }
    )
)