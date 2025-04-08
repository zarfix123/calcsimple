import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from functools import partial
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beautiful Calculator")
        self.root.geometry("360x580")  # Made slightly taller for theme controls
        self.root.resizable(False, False)
        
        # Theme variables
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f5f5f5",
                "display_bg": "#f5f5f5",
                "display_fg": "#212121",
                "history_fg": "#9e9e9e",
                "number_bg": "#ffffff",
                "number_fg": "#212121",
                "operation_bg": "#e0e0e0",
                "operation_fg": "#212121",
                "equal_bg": "#2196f3",
                "equal_fg": "#ffffff",
                "clear_bg": "#f44336",
                "clear_fg": "#ffffff",
                "function_bg": "#9575cd",
                "function_fg": "#ffffff",
            },
            "dark": {
                "bg": "#263238",
                "display_bg": "#37474F",
                "display_fg": "#ECEFF1",
                "history_fg": "#B0BEC5",
                "number_bg": "#455A64",
                "number_fg": "#ECEFF1",
                "operation_bg": "#546E7A",
                "operation_fg": "#ECEFF1",
                "equal_bg": "#039BE5",
                "equal_fg": "#FFFFFF",
                "clear_bg": "#E53935",
                "clear_fg": "#FFFFFF",
                "function_bg": "#7E57C2",
                "function_fg": "#FFFFFF",
            },
            "pastel": {
                "bg": "#E8F5E9",
                "display_bg": "#C8E6C9",
                "display_fg": "#2E7D32",
                "history_fg": "#81C784",
                "number_bg": "#F1F8E9",
                "number_fg": "#33691E",
                "operation_bg": "#DCEDC8",
                "operation_fg": "#33691E",
                "equal_bg": "#9CCC65",
                "equal_fg": "#FFFFFF",
                "clear_bg": "#EF9A9A",
                "clear_fg": "#FFFFFF",
                "function_bg": "#AED581",
                "function_fg": "#33691E",
            }
        }
        
        # Variables
        self.current_expression = ""
        self.total_expression = ""
        self.memory_value = 0
        self.history = []
        
        # Main frames - calculator and graph
        self.frames = {}
        self.current_frame = "calculator"
        
        self.frames["calculator"] = tk.Frame(self.root)
        self.frames["calculator"].pack(fill="both", expand=True)
        
        self.frames["graph"] = tk.Frame(self.root)
        # Not packing the graph frame until needed
        
        # Apply initial theme
        self.apply_theme(self.current_theme)
        
        # Create the UI components for calculator
        self.create_display()
        self.create_buttons()
        self.create_theme_controls()
        
        # Create graphing UI
        self.create_graph_ui()
        
        # Configure the grid layout
        self.frames["calculator"].grid_rowconfigure(1, weight=1)
        for i in range(5):
            self.frames["calculator"].grid_columnconfigure(i, weight=1)
    
    def apply_theme(self, theme_name):
        """Apply the selected theme to the calculator"""
        theme = self.themes[theme_name]
        self.current_theme = theme_name
        
        self.root.configure(bg=theme["bg"])
        
        # Apply to frames if they exist
        if hasattr(self, 'frames'):
            for frame in self.frames.values():
                frame.configure(bg=theme["bg"])
                
        # Apply to other elements if they exist
        if hasattr(self, 'expression_display'):
            self.expression_display.configure(
                bg=theme["display_bg"], 
                fg=theme["display_fg"]
            )
            
        if hasattr(self, 'history_display'):
            self.history_display.configure(
                bg=theme["display_bg"], 
                fg=theme["history_fg"]
            )
            
        if hasattr(self, 'display_frame'):
            self.display_frame.configure(bg=theme["display_bg"])
            
        # Update button styles
        if hasattr(self, 'style'):
            self.style.configure("Number.TButton", background=theme["number_bg"], foreground=theme["number_fg"])
            self.style.configure("Operation.TButton", background=theme["operation_bg"], foreground=theme["operation_fg"])
            self.style.configure("Equal.TButton", background=theme["equal_bg"], foreground=theme["equal_fg"])
            self.style.configure("Clear.TButton", background=theme["clear_bg"], foreground=theme["clear_fg"])
            self.style.configure("Function.TButton", background=theme["function_bg"], foreground=theme["function_fg"])
            self.style.map("Number.TButton", background=[("active", self.lighten_color(theme["number_bg"]))])
            self.style.map("Operation.TButton", background=[("active", self.lighten_color(theme["operation_bg"]))])
            self.style.map("Equal.TButton", background=[("active", self.lighten_color(theme["equal_bg"]))])
            self.style.map("Clear.TButton", background=[("active", self.lighten_color(theme["clear_bg"]))])
            self.style.map("Function.TButton", background=[("active", self.lighten_color(theme["function_bg"]))])
    
    def lighten_color(self, hex_color, amount=0.15):
        """Lighten a hex color by the given amount"""
        # Convert to RGB
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        rgb = [min(int(c * (1 + amount)), 255) for c in rgb]
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def create_display(self):
        # Main display frame
        self.display_frame = tk.Frame(self.frames["calculator"], bg=self.themes[self.current_theme]["display_bg"])
        self.display_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=(20, 10))
        
        # History display
        self.history_display = tk.Label(
            self.display_frame, 
            text="", 
            anchor="e", 
            bg=self.themes[self.current_theme]["display_bg"], 
            fg=self.themes[self.current_theme]["history_fg"], 
            font=("Arial", 12)
        )
        self.history_display.pack(fill="both", expand=True)
        
        # Expression display
        self.expression_display = tk.Label(
            self.display_frame, 
            text="0", 
            anchor="e", 
            bg=self.themes[self.current_theme]["display_bg"], 
            fg=self.themes[self.current_theme]["display_fg"], 
            font=("Arial", 30, "bold")
        )
        self.expression_display.pack(fill="both", expand=True)
    
    def create_buttons(self):
        buttons_frame = tk.Frame(self.frames["calculator"], bg=self.themes[self.current_theme]["bg"])
        buttons_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        
        # Button styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 14), borderwidth=0)
        
        # Apply theme to buttons
        self.style.configure("Number.TButton", 
                          background=self.themes[self.current_theme]["number_bg"], 
                          foreground=self.themes[self.current_theme]["number_fg"])
        self.style.configure("Operation.TButton", 
                          background=self.themes[self.current_theme]["operation_bg"], 
                          foreground=self.themes[self.current_theme]["operation_fg"])
        self.style.configure("Equal.TButton", 
                          background=self.themes[self.current_theme]["equal_bg"], 
                          foreground=self.themes[self.current_theme]["equal_fg"])
        self.style.configure("Clear.TButton", 
                          background=self.themes[self.current_theme]["clear_bg"], 
                          foreground=self.themes[self.current_theme]["clear_fg"])
        self.style.configure("Function.TButton", 
                          background=self.themes[self.current_theme]["function_bg"], 
                          foreground=self.themes[self.current_theme]["function_fg"])
        
        # Button hover effects
        self.style.map("Number.TButton", 
                    background=[("active", self.lighten_color(self.themes[self.current_theme]["number_bg"]))])
        self.style.map("Operation.TButton", 
                    background=[("active", self.lighten_color(self.themes[self.current_theme]["operation_bg"]))])
        self.style.map("Equal.TButton", 
                    background=[("active", self.lighten_color(self.themes[self.current_theme]["equal_bg"]))])
        self.style.map("Clear.TButton", 
                    background=[("active", self.lighten_color(self.themes[self.current_theme]["clear_bg"]))])
        self.style.map("Function.TButton", 
                    background=[("active", self.lighten_color(self.themes[self.current_theme]["function_bg"]))])
        
        # Define buttons with their properties
        # (text, row, column, columnspan, style, command)
        buttons = [
            ("MC", 0, 0, 1, "Function.TButton", lambda: self.memory_clear()),
            ("MR", 0, 1, 1, "Function.TButton", lambda: self.memory_recall()),
            ("M+", 0, 2, 1, "Function.TButton", lambda: self.memory_add()),
            ("M-", 0, 3, 1, "Function.TButton", lambda: self.memory_subtract()),
            ("C", 0, 4, 1, "Clear.TButton", lambda: self.clear_display()),
            
            ("x²", 1, 0, 1, "Function.TButton", lambda: self.add_to_expression("**2")),
            ("x³", 1, 1, 1, "Function.TButton", lambda: self.add_to_expression("**3")),
            ("x^y", 1, 2, 1, "Function.TButton", lambda: self.add_to_expression("**")),
            ("√", 1, 3, 1, "Function.TButton", lambda: self.add_operation("sqrt(")),
            ("⌫", 1, 4, 1, "Clear.TButton", lambda: self.backspace()),
            
            ("n!", 2, 0, 1, "Function.TButton", lambda: self.add_operation("factorial(")),
            ("(", 2, 1, 1, "Operation.TButton", lambda: self.add_to_expression("(")),
            (")", 2, 2, 1, "Operation.TButton", lambda: self.add_to_expression(")")),
            ("%", 2, 3, 1, "Operation.TButton", lambda: self.add_to_expression("%")),
            ("÷", 2, 4, 1, "Operation.TButton", lambda: self.add_to_expression("/")),
            
            ("7", 3, 0, 1, "Number.TButton", lambda: self.add_to_expression("7")),
            ("8", 3, 1, 1, "Number.TButton", lambda: self.add_to_expression("8")),
            ("9", 3, 2, 1, "Number.TButton", lambda: self.add_to_expression("9")),
            ("×", 3, 3, 1, "Operation.TButton", lambda: self.add_to_expression("*")),
            ("ⁿ√x", 3, 4, 1, "Function.TButton", lambda: self.add_operation("nthroot(")),
            
            ("4", 4, 0, 1, "Number.TButton", lambda: self.add_to_expression("4")),
            ("5", 4, 1, 1, "Number.TButton", lambda: self.add_to_expression("5")),
            ("6", 4, 2, 1, "Number.TButton", lambda: self.add_to_expression("6")),
            ("-", 4, 3, 1, "Operation.TButton", lambda: self.add_to_expression("-")),
            ("log", 4, 4, 1, "Function.TButton", lambda: self.add_operation("log10(")),
            
            ("1", 5, 0, 1, "Number.TButton", lambda: self.add_to_expression("1")),
            ("2", 5, 1, 1, "Number.TButton", lambda: self.add_to_expression("2")),
            ("3", 5, 2, 1, "Number.TButton", lambda: self.add_to_expression("3")),
            ("+", 5, 3, 1, "Operation.TButton", lambda: self.add_to_expression("+")),
            ("ln", 5, 4, 1, "Function.TButton", lambda: self.add_operation("log(")),
            
            ("0", 6, 0, 2, "Number.TButton", lambda: self.add_to_expression("0")),
            (".", 6, 2, 1, "Number.TButton", lambda: self.add_to_expression(".")),
            ("=", 6, 3, 1, "Equal.TButton", lambda: self.evaluate()),
            ("📊", 6, 4, 1, "Function.TButton", lambda: self.switch_to_graph_mode())
        ]
        
        # Store button widgets to be able to create animations
        self.button_widgets = {}
        
        for (text, row, column, columnspan, style_name, command) in buttons:
            button = ttk.Button(
                buttons_frame, 
                text=text, 
                style=style_name, 
                command=command
            )
            
            # Create animation effect
            button.bind("<ButtonPress-1>", lambda event, b=button: self.button_press_animation(b))
            button.bind("<ButtonRelease-1>", lambda event, b=button: self.button_release_animation(b))
            
            button.grid(
                row=row, 
                column=column, 
                columnspan=columnspan, 
                sticky="nsew", 
                padx=3, 
                pady=3
            )
            
            # Store widget
            self.button_widgets[text] = button
        
        # Configure grid
        for i in range(7):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)

    def create_theme_controls(self):
        """Create theme controls at the bottom of the calculator"""
        theme_frame = tk.Frame(self.frames["calculator"], bg=self.themes[self.current_theme]["bg"])
        theme_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=10, pady=5)
        
        # Theme label
        theme_label = tk.Label(
            theme_frame, 
            text="Theme:", 
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 10)
        )
        theme_label.pack(side="left", padx=5)
        
        # Create a button for each theme
        for theme_name in self.themes:
            theme_button = ttk.Button(
                theme_frame,
                text=theme_name.capitalize(),
                command=lambda tn=theme_name: self.apply_theme(tn),
                style="Function.TButton"
            )
            theme_button.pack(side="left", padx=5)
    
    def create_graph_ui(self):
        """Create the UI for the graphing functionality"""
        # Main frame for graphing
        graph_frame = self.frames["graph"]
        graph_frame.configure(bg=self.themes[self.current_theme]["bg"])
        
        # Controls frame
        controls_frame = tk.Frame(graph_frame, bg=self.themes[self.current_theme]["bg"])
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Function entry
        function_label = tk.Label(
            controls_frame, 
            text="f(x) =", 
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 12)
        )
        function_label.pack(side="left", padx=5)
        
        self.function_entry = tk.Entry(
            controls_frame,
            font=("Arial", 12),
            bg=self.themes[self.current_theme]["number_bg"],
            fg=self.themes[self.current_theme]["number_fg"],
            insertbackground=self.themes[self.current_theme]["number_fg"]
        )
        self.function_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.function_entry.insert(0, "sin(x)")  # Default function
        
        # Range controls
        range_frame = tk.Frame(graph_frame, bg=self.themes[self.current_theme]["bg"])
        range_frame.pack(fill="x", padx=10, pady=5)
        
        # X range
        x_min_label = tk.Label(
            range_frame, 
            text="X Min:", 
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 10)
        )
        x_min_label.pack(side="left", padx=5)
        
        self.x_min_entry = tk.Entry(
            range_frame,
            font=("Arial", 10),
            width=5,
            bg=self.themes[self.current_theme]["number_bg"],
            fg=self.themes[self.current_theme]["number_fg"]
        )
        self.x_min_entry.pack(side="left", padx=5)
        self.x_min_entry.insert(0, "-10")
        
        x_max_label = tk.Label(
            range_frame, 
            text="X Max:", 
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 10)
        )
        x_max_label.pack(side="left", padx=5)
        
        self.x_max_entry = tk.Entry(
            range_frame,
            font=("Arial", 10),
            width=5,
            bg=self.themes[self.current_theme]["number_bg"],
            fg=self.themes[self.current_theme]["number_fg"]
        )
        self.x_max_entry.pack(side="left", padx=5)
        self.x_max_entry.insert(0, "10")
        
        # Button frame
        button_frame = tk.Frame(graph_frame, bg=self.themes[self.current_theme]["bg"])
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Plot button
        plot_button = ttk.Button(
            button_frame,
            text="Plot",
            command=self.plot_graph,
            style="Equal.TButton"
        )
        plot_button.pack(side="left", padx=5)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_graph,
            style="Clear.TButton"
        )
        clear_button.pack(side="left", padx=5)
        
        # Back button
        back_button = ttk.Button(
            button_frame,
            text="Back to Calculator",
            command=self.switch_to_calculator_mode,
            style="Function.TButton"
        )
        back_button.pack(side="right", padx=5)
        
        # Canvas for graph - with better integration
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add navigation toolbar for zoom/pan functionality
        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()
        
        # Initialize the plot
        self.ax.grid(True)
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Graph')
        self.canvas.draw()
    
    def show_solver(self):
        """Show a simple equation solver dialog"""
        solver_window = tk.Toplevel(self.root)
        solver_window.title("Equation Solver")
        solver_window.geometry("300x200")
        solver_window.configure(bg=self.themes[self.current_theme]["bg"])
        
        # Instruction
        instruction = tk.Label(
            solver_window,
            text="Enter an equation to solve\n(Use 'x' as the variable)",
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 12)
        )
        instruction.pack(pady=10)
        
        # Equation entry
        equation_frame = tk.Frame(solver_window, bg=self.themes[self.current_theme]["bg"])
        equation_frame.pack(fill="x", padx=10)
        
        equation_entry = tk.Entry(
            equation_frame,
            font=("Arial", 12),
            bg=self.themes[self.current_theme]["number_bg"],
            fg=self.themes[self.current_theme]["number_fg"]
        )
        equation_entry.pack(fill="x", padx=5)
        equation_entry.insert(0, "x**2 = 9")
        
        # Result label
        result_var = tk.StringVar()
        result_label = tk.Label(
            solver_window,
            textvariable=result_var,
            bg=self.themes[self.current_theme]["bg"],
            fg=self.themes[self.current_theme]["display_fg"],
            font=("Arial", 12)
        )
        result_label.pack(pady=10)
        
        # Solve button
        def solve_equation():
            equation = equation_entry.get()
            try:
                # Handle common equation formats
                if "=" in equation:
                    left, right = equation.split("=")
                    equation = f"({left}) - ({right})"
                
                # For simple equations, use np.roots
                if "x**2" in equation and "x**3" not in equation:
                    # Extract coefficients for ax^2 + bx + c = 0
                    # This is a very simplified approach
                    import re
                    
                    # Find coefficient of x^2
                    a_match = re.search(r'([+-]?\s*\d*\.?\d*)\s*\*?\s*x\*\*2', equation)
                    a = 1.0 if a_match and not a_match.group(1) else 0.0
                    if a_match and a_match.group(1):
                        a_str = a_match.group(1).replace(" ", "")
                        if a_str in ["+", "-"]:
                            a = float(a_str + "1")
                        else:
                            a = float(a_str)
                    
                    # Find coefficient of x
                    b_match = re.search(r'([+-]?\s*\d*\.?\d*)\s*\*?\s*x(?!\*)', equation)
                    b = 0.0
                    if b_match and b_match.group(1):
                        b_str = b_match.group(1).replace(" ", "")
                        if b_str in ["+", "-"]:
                            b = float(b_str + "1")
                        else:
                            b = float(b_str)
                    
                    # Find constant term - very simplified approach
                    c_pattern = r'([+-]?\s*\d+\.?\d*(?!\s*\*?\s*x))'
                    c_matches = re.findall(c_pattern, equation)
                    c = 0.0
                    for match in c_matches:
                        c_str = match.replace(" ", "")
                        c += float(c_str)
                    
                    roots = np.roots([a, b, c])
                    result_var.set(f"Solutions: x = {', '.join([str(round(root, 4)) for root in roots])}")
                else:
                    # For linear equations or more complex equations
                    # Use a numerical method
                    def f(x):
                        return eval(equation)
                    
                    # Try to find a root between -100 and 100
                    from scipy import optimize
                    try:
                        root = optimize.brentq(f, -100, 100)
                        result_var.set(f"Solution: x ≈ {round(root, 4)}")
                    except:
                        result_var.set("Could not find a solution in range [-100, 100]")
            
            except Exception as e:
                result_var.set(f"Error: {str(e)}")
        
        solve_button = ttk.Button(
            solver_window,
            text="Solve",
            command=solve_equation,
            style="Equal.TButton"
        )
        solve_button.pack(pady=10)
    
    def plot_graph(self):
        """Plot the function on the graph"""
        # Clear the current plot
        self.ax.clear()
        
        # Get the function and range
        function_str = self.function_entry.get()
        try:
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Range", "Please enter valid numbers for X Min and X Max.")
            return
        
        # Create x values
        x_values = np.linspace(x_min, x_max, 1000)
        
        # Better function parsing - handle more expressions
        expression = function_str
        
        # Handle implicit multiplication like 2x -> 2*x
        import re
        expression = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'(\))([a-zA-Z\(])', r'\1*\2', expression)
        
        # Replace common functions with numpy versions
        replacements = [
            ("sin(", "np.sin("), 
            ("cos(", "np.cos("),
            ("tan(", "np.tan("),
            ("exp(", "np.exp("),
            ("sqrt(", "np.sqrt("),
            ("log10(", "np.log10("),
            ("log(", "np.log("),
            ("ln(", "np.log("),
            ("abs(", "np.abs("),
            ("pi", "np.pi"),
            ("^", "**"),  # Handle caret for exponents
        ]
        
        for old, new in replacements:
            expression = expression.replace(old, new)
        
        print(f"Original: {function_str} -> Parsed: {expression}")  # Debugging
        
        # Create vectorized function using numpy
        try:
            # Create a safe evaluation environment
            safe_dict = {
                'np': np,
                'x': x_values,
                'e': np.e,  # Add e constant
                'pi': np.pi  # Add pi constant
            }
            
            # Evaluate the function 
            y_values = eval(expression, {"__builtins__": {}}, safe_dict)
            
            # Plot with a more visible line
            self.ax.plot(x_values, y_values, 'b-', linewidth=2)
            
            # Set grid and labels
            self.ax.grid(True)
            self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title(f'f(x) = {function_str}')
            
            # Update the plot
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not plot function: {str(e)}")
            print(f"Graphing error: {str(e)}")