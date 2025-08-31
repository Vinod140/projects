import tkinter as tk
from tkinter import ttk, messagebox
import math

# History
history_list = []

# Calculator Functions
def calculate_expression():
    expr = calc_input.get()
    try:
        expr = expr.replace("√", "math.sqrt").replace("^2", "**2")
        result = eval(expr)
        calc_output.config(text=str(result))
        history_list.append(f"{expr} = {result}")
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")

def clear_calc():
    calc_input.delete(0, tk.END)
    calc_output.config(text="")

def backspace_calc():
    current = calc_input.get()
    calc_input.delete(0, tk.END)
    calc_input.insert(0, current[:-1])

def append_calc(char):
    calc_input.insert(tk.END, char)

def show_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("Calculation History")
    hist_win.geometry("300x400")
    hist_win.config(bg="gray")
    tk.Label(hist_win, text="History", font=("Arial", 16, "bold"), bg="gray", bd=2, relief="solid").pack(pady=10)
    hist_text = tk.Text(hist_win, font=("Arial", 12), width=40, height=20, bg='silver', bd=2, relief="solid")
    hist_text.pack(pady=10)
    hist_text.insert(tk.END, "\n".join(history_list))
    hist_text.config(state='disabled')

# Tool Functions
def open_tool(title, hint_text, conversion_func, is_time_conversion=False):
    tool_win = tk.Toplevel(root)
    tool_win.title(title)
    tool_win.geometry("400x400")
    tool_win.config(bg="gray", bd=3, relief="solid")

    # Hint label
    tk.Label(tool_win, text=hint_text, font=("Arial", 14, "bold"), fg="#333333", bg="#f7f7f7", bd=2, relief="solid").pack(pady=10)

    # Input screen
    input_var = tk.StringVar()
    tool_input = tk.Entry(tool_win, textvariable=input_var, font=("Arial", 14), justify="center", bd=2, relief="solid")
    tool_input.pack(pady=5)

    # Output screen
    tool_output = tk.Label(tool_win, text="", font=("Arial", 14), fg="#333333", bg="#e0e0e0", width=30, height=2, bd=2, relief="solid")
    tool_output.pack(pady=10)

    dynamic_frame = None

    def calculate():
        nonlocal dynamic_frame
        if dynamic_frame:
            dynamic_frame.destroy()
        try:
            val = float(tool_input.get())
            tool_output.config(text=conversion_func(val))

            if is_time_conversion:
                dynamic_frame = tk.Frame(tool_win, bg="#e0e0e0", bd=2, relief='solid')
                dynamic_frame.pack(pady=10)
                minutes = val * 60
                seconds = val * 3600
                tk.Label(dynamic_frame, text=f"Minutes: {minutes:.2f}", font=("Arial", 12), fg="#006600", bg="#e0e0e0", bd=1, relief="solid").pack(pady=2)
                tk.Label(dynamic_frame, text=f"Seconds: {seconds:.2f}", font=("Arial", 12), fg="#000099", bg="#e0e0e0", bd=1, relief="solid").pack(pady=2)

        except:
            tool_output.config(text="Invalid Input!")

    tk.Button(tool_win, text="Convert", width=12, command=calculate, bg="gray", fg="black", bd=2, relief="raised").pack(pady=5)
    tk.Button(tool_win, text="Clear", width=12, command=lambda: tool_input.delete(0, tk.END), bg="gray", fg="black", bd=2, relief="raised").pack(pady=5)
    tk.Button(tool_win, text="Back", width=12, command=tool_win.destroy, bg="gray", fg="black", bd=2, relief="raised").pack(pady=5)

# Conversion Logic
def c_to_f(val): return f"{(val * 9/5) + 32:.2f} °F"
def km_to_mile(val): return f"{val * 0.621371:.2f} miles"
def kg_to_lb(val): return f"{val * 2.20462:.2f} lbs"
def sq_m_to_sq_ft(val): return f"{val * 10.7639:.2f} ft²"
def hr_to_min_sec(val): return f"{val} hr = {val*60:.2f} min = {val*3600:.2f} sec"
def mon_to_day(val): return f"{val*30:.2f} days"
def l_to_ml(val): return f"{val*1000:.2f} ml"
def m_to_cm(val):return f"{val*100:.2f} cm"

