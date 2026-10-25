import tkinter as tk
from tkinter import ttk, messagebox
import re

class Pila:
    def __init__(self):
        self.items = []
    def push(self, valor):
        self.items.append(valor)
    def pop(self):
        if not self.items:
            raise ValueError("La expresión está incompleta.")
        return self.items.pop()

def aplicar(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0: raise ValueError("No se puede dividir entre cero.")
        return a / b
    if op == '^': return a ** b
    raise ValueError(f"Operador no reconocido: {op}")

def evaluar(tokens, tipo):
    pila = Pila()
    pasos = []
    secuencia = tokens if tipo == "Posfija" else list(reversed(tokens))
    for token in secuencia:
        if re.fullmatch(r'-?\d+(?:\.\d+)?', token):
            pila.push(float(token))
            pasos.append((f"Apilar {token}", pila.items.copy()))
        elif token in {"+", "-", "*", "/", "^"}:
            if tipo == "Posfija":
                b, a = pila.pop(), pila.pop()
            else:
                a, b = pila.pop(), pila.pop()
            res = aplicar(a, b, token)
            pila.push(res)
            pasos.append((f"Calcular {a:g} {token} {b:g} = {res:g}", pila.items.copy()))
        else:
            raise ValueError(f"Token no válido: {token}")
    if len(pila.items) != 1:
        raise ValueError("La expresión no es válida. Revisa los espacios y operadores.")
    return pila.items[0], pasos

class App:
    def __init__(self, root):
        self.root = root
        root.title("Evaluador de expresiones con pila")
        root.geometry("820x570")
        root.minsize(700, 500)
        ttk.Label(root, text="Evaluador de expresiones aritméticas", font=("Segoe UI", 17, "bold")).pack(pady=(12, 4))
        ttk.Label(root, text="Usa espacios entre cada número y operador. Operadores: +  -  *  /  ^").pack()
        form = ttk.Frame(root, padding=10)
        form.pack(fill="x")
        ttk.Label(form, text="Notación:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo = tk.StringVar(value="Posfija")
        ttk.Combobox(form, textvariable=self.tipo, values=["Posfija", "Prefija"], state="readonly", width=12).grid(row=0, column=1, padx=5)
        ttk.Label(form, text="Expresión:").grid(row=0, column=2, padx=5)
        self.expr = tk.StringVar(value="5 3 + 2 *")
        ttk.Entry(form, textvariable=self.expr, width=30).grid(row=0, column=3, padx=5, sticky="ew")
        ttk.Button(form, text="Evaluar", command=self.calcular).grid(row=0, column=4, padx=5)
        form.columnconfigure(3, weight=1)
        examples = ttk.Frame(root, padding=(10, 0))
        examples.pack(fill="x")
        ttk.Button(examples, text="Ejemplo posfijo", command=lambda: self.cargar("Posfija", "5 3 + 2 *")).pack(side="left", padx=3)
        ttk.Button(examples, text="Ejemplo prefijo", command=lambda: self.cargar("Prefija", "* + 5 3 2")).pack(side="left", padx=3)
        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)
        left = ttk.LabelFrame(main, text="Visualización de la pila", padding=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.canvas = tk.Canvas(left, bg="#f4f7fb", highlightthickness=0, width=300)
        self.canvas.pack(fill="both", expand=True)
        right = ttk.LabelFrame(main, text="Pasos de evaluación", padding=8)
        right.pack(side="right", fill="both", expand=True)
        self.log = tk.Listbox(right, font=("Consolas", 10), height=15)
        self.log.pack(fill="both", expand=True)
        self.result = ttk.Label(root, text="Resultado: —", font=("Segoe UI", 13, "bold"))
        self.result.pack(pady=(0, 12))
        self.canvas.bind("<Configure>", lambda e: self.dibujar(self.ultima_pila))
        self.ultima_pila = []
        self.calcular()
    def cargar(self, tipo, expr):
        self.tipo.set(tipo); self.expr.set(expr); self.calcular()
    def calcular(self):
        try:
            tokens = self.expr.get().split()
            if not tokens: raise ValueError("Escribe una expresión.")
            valor, pasos = evaluar(tokens, self.tipo.get())
            self.log.delete(0, tk.END)
            for i, (desc, estado) in enumerate(pasos, 1):
                self.log.insert(tk.END, f"{i}. {desc} | Pila: {estado}")
            self.ultima_pila = [valor]
            self.dibujar(self.ultima_pila)
            self.result.config(text=f"Resultado: {valor:g}")
        except Exception as e:
            messagebox.showerror("No se pudo evaluar", str(e))
    def dibujar(self, items):
        c = self.canvas; c.delete("all")
        w = max(c.winfo_width(), 280); h = max(c.winfo_height(), 260)
        x = w // 2
        c.create_text(x, 20, text="TOPE DE LA PILA", font=("Segoe UI", 10, "bold"), fill="#243b53")
        c.create_line(x-75, 40, x-75, h-20, fill="#526777", width=3)
        c.create_line(x+75, 40, x+75, h-20, fill="#526777", width=3)
        c.create_line(x-75, h-20, x+75, h-20, fill="#526777", width=3)
        if not items:
            c.create_text(x, h//2, text="Pila vacía", fill="#526777")
        else:
            visible = items[-8:]
            for idx, val in enumerate(visible):
                y2 = h-25-idx*34; y1 = y2-29
                c.create_rectangle(x-68, y1, x+68, y2, fill="#4f86c6", outline="#2f5d8c", width=2)
                c.create_text(x, (y1+y2)//2, text=f"{val:g}", fill="white", font=("Segoe UI", 11, "bold"))
        c.create_text(x, h-7, text="BASE", fill="#526777", font=("Segoe UI", 8))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
