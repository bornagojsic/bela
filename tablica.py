"""
Scoreboard module for the Bela card game.

This module contains the Scoreboard class for displaying game scores in a table format.
"""

from tkinter import *


class Scoreboard:
    """Manages and displays the score table for the Bela card game."""

    def __init__(self, window, data_list):
        """
        Initializes the scoreboard.

        Args:
            window: Parent tkinter window
            data_list: Initial data to display in the scoreboard
        """
        self.window = window
        self.data_list = data_list
        self.row_count = 0
        self.table_cells = []
        self.total_cell = None
        self.column_totals = []
        self.add_data(data_list)

    def add_data(self, data_list):
        """
        Adds data to the scoreboard.

        Args:
            data_list: List of data rows to add to the scoreboard
        """
        if self.total_cell:
            self.total_cell.destroy()

        initial_row = self.row_count
        self.row_count += len(data_list)

        # Create cells for the new data
        new_table = [
            [self.add_cell(self.window, data_list, i, j, initial_row)
             for j in range(len(data_list[0]))]
            for i in range(len(data_list))
        ]
        self.table_cells += new_table

        # Add the total row
        self.total_cell = self.add_cell(self.window, [["Total:"]], 0, 0, self.row_count)
        self.total_cell.config(width=20, borderwidth=4)
        self.total_cell.grid(row=self.row_count, column=0, columnspan=len(self.table_cells[0]))

        # Calculate and add column totals
        self.column_totals = [
            self.add_cell(
                self.window,
                [[self.calculate_column_total(i) for i in range(len(self.table_cells[0]))]],
                0, j, self.row_count + 1
            )
            for j in range(len(self.table_cells[0]))
        ]

    def add_cell(self, window, data_list, row_idx, col_idx, initial_row):
        """
        Creates and adds a single cell to the scoreboard.

        Args:
            window: Parent tkinter window
            data_list: List of data containing the cell value
            row_idx: Row index of the cell
            col_idx: Column index of the cell
            initial_row: Starting row offset

        Returns:
            tkinter.Label: The created cell widget
        """
        cell = Label(
            window,
            width=10,
            text=data_list[row_idx][col_idx],
            fg='#20bebe',
            font=("Cascadia Code", 18),
            justify='center',
            borderwidth=2,
            relief="groove"
        )
        cell.grid(row=(row_idx + initial_row), column=col_idx)
        return cell

    def update_cell_value(self, row_idx, col_idx, new_value):
        """
        Updates the value of a specific cell.

        Args:
            row_idx: Row index of the cell to update
            col_idx: Column index of the cell to update
            new_value: New value to set in the cell
        """
        self.table_cells[row_idx][col_idx].config(text=new_value)

    def update_last_row(self, data_list):
        """
        Updates the values in the last row of the scoreboard.

        Args:
            data_list: List of new values for the last row
        """
        for j in range(len(self.table_cells[-1])):
            self.table_cells[-1][j].config(text=data_list[j])

        # Recalculate column totals
        self.column_totals = [
            self.add_cell(
                self.window,
                [[self.calculate_column_total(i) for i in range(len(self.table_cells[0]))]],
                0, j, self.row_count + 1
            )
            for j in range(len(self.table_cells[0]))
        ]

    def get_cell_value(self, row_idx, col_idx):
        """
        Gets the value of a specific cell.

        Args:
            row_idx: Row index of the cell
            col_idx: Column index of the cell

        Returns:
            str: The text value of the specified cell
        """
        return self.table_cells[row_idx][col_idx]["text"]

    def calculate_column_total(self, col_idx):
        """
        Calculates the total value for a specific column.

        Args:
            col_idx: Index of the column to sum

        Returns:
            int: Sum of all numeric values in the column (excluding header)
        """
        total = 0
        for row_idx in range(1, self.row_count):  # Skip header row
            cell_text = self.table_cells[row_idx][col_idx]["text"]
            if cell_text != "–":  # Skip dash symbols
                try:
                    total += int(cell_text)
                except ValueError:
                    # If conversion fails, treat as 0
                    continue
        return total