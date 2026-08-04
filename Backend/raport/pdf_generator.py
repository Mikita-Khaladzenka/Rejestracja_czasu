from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    LongTable,
    SimpleDocTemplate,
    TableStyle,
)


class PDFGenerator:
    """
    Generuje raport PDF.

    Wszystkie dni miesiąca są umieszczane
    w jednym poziomym wierszu.
    """

    FONT_REGULAR = "DejaVuSans"
    FONT_BOLD = "DejaVuSans-Bold"

    BACKEND_DIRECTORY = Path(__file__).resolve().parent.parent

    FONT_DIRECTORY = (
        BACKEND_DIRECTORY
        / "assets"
        / "fonts"
    )

    FONT_FILES = {
        FONT_REGULAR:
            FONT_DIRECTORY / "DejaVuSans.ttf",

        FONT_BOLD:
            FONT_DIRECTORY / "DejaVuSans-Bold.ttf",
    }

    @classmethod
    def generate(
        cls,
        report_table: dict,
    ) -> BytesIO:

        cls._register_fonts()

        buffer = BytesIO()

        columns_count = len(
            report_table["table"][0]
        )

        page_width = cls._calculate_page_width(
            columns_count
        )

        page_height = A4[1]

        document = SimpleDocTemplate(
            buffer,
            pagesize=(
                page_width,
                page_height,
            ),
            leftMargin=15,
            rightMargin=15,
            topMargin=20,
            bottomMargin=20,
        )

        column_widths = cls._calculate_column_widths(
            report_table["table"]
        )

        table = LongTable(
            report_table["table"],
            colWidths=column_widths,
            repeatRows=2,
        )

        style = cls._create_style()

        cls._add_merged_cells(
            style,
            report_table["merged"],
        )

        cls._add_error_cells(
            style,
            report_table["red_cells"],
        )

        table.setStyle(
            TableStyle(style)
        )

        document.build(
            [table]
        )

        buffer.seek(0)

        return buffer

    @staticmethod
    def _calculate_page_width(
        columns_count: int,
    ) -> float:
        """
        Oblicza szerokość strony zależnie od liczby kolumn.

        Pierwsze dwie kolumny to imię i nazwisko,
        ostatnia kolumna to suma.
        Pozostałe kolumny zawierają godziny R i K.
        """

        name_width = 70
        surname_width = 90
        total_width = 55
        time_column_width = 30

        time_columns_count = max(
            columns_count - 3,
            0,
        )

        table_width = (
            name_width
            + surname_width
            + total_width
            + time_columns_count
            * time_column_width
        )

        margins = 30

        return table_width + margins

    @staticmethod
    def _calculate_column_widths(
        table_data: list,
    ) -> list[float]:

        columns_count = len(
            table_data[0]
        )

        if columns_count < 3:
            return []

        time_columns_count = (
            columns_count - 3
        )

        return (
            [
                70,
                90,
            ]
            + [
                30
            ] * time_columns_count
            + [
                55
            ]
        )

    @classmethod
    def _register_fonts(cls) -> None:

        cls._register_font(
            cls.FONT_REGULAR,
            cls.FONT_FILES[
                cls.FONT_REGULAR
            ],
        )

        cls._register_font(
            cls.FONT_BOLD,
            cls.FONT_FILES[
                cls.FONT_BOLD
            ],
        )

    @staticmethod
    def _register_font(
        font_name: str,
        font_path: Path,
    ) -> None:

        if (
            font_name
            in pdfmetrics.getRegisteredFontNames()
        ):
            return

        if not font_path.exists():

            raise FileNotFoundError(
                f"Nie znaleziono czcionki: "
                f"{font_path}"
            )

        pdfmetrics.registerFont(
            TTFont(
                font_name,
                str(font_path),
            )
        )

    @classmethod
    def _create_style(cls) -> list:

        return [
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black,
            ),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 1),
                colors.HexColor(
                    "#0078D7"
                ),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 1),
                colors.white,
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 1),
                cls.FONT_BOLD,
            ),
            (
                "FONTNAME",
                (0, 2),
                (-1, -1),
                cls.FONT_REGULAR,
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, 1),
                6,
            ),
            (
                "FONTSIZE",
                (0, 2),
                (-1, -1),
                6,
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER",
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                1,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                1,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
        ]

    @staticmethod
    def _add_merged_cells(
        style: list,
        merged: list,
    ) -> None:

        for (
            start_col,
            start_row,
            end_col,
            end_row,
        ) in merged:

            style.append(
                (
                    "SPAN",
                    (
                        start_col - 1,
                        start_row - 1,
                    ),
                    (
                        end_col - 1,
                        end_row - 1,
                    ),
                )
            )

    @staticmethod
    def _add_error_cells(
        style: list,
        red_cells: list,
    ) -> None:

        for row, column in red_cells:

            style.append(
                (
                    "BACKGROUND",
                    (
                        column - 1,
                        row - 1,
                    ),
                    (
                        column - 1,
                        row - 1,
                    ),
                    colors.red,
                )
            )