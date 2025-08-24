rm -rf build dist
rm -f *.c
rm -f *.so
python setup.py build_ext --inplace
mkdir -p dist
mv *.so dist/
pyinstaller beck-view-movie-gui.spec --noconfirm
mv dist/beck-view-movie-gui-bundle/beck-view-movie-gui .
chmod +x ./beck-view-movie-gui
dir=$(pwd -P)
echo 'Executable `beck-view-movie-gui` ready for usage in directory' $dir