import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import csv
import math

def ccw(A, B, C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def lines_intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def point_in_triangle(P, A, B, C):
    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
    b1 = sign(P, A, B) < 0.0
    b2 = sign(P, B, C) < 0.0
    b3 = sign(P, C, A) < 0.0
    return (b1 == b2) and (b2 == b3)

class RightTriangle:
    def __init__(self, vertices, color="lightblue"):
        self.vertices = vertices
        self.pivot = vertices[0]
        self.color = color

    def get_points(self):
        return [coord for v in self.vertices for coord in v]

    def rotate(self, angle=90):
        px, py = self.pivot
        rad = math.radians(angle)
        def rotate_point(x, y):
            dx, dy = x - px, y - py
            new_x = px + dx*math.cos(rad) - dy*math.sin(rad)
            new_y = py + dx*math.sin(rad) + dy*math.cos(rad)
            return new_x, new_y
        self.vertices[1] = rotate_point(*self.vertices[1])
        self.vertices[2] = rotate_point(*self.vertices[2])

    def intersects(self, other):
        edges1 = [(self.vertices[i], self.vertices[(i+1)%3]) for i in range(3)]
        edges2 = [(other.vertices[i], other.vertices[(i+1)%3]) for i in range(3)]
        for e1 in edges1:
            for e2 in edges2:
                if lines_intersect(e1[0], e1[1], e2[0], e2[1]):
                    return True
        if any(point_in_triangle(p, *other.vertices) for p in self.vertices):
            return True
        if any(point_in_triangle(p, *self.vertices) for p in other.vertices):
            return True
        return False

class TriangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лаба 8")
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        frame = tk.Frame(root)
        frame.pack()
        tk.Button(frame, text="Загрузить CSV", command=self.load_from_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Проверить пересечение", command=self.check_intersection).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Изменить цвет", command=self.recolor).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Повернуть выбранный", command=self.rotate_selected).pack(side=tk.LEFT, padx=5)

        self.triangles = []
        self.selected_triangle = None
        self.canvas.bind("<Button-1>", self.on_click)

    def load_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename:
            return
        try:
            with open(filename, newline='') as f:
                reader = csv.reader(f, delimiter=",")
                self.triangles.clear()
                for row in reader:
                    if len(row) < 6:
                        raise ValueError("Неверные данные в строке: " + str(row))
                    vertices = [tuple(map(float, row[i:i + 2])) for i in range(0, 6, 2)]
                    self.triangles.append(RightTriangle(vertices))
            self.redraw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

    def redraw(self):
        self.canvas.delete("all")
        for t in self.triangles:
            outline = "red" if t == self.selected_triangle else "black"
            self.canvas.create_polygon(t.get_points(), fill=t.color, outline=outline)

    def on_click(self, event):
        self.selected_triangle = None
        for t in reversed(self.triangles):
            poly_id = self.canvas.create_polygon(t.get_points(), outline="", fill="")
            if poly_id in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
                self.selected_triangle = t
            self.canvas.delete(poly_id)
        self.redraw()

    def rotate_selected(self):
        if not self.selected_triangle:
            messagebox.showinfo("Нет выбора", "Сначала выберите треугольник.")
            return
        self.selected_triangle.rotate()
        self.redraw()

    def recolor(self):
        if not self.selected_triangle:
            messagebox.showinfo("Нет выбора", "Сначала выберите треугольник.")
            return
        color_code = colorchooser.askcolor(title="Выберите цвет треугольника")
        if color_code[1]:
            self.selected_triangle.color = color_code[1]
            self.redraw()

    def check_intersection(self):
        n = len(self.triangles)
        if n < 2:
            messagebox.showinfo("Недостаточно данных", "Нужно хотя бы два треугольника.")
            return
        intersections = []
        for i in range(n):
            for j in range(i + 1, n):
                if self.triangles[i].intersects(self.triangles[j]):
                    intersections.append((i + 1, j + 1))
        if intersections:
            msg = "Пересекаются треугольники:\n" + "\n".join([f"{a} и {b}" for a, b in intersections])
            messagebox.showinfo("Результат", msg)
        else:
            messagebox.showinfo("Результат", "Ни один треугольник не пересекается")

if __name__ == "__main__":
    root = tk.Tk()
    app = TriangleApp(root)
    root.mainloop()
