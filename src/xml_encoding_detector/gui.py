"""
XML Encoding Detector GUI
"""

from tkinter import (
    filedialog,
    messagebox,
)
from pathlib import Path
from xml_encoding_detector.detector import (
    detect_encoding,
    validate_xml,
)

from xml_encoding_detector.report import (
    write_html_report,
    write_csv_report,
    write_markdown_report,
)
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
        self.results = []

        self.encodings = {}

        self.valid_count = 0

        self.invalid_count = 0
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

        button_frame = ttk.Frame(
            frame
        )

        button_frame.pack(
            fill="x",
            pady=15,
        )

        ttk.Button(
            button_frame,
            text="Scan",
            command=self.scan,
        ).pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Button(
            button_frame,
            text="Export",
            command=self.export_report,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0),
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
        self.table.column(
            "file",
            width=350,
        )

        self.table.column(
            "valid",
            width=100,
            anchor="center",
        )

        self.table.column(
            "encoding",
            width=120,
            anchor="center",
        )

        self.table.column(
            "error",
            width=400,
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
        folder = self.folder_var.get()

        if not folder:
            self.status.config(
                text="Please select a folder."
            )
            return

        self.status.config(
            text="Scanning..."
        )
        self.table.delete(
            *self.table.get_children()
        )
        files_scanned = 0
        valid_xml = 0
        invalid_xml = 0
        encodings = {}
        results = []
        pattern = (
            "**/*.xml"
            if self.recursive_var.get()
            else "*.xml"
        )

        for xml_file in Path(folder).glob(
            pattern
        ):
            files_scanned += 1

            data = xml_file.read_bytes()

            validation = validate_xml(
                data
            )
            if validation.valid:
                valid_xml += 1
            else:
                invalid_xml += 1

            encoding = (
                validation.encoding
                or "unknown"
            )
            encodings[
                encoding
            ] = (
                encodings.get(
                    encoding,
                    0,
                )
                + 1
            )
            results.append(
                {
                    "file": xml_file.name,
                    "valid": validation.valid,
                    "encoding": encoding,
                    "error": validation.error,
                }
            )


            self.table.insert(
                "",
                "end",
                values=(
                    xml_file.name,
                    validation.valid,
                    encoding,
                    validation.error or "",
                ),
            )
                
            self.valid_label.config(
                text=f"Valid XML: {valid_xml}"
            )

            self.invalid_label.config(
                text=f"Invalid XML: {invalid_xml}"
            )
            top_encoding = (
                max(
                    encodings,
                    key=encodings.get,
                )
                if encodings
                else "N/A"
            )

            self.encoding_label.config(
                text=f"Top Encoding: {top_encoding}"
            )
        self.files_label.config(
            text=f"Files Scanned: {files_scanned}"
        )
        self.results = results

        self.encodings = encodings

        self.valid_count = valid_xml

        self.invalid_count = invalid_xml
        self.status.config(
            text="Scan complete"
        )
    def export_report(
        self,
    ) -> None:
        output_format = (
            self.output_format.get()
        )

        extension = {
            "html": ".html",
            "csv": ".csv",
            "json": ".json",
            "markdown": ".md",
        }[output_format]

        output_file = (
            filedialog.asksaveasfilename(
                defaultextension=extension,
                filetypes=[
                    (
                        f"{output_format.upper()} files",
                        f"*{extension}",
                    ),
                ],
            )
        )

        if not output_file:
            return

        if output_format == "html":
            write_html_report(
                output_file,
                self.results,
                self.encodings,
                self.valid_count,
                self.invalid_count,
            )
        elif output_format == "csv":
            print(
                "CSV RESULTS:",
                self.results,
            )
            write_csv_report(
                output_file,
                self.results,
            )
        elif output_format == "json":
            import json

            with open(
                output_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    self.results,
                    file,
                    indent=2,
                    ensure_ascii=False,
                 )
        elif output_format == "markdown":
             write_markdown_report(
                output_file,
                self.results,
                self.valid_count,
                self.invalid_count,
            )


        messagebox.showinfo(
            "Export",
            (
                f"Export {output_format.upper()} "
                f"to:\n{output_file}"
            ),
        )

        self.status.config(
            text=(
                f"Exported "
                f"{output_format.upper()}"
            )
        )

def main() -> None:
    root = tk.Tk()

    XMLDetectorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()