# Main GUI
root = tk.Tk()
root.title("Calculator")
root.geometry("370x650")
root.config(bg="gray")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Calculator Tab
calc_frame = tk.Frame(notebook, bg="lightgray")
notebook.add(calc_frame, text="Calculator")

# Input screen 
calc_input = tk.Entry(calc_frame, font=("Arial", 20), justify="center", bd=2, relief="solid", bg="gray", fg="#0A0A0A")
calc_input.pack(fill="both", ipadx=8, ipady=15, pady=5)

# Output screen
calc_output = tk.Label(calc_frame, text="", font=("Arial", 16), fg="#000000", bg="#807a7a", width=25, height=2, bd=2, relief="solid")
calc_output.pack(pady=10)

# History button
tk.Button(
    calc_frame,text="History",font=("Arial", 12),width=12,bg="#ADCACC",fg="#0A0A0A",bd=2,relief="raised",
    highlightbackground="black",highlightthickness=2,command=show_history
).pack(pady=5)

# Calculator buttons
btns = [
    ["7", "8", "9", "<-"],
    ["4", "5", "6", "Clear"],
    ["1", "2", "3", "="],
    ["0", ".", "*", "-"],
    ["(", ")", "/", "+"],
    ["x²", "√", "%"]
]

btn_frame = tk.Frame(calc_frame, bg="gray", bd=2, relief="solid")
btn_frame.pack()

for r, row in enumerate(btns):
    for c, char in enumerate(row):
        # Button color logic
        if char == "Clear":
            color_bg = "#FF6B6B"   # Red-ish background for Clear
            color_fg = "white"
        elif char == "<-":
            color_bg = "#FFD93D"   # Yellow-ish background for Backspace
            color_fg = "black"
        elif char == "=":
            color_bg = "#4ECDC4"   # Cyan-ish background for Equals
            color_fg = "white"
        else:
            color_bg = "lightgray"
            color_fg = "black"

        b = tk.Button(
            btn_frame, text=char, font=("Arial", 14), width=5, height=2,
            bg=color_bg, fg=color_fg,
            bd=2, relief="raised",
            command=lambda ch=char: (calculate_expression() if ch=="=" else
                                     clear_calc() if ch=="Clear" else
                                     backspace_calc() if ch=="<-" else
                                     append_calc(ch))
        )
        b.grid(row=r, column=c, padx=5, pady=5)


# Tools Tab 
tools_frame = tk.Frame(notebook, bg="gray", bd=3, relief="solid")
notebook.add(tools_frame, text="Tools")

tools = [
    ("Temprature", "Enter °C", c_to_f, False),
    ("lenght","Enter m", m_to_cm,False),
    ("Distance", "Enter Km", km_to_mile, False),
    ("Weight", "Enter Kg", kg_to_lb, False),
    ("Area", "Enter m²", sq_m_to_sq_ft, False),
    ("Time", "Enter Hour", hr_to_min_sec, True),
    ('days',"enter months", mon_to_day, False),
    ("Volume", "Enter L", l_to_ml, False),
]

tool_btn_frame = tk.Frame(tools_frame, bg="gray")
tool_btn_frame.pack(pady=20)

for i, (title, hint, func, time_flag) in enumerate(tools):
    r, c = divmod(i, 2)
    tk.Button(
        tool_btn_frame, text=title, font=("Arial", 12), width=15, height=3,
        bg="silver", fg="black",
        bd=2, relief="raised",
        command=lambda t=title, h=hint, f=func, flag=time_flag: open_tool(t, h, f, flag)
    ).grid(row=r, column=c, padx=8, pady=8)

root.mainloop()
