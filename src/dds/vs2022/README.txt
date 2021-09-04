Visual Studio 2022 solution (.sln) and project (*.vc*) files for building Bo Haglund's Double Dummy Solver.
The files build dds.dll, dtest.exe, itest.exe and DealerPar.exe projects.

The dds github is at: https://github.com/dds-bridge/dds

Put the files into a directory (e.g. VS2022) at same directory level and src, hands, test, etc.
The project files expect source files to be in ../src and ../test. dtest expects data to be in ../hands.

Multithreading is enabled for openmp, stl and winapi. Choose multithreading implementation using the -t switch.
Other implementations may work but they're untested. Multithreading is enabled by specifying compiler defs in .vcxproj files.

A Visual Studio template is provided for creating additional projects from the examples directory.
