import asyncio
import os
import platform
import signal
import subprocess
import time
import tkinter
from asyncio import Task
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tooltip import ToolTip

beck_view_font = ("Helvetica", 14)


class FrameInputDirectory(ttk.LabelFrame):
    from tkinter.filedialog import askdirectory

    @staticmethod
    def show_directory_dialog(must_exist) -> str:
        path = FrameInputDirectory.askdirectory(title="Verzeichnis mit digitalisierten Bildern",
                                                initialdir=".",
                                                mustexist=must_exist)
        return r'{}'.format(path)

    def __init__(self, master):
        super().__init__(master)

        self.configure(borderwidth=3, text="Ordner mit digitalisierten Bildern auswählen", relief=SOLID)
        self.input_directory_label = ttk.Label(self, text="Verzeichnis", font=beck_view_font)
        self.input_directory_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.input_directory_path = ttk.Entry(self, font=beck_view_font, takefocus=0)
        self.input_directory_path.insert(0, os.getcwd())
        self.input_directory_path.configure(state=ttk.READONLY)
        self.input_directory_path.grid(row=0, column=1, pady=(10, 10), sticky="ew")

        s = ttk.Style()
        s.configure('Beck-View_Movie-GUI.TButton', font=beck_view_font)
        self.input_directory_button = ttk.Button(self,
                                                 text="Auswählen",
                                                 style="Beck-View_Movie-GUI.TButton",
                                                 command=self.input_directory_button_callback)
        self.input_directory_button.grid(row=0, column=2, padx=(10, 10))
        ToolTip(self.input_directory_button,
                text="Öffnet den Dialog zur Auswahl des Ordners in dem sich digitalisierte Bilder befinden.",
                bootstyle="INFO, INVERSE")

    def input_directory_button_callback(self):
        path = FrameInputDirectory.show_directory_dialog(True)
        self.input_directory_path.configure(state=ttk.NORMAL)
        text = self.input_directory_path.get()
        if len(path) > 0:
            self.input_directory_path.delete(0, len(text))
            self.input_directory_path.insert(index=0, string=path)
        self.input_directory_path.configure(state=ttk.READONLY)


class FrameOutputDirectory(ttk.LabelFrame):
    from tkinter.filedialog import askdirectory

    @staticmethod
    def show_directory_dialog(must_exist) -> str:
        path = FrameOutputDirectory.askdirectory(title="Ausgabeverzeichnis für den generierten Film festlegen",
                                                 initialdir=".",
                                                 mustexist=must_exist)
        return r'{}'.format(path)

    def __init__(self, master):
        super().__init__(master)

        self.configure(borderwidth=3, text="Name und Ausgabeverzeichnis für den generierten Film festlegen",
                       relief=SOLID)

        self.filename_label = ttk.Label(self, text="Dateiname", font=beck_view_font)
        self.filename_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.filename = tkinter.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.filename, font=beck_view_font)

        self.filename.set("beck-view-movie")
        self.entry.grid(row=0, column=1, padx=(0, 0), pady=(10, 10), sticky="ew")

        self.output_directory_label = ttk.Label(self, text="Verzeichnis", font=beck_view_font)
        self.output_directory_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.output_directory_path = ttk.Entry(self, font=beck_view_font, takefocus=0)
        self.output_directory_path.insert(0, os.getcwd())
        self.output_directory_path.configure(state=ttk.READONLY)
        self.output_directory_path.grid(row=1, column=1, pady=(10, 10), sticky="ew")

        s = ttk.Style()
        s.configure('Beck-View_Movie-GUI.TButton', font=beck_view_font)
        self.output_directory_button = ttk.Button(self,
                                                  text="Auswählen",
                                                  style="Beck-View_Movie-GUI.TButton",
                                                  command=self.directory_button_callback)
        self.output_directory_button.grid(row=1, column=2, padx=(10, 10))
        ToolTip(self.output_directory_button,
                text="Öffnet den Dialog zur Auswahl des Ordners in dem sich digitalisierte Bilder befinden.",
                bootstyle="INFO, INVERSE")

    def directory_button_callback(self):
        path = FrameOutputDirectory.show_directory_dialog(False)
        self.output_directory_path.configure(state=ttk.NORMAL)
        text = self.output_directory_path.get()
        if len(path) > 0:
            self.output_directory_path.delete(0, len(text))
            self.output_directory_path.insert(index=0, string=path)
        self.output_directory_path.configure(state=ttk.READONLY)


