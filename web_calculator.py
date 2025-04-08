from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import math
from matplotlib.figure import Figure
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form.get('expression', '')
        
        # Replace special operations
        expression = expression.replace("sqrt(", "math.sqrt(")
        expression = expression.replace("log10(", "math.log10(")
        expression = expression.replace("log(", "math.log(")
        expression = expression.replace("factorial(", "math.factorial(")
        expression = expression.replace("sin(", "math.sin(")
        expression = expression.replace("cos(", "math.cos(")
        expression = expression.replace("tan(", "math.tan(")
        
        # Handle percentage
        if "%" in expression:
            expression = expression.replace("%", "/100")
        
        # Calculate result
        result = eval(expression, {"__builtins__": {}, "math": math})
        
        return jsonify({"result": str(result), "error": None})
    except Exception as e:
        return jsonify({"result": None, "error": str(e)})

@app.route('/plot', methods=['POST'])
def plot():
    try:
        function_str = request.form.get('function', 'x')
        x_min = float(request.form.get('x_min', '-10'))
        x_max = float(request.form.get('x_max', '10'))
        
        # Create x values
        x_values = np.linspace(x_min, x_max, 1000)
        
        # Better function parsing with improved regex
        expression = function_str
        
        # Replace 'y' with 'x' for equation plotting
        if 'y' in expression and 'x' not in expression:
            expression = expression.replace('y', 'x')
        
        # Handle more implicit multiplication cases
        # Number followed by variable: 2x -> 2*x
        expression = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expression)
        
        # Number or variable followed by parenthesis: 2(x) -> 2*(x) or x(2) -> x*(2)
        expression = re.sub(r'(\d+|\w)(\()', r'\1*\2', expression)
        
        # IMPORTANT: Don't add multiplication between function names and parentheses
        # First, protect common function names
        expression = expression.replace('sin(', 'SIN_FUNC(')
        expression = expression.replace('cos(', 'COS_FUNC(')
        expression = expression.replace('tan(', 'TAN_FUNC(')
        expression = expression.replace('log(', 'LOG_FUNC(')
        expression = expression.replace('ln(', 'LN_FUNC(')
        expression = expression.replace('sqrt(', 'SQRT_FUNC(')
        
        # Closing parenthesis followed by opening parenthesis: )(  -> )*(
        expression = re.sub(r'(\))(\()', r'\1*\2', expression)
        
        # Closing parenthesis followed by number or variable: )2 or )x -> )*2 or )*x
        expression = re.sub(r'(\))(\w|\d)', r'\1*\2', expression)
        
        # Now restore the function names
        expression = expression.replace('SIN_FUNC(', 'sin(')
        expression = expression.replace('COS_FUNC(', 'cos(')
        expression = expression.replace('TAN_FUNC(', 'tan(')
        expression = expression.replace('LOG_FUNC(', 'log(')
        expression = expression.replace('LN_FUNC(', 'ln(')
        expression = expression.replace('SQRT_FUNC(', 'sqrt(')
        
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
        
        # Create a safe evaluation environment
        safe_dict = {
            'np': np,
            'x': x_values,
            'e': np.e,  # Add e constant
            'pi': np.pi  # Add pi constant
        }
        
        # Evaluate the function 
        y_values = eval(expression, {"__builtins__": {}}, safe_dict)
        
        # Create the figure with a more attractive style
        plt.style.use('ggplot')  # Use a nicer style
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot with a more visible line and better styling
        ax.plot(x_values, y_values, linewidth=2.5, color='#2196f3')
        
        # Set grid and labels with better styling
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axhline(y=0, color='#616161', linestyle='-', alpha=0.5, linewidth=1)
        ax.axvline(x=0, color='#616161', linestyle='-', alpha=0.5, linewidth=1)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(f'f(x) = {function_str}', fontsize=14, fontweight='bold')
        
        # Better styling for the figure
        fig.patch.set_facecolor('#f5f5f5')
        ax.set_facecolor('#f9f9f9')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Save the figure to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        
        # Convert PNG buffer to base64 string
        image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return jsonify({"image": image_data, "error": None})
    except Exception as e:
        return jsonify({"image": None, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 