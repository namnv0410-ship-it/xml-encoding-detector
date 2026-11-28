"""
XML Encoding Detector GUI
"""

from tkinter import filedialog
import tkinter as tk
from tkinter import ttk


class XMLDetectorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.root.title(
            "XML Encoding Detector"
        )

        self.root.geometry(
            "1100x750"
        )

        self.root.minsize(
            1000,
            700,
        )

        self.folder_var = tk.StringVar()

        self.output_format = tk.StringVar(
            value="html"
        )

        self.recursive_var = tk.BooleanVar(
            value=True
        )

        self._build_ui()

    def _build_ui(self) -> None:
        """
        Build the user interface.
        """

        main = ttk.Frame(
            self.root,
            padding=10,
        )

        main.pack(
            fill="both",
            expand=True,
        )

        title = ttk.Label(
            main,
            text="XML Encoding Detector",
            font=(
                "Segoe UI",
                18,
                "bold",
            ),
        )

        title.pack(
            anchor="w",
            pady=(0, 10),
        )

        top = ttk.Frame(main)

        top.pack(
            fill="x",
        )

        self._build_config_panel(
            top
        )

        self._build_stats_panel(
            top
        )

        self._build_results_table(
            main
        )

        self._build_status_bar(
            main
        )

    def _build_config_panel(
        self,
        parent: ttk.Frame,
    ) -> None:
        frame = ttk.LabelFrame(
            parent,
            text="Configuration",
            padding=10,
        )

        frame.pack(
            side="left",
            fill="y",
            padx=(0, 10),
        )

        ttk.Label(
            frame,
            text="Folder",
        ).pack(anchor="w")

        folder_row = ttk.Frame(frame)

        folder_row.pack(
            fill="x",
            pady=5,
        )

        ttk.Entry(
            folder_row,
            textvariable=self.folder_var,
            width=40,
        ).pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Button(
            folder_row,
            text="Browse",
            command=self.choose_folder,
        ).pack(
            side="left",
            padx=(5, 0),
        )

        ttk.Checkbutton(
            frame,
            text="Recursive Scan",
            variable=self.recursive_var,
        ).pack(
            anchor="w",
            pady=10,
        )

        ttk.Label(
            frame,
            text="Output Format",
        ).pack(
            anchor="w",
            pady=(10, 5),
        )

        for value, text in (
            ("html", "HTML"),
            ("csv", "CSV"),
            ("json", "JSON"),
            ("markdown", "Markdown"),
        ):
            ttk.Radiobutton(
                frame,
                text=text,
                value=value,
                variable=self.output_format,
            ).pack(
                anchor="w",
            )

        ttk.Button(
            frame,
            text="Scan",
            command=self.scan,
        ).pack(
            fill="x",
            pady=15,
        )

    def _build_stats_panel(
        self,
        parent: ttk.Frame,
    ) -> None:
        frame = ttk.LabelFrame(
            parent,
            text="Statistics",
            padding=10,
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.files_label = ttk.Label(
            frame,
            text="Files Scanned: 0",
        )

        self.files_label.pack(
            anchor="w",
            pady=5,
        )

        self.valid_label = ttk.Label(
            frame,
            text="Valid XML: 0",
        )

        self.valid_label.pack(
            anchor="w",
            pady=5,
        )

        self.invalid_label = ttk.Label(
            frame,
            text="Invalid XML: 0",
        )

        self.invalid_label.pack(
            anchor="w",
            pady=5,
        )

        self.encoding_label = ttk.Label(
            frame,
            text="Top Encoding: N/A",
        )

        self.encoding_label.pack(
            anchor="w",
            pady=5,
        )

    def _build_results_table(
        self,
        parent: ttk.Frame,
    ) -> None:
        table_frame = ttk.LabelFrame(
            parent,
            text="Results",
            padding=5,
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10,
        )

        columns = (
            "file",
            "valid",
            "encoding",
            "error",
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )

        for column in columns:
            self.table.heading(
                column,
                text=column.title(),
            )

        self.table.pack(
            fill="both",
            expand=True,
        )

    def _build_status_bar(
        self,
        parent: ttk.Frame,
    ) -> None:
        self.status = ttk.Label(
            parent,
            text="Ready",
        )

        self.status.pack(
            fill="x",
            side="bottom",
        )

    def choose_folder(
        self,
    ) -> None:
        folder = filedialog.askdirectory()

        if folder:
            self.folder_var.set(
                folder
            )

    def scan(
        self,
    ) -> None:
        self.status.config(
            text="Scanning..."
        )

        # TODO:
        # connect detector logic

        self.status.config(
            text="Scan complete"
        )


def main() -> None:
    root = tk.Tk()

    XMLDetectorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()