class TechnicalAttributes(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(borderwidth=3, text="Performance-Tuning", relief=SOLID)
        row = 0

        self.batch_label = ttk.Label(self, font=beck_view_font,
                                     text="Anzahl Bilder, die jedem Prozess übergeben werden")
        self.batch_label.grid(row=row, column=0, padx=(10, 0), pady=(10, 10), sticky="ew")
        self.batch = ttk.Spinbox(self, font=beck_view_font, from_=1, to=99, state=ttk.READONLY)
        self.batch.grid(row=row, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.batch.set(10)
        ToolTip(self.batch,
                text="Anzahl Bilder die in einem `Paket`parallel verarbeitet werden. Beeinflusst die "
                     "Verarbeitungs-geschwindigkeit.\nWertebereich 1 bis 99.",
                bootstyle="INFO, INVERSE")

        self.threads_label = ttk.Label(self, font=beck_view_font,
                                       text="Anzahl parallele Threads")
        self.threads_label.grid(row=row, column=2, padx=(10, 0), pady=(10, 10), sticky="ew")
        self.threads = ttk.Spinbox(self, font=beck_view_font, from_=1, to=20, state=ttk.READONLY)
        self.threads.grid(row=row, column=3, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.threads.set(8)
        ToolTip(self.threads,
                text="Anzahl paralleler Threads die jeweils ein `Paket` verarbeiten. Beeinflusst die Konvertierungsgeschwindigkeit. Wertebereich 1 bis 20.",
                bootstyle="INFO, INVERSE")

        self.panel = ttk.Frame(self, borderwidth=0)
        self.panel.grid(row=row, column=4, rowspan=2, padx=(10, 10), pady=(10, 10), sticky="ewns")


class Preferences(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)

        # increase font size for Listbox of Combobox
        list_font = ttk.font.Font(family="Helvetica", size=14)
        self.master.option_add("*TCombobox*Listbox*Font", list_font)

        # increase font size for TCheckbutton
        s = ttk.Style()
        s.configure('Beck-View_Movie-GUI.TCheckbutton', font=beck_view_font)

        self.configure(borderwidth=3, text="Einstellungen", relief=SOLID)

        self.logo = ttk.PhotoImage(file="beck-view-movie-logo.png")
        self.logo_label = ttk.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, rowspan=3, padx=(10, 10), pady=(0, 0), sticky="ew")

        self.flip_vertical = tkinter.BooleanVar()
        self.flip_vertical.set(True)

        self.flip_vertical_checkbutton = ttk.Checkbutton(self, text="An vertikaler Achse spiegeln",
                                                         onvalue=True, offvalue=False,
                                                         variable=self.flip_vertical,
                                                         padding="5  10",
                                                         style='Beck-View_Movie-GUI.TCheckbutton'
                                                         )
        self.flip_vertical_checkbutton.grid(row=0, column=1, padx=(5, 0), pady=(5, 5), sticky="w")
        ToolTip(self.flip_vertical_checkbutton,
                text="Alle Bilder des Films an der vertikalen Bildachse spiegeln.",
                bootstyle="INFO, INVERSE")

        self.flip_horizontal = tkinter.BooleanVar()
        self.flip_horizontal.set(False)

        self.flip_horizontal_checkbutton = ttk.Checkbutton(self, text="An horizontaler Achse spiegeln",
                                                           onvalue=True, offvalue=False,
                                                           variable=self.flip_horizontal,
                                                           padding="5  10",
                                                           style='Beck-View_Movie-GUI.TCheckbutton'
                                                           )
        self.flip_horizontal_checkbutton.grid(row=0, column=2, padx=(15, 0), pady=(5, 5), sticky="w")
        ToolTip(self.flip_horizontal_checkbutton,
                text="Alle Bilder des Films an der horizontalen Bildachse spiegeln.",
                bootstyle="INFO, INVERSE")

        # self.scale_up = tkinter.BooleanVar()
        # self.scale_up.set(False)
        #
        # self.scale_up_checkbutton = ttk.Checkbutton(self, text="Hochskalieren",
        #                                             onvalue=True, offvalue=False,
        #                                             variable=self.scale_up,
        #                                             padding="5  10",
        #                                             style='beck-view-gui.TCheckbutton'
        #                                             )
        # self.scale_up_checkbutton.grid(row=0, column=3, padx=(120, 0), pady=(5, 5), sticky="w")
        # ToolTip(self.scale_up_checkbutton,
        #         text="Mit ESPCN Modell hochskalieren auf 3840 x 2160 Pixel.",
        #         bootstyle="INFO, INVERSE")

        self.panel = ttk.Frame(self, borderwidth=0)
        self.panel.grid(row=1, column=1, rowspan=2, columnspan=4, padx=(0, 0), pady=(0, 0), sticky="ewns")

        self.film_wrapper_label = ttk.Label(self.panel,
                                            font=beck_view_font,
                                            text="Ausgabeformat (Wrapper)")
        self.film_wrapper_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="ew")
        self.film_wrapper_values = [
            "avi",
            "mov",
            "mp4",
            "mv4",
            "wmf",
        ]

        self.film_wrapper = ttk.Combobox(self.panel,
                                         font=beck_view_font,
                                         values=self.film_wrapper_values,
                                         state=ttk.READONLY)

        self.film_wrapper.grid(row=0, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
        self.film_wrapper.current(2)
        ToolTip(self.film_wrapper,
                text="Das Ausgabeformat ist eine Hülle um das interne Format des generierten Films.",
                bootstyle="INFO, INVERSE")

        self.film_codec_values = [
            "avc1",
            "h263",
            "h264",
            "mp4v"
        ]

        self.film_codec_label = ttk.Label(self.panel, font=beck_view_font, text="Codec")
        self.film_codec_label.grid(row=0, column=2, padx=(30, 10), pady=(5, 5), sticky="ew")
        self.film_codec = ttk.Combobox(self.panel,
                                       font=beck_view_font,
                                       values=self.film_codec_values,
                                       state=ttk.READONLY)
        self.film_codec.grid(row=0, column=3, padx=(0, 10), pady=(5, 5), sticky="ew")
        self.film_codec.current(0)
        ToolTip(self.film_codec,
                text="Codec legt die interne Kodierung fest. Damit werden Qualität und Größe der Ausgabedatei (Komprimierung) beeinflusst.",
                bootstyle="INFO, INVERSE")

        self.film_resolution_values = [
            "1600 x 1200",
            "1920 x 1080",
            "2048 x 1536",
            "2592 x 1944",
            "3840 x 2160",
        ]

        self.film_resolution_label = ttk.Label(self.panel, font=beck_view_font, text="Auflösung")
        self.film_resolution_label.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="ew")
        self.film_resolution = ttk.Combobox(self.panel,
                                            font=beck_view_font,
                                            values=self.film_resolution_values,
                                            state=ttk.READONLY)
        self.film_resolution.grid(row=1, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
        self.film_resolution.current(1)
        ToolTip(self.film_resolution,
                text="Auflösung in horizontaler und vertikaler Richtung.",
                bootstyle="INFO, INVERSE")

        self.fps_label = ttk.Label(self.panel, font=beck_view_font,
                                   text="FPS")
        self.fps_label.grid(row=1, column=2, padx=(30, 0), pady=(5, 5), sticky="ew")
        self.fps = ttk.Spinbox(self.panel, font=beck_view_font, from_=18, to=30, state=ttk.READONLY)
        self.fps.grid(row=1, column=3, padx=(0, 10), pady=(10, 10), sticky="ew")
        self.fps.set(24)
        ToolTip(self.fps,
                text="Bilder pro Sekunde (FPS).\nWertebereich 18 bis 30.",
                bootstyle="INFO, INVERSE")


class SubprocessOutput(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(borderwidth=3, text="Ausgabe `Beck-View-Movie`", relief=SOLID)

        # Create ScrolledText widget for displaying subprocess output
        self.text_output = ScrolledText(self, height=10, font=beck_view_font, wrap=WORD, autohide=True, takefocus=FALSE)
        self.text_output.grid(row=0, column=0, rowspan=10, padx=10, pady=10, sticky=NSEW)

        # Configure grid to make the text_output widget expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class MainMenu(ttk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.file_menu = ttk.Menu(self, tearoff=1)
        self.file_menu.add_command(label="Neues Projekt")
        self.file_menu.add_command(label="Letzte Projekte")
        self.file_menu.add_command(label="Projekt schließen")
        self.file_menu.add_command(label="Alle Projekte schließen")
        self.file_menu.add_command(label="Projekt umbenennen")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Beenden", command=master.destroy)
        self.add_cascade(label="Datei", menu=self.file_menu, underline=0)

        self.window_menu = tkinter.Menu(self, tearoff=0)
        self.window_menu.add_command(label="Normal", command=self.normal)
        self.window_menu.add_command(label="Vollbild", command=self.maximize)
        self.window_menu.add_command(label="Minimiert", command=self.minimize)
        self.add_cascade(label="Fenster", menu=self.window_menu, underline=0)

    def maximize(self):
        app.state("zoomed")

    def normal(self):
        app.state("normal")

    def minimize(self):
        app.state("iconic")


class GroupLayout(ttk.Frame):
    def __init__(self, master, windows: bool):
        super().__init__(master)

        self.windows = windows

        self.panel = ttk.Frame(self, borderwidth=0)
        self.panel.grid_columnconfigure(0, weight=0)
        self.panel.grid_columnconfigure(1, weight=1)
        self.panel.grid(row=0, column=0, rowspan=4, columnspan=6, padx=(0, 0), pady=(0, 0), sticky="ewns")

        # Create other GUI elements
        self.preferences = Preferences(self.panel)
        self.preferences.grid_columnconfigure(0, weight=0)
        self.preferences.grid_columnconfigure(1, weight=0)
        self.preferences.grid_columnconfigure(2, weight=0)
        self.preferences.grid_columnconfigure(3, weight=2)
        self.preferences.grid(row=0, column=0, columnspan=3, padx=(10, 10), pady=(10, 5), sticky=EW)

        self.input_directory = FrameInputDirectory(self.panel)
        self.input_directory.grid_columnconfigure(0, weight=0)
        self.input_directory.grid_columnconfigure(1, weight=1)
        self.input_directory.grid_columnconfigure(2, weight=0)
        self.input_directory.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(5, 5), sticky=EW)

        self.output_directory = FrameOutputDirectory(self.panel)
        self.output_directory.grid_columnconfigure(0, weight=0)
        self.output_directory.grid_columnconfigure(1, weight=1)
        self.output_directory.grid_columnconfigure(2, weight=0)
        self.output_directory.grid(row=2, column=0, columnspan=3, padx=(10, 10), pady=(5, 5), sticky=EW)

        self.technical_attributes = TechnicalAttributes(self.panel)
        self.technical_attributes.grid(row=3, column=0, columnspan=3, padx=(10, 10), pady=(5, 5), sticky=EW)

        self.subprocess_output = SubprocessOutput(self)
        self.subprocess_output.grid(row=4, column=0, columnspan=3, rowspan=1, padx=(10, 10), pady=(0, 5), sticky=NSEW)

        self.start_button = ttk.Button(self,
                                       text="Beck-View-Movie starten",
                                       style="Beck-View_Movie-GUI.TButton",
                                       command=self.start_digitization)
        self.start_button.grid(row=5, column=0, columnspan=1, padx=(10, 10), pady=(5, 10), sticky=EW)

        self.stop_button = ttk.Button(self,
                                      text="Beck-View-Movie stoppen",
                                      style="Beck-View_Movie-GUI.TButton",
                                      command=self.stop_digitization)
        self.stop_button.grid(row=5, column=1, columnspan=1, padx=(10, 10), pady=(5, 10), sticky=EW)

        # Configure grid weights
        self.grid_rowconfigure(4, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create asyncio event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Store reference to subprocess
        self.process = None
        self.output_task: Task

    async def read_subprocess_output(self, process: asyncio.subprocess.Process):
        # Asynchronously read subprocess output
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            self.subprocess_output.text_output.insert(tkinter.END, line.decode())
            self.subprocess_output.text_output.see(tkinter.END)

    def start_digitization(self):
        self.subprocess_output.text_output.insert(tkinter.END, "Beck-View_Movie - Starte Filmgenerierung...\n")

        async def run_digitization():
            filepath = Path.home().joinpath('PycharmProjects',
                                            'beck-view-movie',
                                            'assemble_film.cmd' if self.windows else 'beck-view-movie')

            self.fps = self.preferences.fps.get()
            self.date = f"{ttk.datetime.now():%Y_%m_%d}"
            self.filename = f"{self.output_directory.filename.get()}_{self.fps}fps_{self.date}"
            self.width, self.height = self.preferences.film_resolution.get().split(" x ", 2)

            self.threads = self.technical_attributes.threads.get()
            self.batch = self.technical_attributes.batch.get()
            if self.preferences.scale_up.get():
                self.threads = 1
                self.batch = 1

            command = [
                str(filepath),
                f"--input_path={self.input_directory.input_directory_path.get()}",
                f"--output_path={self.output_directory.output_directory_path.get()}",
                f"--name={self.filename}",
                f"--output_format={self.preferences.film_wrapper.get()}",
                f"--codec={self.preferences.film_codec.get()}",
                f"--width_height={self.width}x{self.height}",
                f"--frames_per_second={self.fps}",
                f"--number_of_workers={self.threads}",
                f"--batch_size={self.batch}"
            ]
            if self.preferences.flip_vertical.get():
                command.append("--flip_vertical")
            if self.preferences.flip_horizontal.get():
                command.append("--flip_horizontal")
            if self.preferences.scale_up.get():
                command.append("--scale_up")

            command.append("--gui")

            self.subprocess_output.text_output.insert(tkinter.END,
                                                      f"Beck-View_Movie - Beck-View-Movie wird mit folgenden Parametern gestartet: {command}\n")
            try:
                if self.windows:
                    self.process = await asyncio.create_subprocess_exec(
                        *command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        creationflags=subprocess.REALTIME_PRIORITY_CLASS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
                    )
                else:
                    self.process = await asyncio.create_subprocess_exec(
                        *command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        preexec_fn=os.setpgrp
                    )

                # Start reading subprocess output asynchronously
                self.output_task = self.loop.create_task(self.read_subprocess_output(self.process))

                # Wait for the process to finish
                await self.process.wait()
                await self.output_task

                self.subprocess_output.text_output.insert(tkinter.END,
                                                          f"Beck-View_Movie - Beck-View-Movie wurde mit Return-Code '{self.process.returncode}' beendet. \n")
                self.process = None

            except Exception as e:
                self.subprocess_output.text_output.insert(tkinter.END,
                                                          f"Beck-View_Movie - Error starting subprocess: {e}\n")
            finally:
                self.subprocess_output.text_output.see(tkinter.END)

        self.loop.create_task(run_digitization())

    def stop_digitization(self):
        if self.process:
            self.subprocess_output.text_output.insert(tkinter.END,
                                                      "Beck-View_Movie - Stoppe Beck-View-Digitize ...\n")
            try:
                if not self.output_task.cancelled():
                    self.subprocess_output.text_output.insert(tkinter.END,
                                                              "Beck-View_Movie - Beende Ausgabe von Nachrichten gesendet von Beck-View-Movie ...\n")
                    self.output_task.cancel()

                if self.windows:
                    self.process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    self.process.terminate()

                time.sleep(1)

                self.subprocess_output.text_output.insert(tkinter.END,
                                                          "Beck-View_Movie - Beck-View-Movie gestoppt!\n")
                self.process = None
            except Exception as e:
                self.subprocess_output.text_output.insert(tkinter.END,
                                                          f"Beck-View_Movie - Fehler beim Stoppen von Beck-View-Movie: {e}\n")
            finally:
                self.subprocess_output.text_output.see(tkinter.END)
        else:
            self.subprocess_output.text_output.insert(tkinter.END,
                                                      "Beck-View_Movie - Kein laufender Prozess 'Beck-View-Movie' gefunden!\n")
            self.subprocess_output.text_output.see(tkinter.END)


class Application(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")

        self.windows = platform.system() == "Windows"

        self.minsize(width=1080, height=800)
        self.geometry("1280x800")
        self.title("Beck View Movie GUI")
        self.option_add("*tearOff", False)

        self.iconbitmap("beck-view-movie-gui.ico")

        self.menu = MainMenu(self)
        self.config(menu=self.menu)

        self.layout = GroupLayout(self, self.windows)
        self.layout.pack(fill=BOTH, expand=YES)

        # Integrate asyncio event loop with Tkinter
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.loop = self.layout.loop
        self.update_loop()

    def update_loop(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.after(100, self.update_loop)

    def on_closing(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.close()
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
