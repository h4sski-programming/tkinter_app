import tkinter as tk
import math
from tkinter import ttk

from settings import Settings
from pipes_db import pipe_dimensions, flange_dimensions

# Create settings instance
settings = Settings()

class SimpleApp:
    def __init__(self, master):
        self.master = master
        master.title("Piping Space Calculator")

        self.label = tk.Label(master, text="Piping Space Calculator")
        self.label.pack()

        self.content_frame = tk.Frame(master)
        self.content_frame.pack()


        # Create input frame
        self.input_frame = tk.Frame(self.content_frame)
        self.input_frame.pack()

        self.pipe_dimensions_list = list(pipe_dimensions.keys())

        # DN_1
        self.dn_1_label = tk.Label(self.input_frame, text='DN_1')
        self.dn_1_label.pack()
        self.dn_1_selected_value = tk.IntVar()
        self.dn_1_combobox = ttk.Combobox(self.input_frame, textvariable=self.dn_1_selected_value,
                                          values=self.pipe_dimensions_list)
        self.dn_1_combobox.pack()

        # DN_2
        self.dn_2_label = tk.Label(self.input_frame, text='DN_2')
        self.dn_2_label.pack()
        self.dn_2_selected_value = tk.IntVar()
        self.dn_2_combobox = ttk.Combobox(self.input_frame, textvariable=self.dn_2_selected_value,
                                          values=self.pipe_dimensions_list)
        self.dn_2_combobox.pack()

        # Min gap between pipes
        self.min_gap_label = tk.Label(self.input_frame, text="Enter minimum gap value [mm]:")
        self.min_gap_label.pack()

        # Minimum and maximum values for min_gap
        self.min_gap_min_value = 0
        self.min_gap_max_value = 200
        self.min_gap_step = 10
        self.min_gap_values_list = list(range(self.min_gap_min_value, self.min_gap_max_value + self.min_gap_step, self.min_gap_step))
        self.min_gap_value = tk.IntVar()
        self.min_gap_entry = ttk.Combobox(self.input_frame, textvariable=self.min_gap_value,
                                          values=self.min_gap_values_list)
        self.min_gap_entry.pack()
        # self.min_gap_entry = tk.Entry(self.input_frame, validate='key', validatecommand=(self.validate_min_gap, '%P'))
        # self.min_gap_entry.pack()

        # Calculate button
        self.calculate_button = tk.Button(self.input_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        # Label to display the calculated value
        self.calculated_label = tk.Label(self.input_frame, text="Calculated Value: ")
        self.calculated_label.pack()
        self.support_label = tk.Label(self.input_frame, text="")
        self.support_label.pack()


        # Create a Treeview widget
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = list(str(f'DN{dn}') for dn in self.pipe_dimensions_list)
        # self.tree["columns"] = ("Column 1", "Column 2", "Column 3")

        # Define column headings
        # self.tree.heading("#0", text="Index")
        for dn in self.pipe_dimensions_list:
            self.tree.heading(f'DN{dn}', text=f'DN{dn}')

        # Insert sample data
        for dn in self.pipe_dimensions_list:
            self.tree.insert('', dn, values = list(pipe_dimensions[d]['OD'] + int(dn) for d in pipe_dimensions.keys()))

        # Pack the Treeview widget
        self.tree.pack()
        

        # Adding quit button into the content_frame
        self.quit_button = tk.Button(self.content_frame, text="Quit", command=master.quit)
        self.quit_button.pack()

    def calculate(self):
        # Get values from DN_1, DN_2, and min_gap_entry
        dn_1_value = self.dn_1_selected_value.get()
        dn_2_value = self.dn_2_selected_value.get()
        min_gap_value = int(self.min_gap_entry.get())

        # Perform calculation (sum of DN_1, DN_2, and min_gap)
        flange_dn_1_od = flange_dimensions['PN16'][str(dn_1_value)]['OD']
        pipe_dn_2_od = pipe_dimensions[str(dn_2_value)]['OD']
        sum_value = int(math.ceil((flange_dn_1_od/2 + pipe_dn_2_od/2 + min_gap_value) / 10)) * 10
        # od_value = flange_dimensions['PN16'][str(dn_1_value)]['OD']
        # print(f'{od_value}')
        calculated_value = f"Calculated Value: DN{dn_1_value} + DN{dn_2_value} + {min_gap_value} = {sum_value}"

        # Update the calculated label
        self.calculated_label.config(text=calculated_value)
        # self.support_label.config(text=f'{flange_dn_1_od = }  {pipe_dn_2_od = }')


    def validate_min_gap(self, value):
        try:
            if value:
                int_value = int(value)
                return self.min_gap_min_value <= int_value <= self.min_gap_max_value
            return True
        except ValueError:
            return False



# Create the main window
root = tk.Tk()
root.geometry(f'{settings.width}x{settings.heigth}')

# Instantiate the SimpleApp class
app = SimpleApp(root)

# Run the Tkinter event loop
root.mainloop()
