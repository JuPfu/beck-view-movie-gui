# Beck View Movie GUI

**Beck View Movie GUI** is a cross‑platform graphical frontend for the
[`beck-view-movie`](https://github.com/JuPfu/beck-view-movie) command‑line application.

It provides a user‑friendly way to configure all movie‑generation parameters and
executes `beck-view-movie` as an external process while displaying its live output
inside the GUI.

The application is written in Python and uses **ttkbootstrap** to provide a modern,
consistent look and feel on Windows, macOS, and Linux.

![Beck View Movie GUI](./assets/img/beck-view-movie-gui.png)

*beck-view-movie-gui after successfully assembling 3600 digitised images into a movie.*

---

## 🚀 Features

* Graphical user interface for the `beck-view-movie` CLI tool
* GUI controls for **all relevant command‑line options**
* Configuration of:

  * Input image directory
  * Output movie directory and base name
  * Frame rate (FPS)
  * Resolution and scaling
  * Container format, and compression settings
  * Vertical and horizontal mirroring of digitised images
* Automatic construction of a valid `beck-view-movie` command line
* Launches `beck-view-movie` as a **subprocess**
* Displays **real‑time stdout / stderr output** in the GUI
* **Stop button** to terminate the running process cleanly

---

## 🧰 Requirements

* Python **3.12 or newer**
* A working build of
  [`beck-view-movie`](https://github.com/JuPfu/beck-view-movie)
* All Python dependencies are installed automatically by the installer scripts

---

## 📦 Installation

Installation is performed via the provided platform-specific installer scripts.

The scripts will:

* create a local Python virtual environment
* install all required Python dependencies
* build the GUI using **Cython**
* create a platform-specific executable using **PyInstaller**

### 🔹 Linux / macOS

```bash
git clone https://github.com/JuPfu/beck-view-movie-gui.git
cd beck-view-movie-gui
./install.sh
```

If required, make the script executable first:

```bash
chmod +x install.sh
```

---

### 🔹 Windows

```bat
git clone https://github.com/JuPfu/beck-view-movie-gui.git
cd beck-view-movie-gui
install.bat
```

---

## ▶️ Usage

After installation, the application can be run either via the generated
executable or directly via Python.

### Run the executable

#### Linux / macOS

```bash
./beck-view-movie-gui
```

#### Windows

```bat
beck-view-movie-gui.exe
```

---

### Run via Python (development mode)

```bash
python beck-view-movie-gui.py
```

---

## 🖥️ How It Works

1. The GUI collects all selected parameters from the user interface.
2. These parameters are translated into a valid `beck-view-movie` command line.
3. The command is executed as a subprocess.
4. Console output is streamed live into the GUI log window.
5. The running process can be terminated at any time using the **Stop** button.

The GUI itself does **not** perform video processing; all heavy lifting is done
by `beck-view-movie`.

---

## 👥 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

   ```bash
   git checkout -b my-feature
   ```
3. Implement your changes
4. Commit with a clear message

   ```bash
   git commit -am "Add feature X"
   ```
5. Push the branch

   ```bash
   git push origin my-feature
   ```
6. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## 🧯 Troubleshooting

**The executable does not start**

* Ensure the installation script completed without errors
* Verify that Python 3.12+ is available on your system
* On Linux/macOS, check executable permissions:

  ```bash
  chmod +x beck-view-movie-gui
  ```

**`beck-view-movie` cannot be found or fails to run**

* Make sure `beck-view-movie` is built and accessible
* Verify that the executable or script is available in the expected location
* Try running `beck-view-movie` manually from a terminal to confirm it works

**GUI starts but no output is shown**

* Check that the selected input directory contains valid image files
* Verify write permissions for the selected output directory

If problems persist, please open a GitHub issue and include:

* your operating system
* Python version
* console output from the installer script

---

## 📬 Contact

For bug reports, feature requests, or questions, please open an issue on GitHub.
