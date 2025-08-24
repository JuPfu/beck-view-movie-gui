rmdir /S /Q build
rmdir /S /Q dist
del *.c *.pyd
python3 setup.py build_ext --inplace
mkdir dist
move *.pyd dist
pyinstaller beck-view-movie-gui.spec --noconfirm
copy /y dist\beck-view-movie-gui-bundle\beck-view-movie-gui.exe "%CD%"
echo "Executable `beck-view-movie-gui.exe` ready for usage in directory %CD%"