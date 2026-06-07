class LinearInterpolator:
    """
    Простой линейный интерполятор.
    Нужен для расчёта вязкости газа по таблице.
    Реализован без numpy, как требует задание.
    """
    def __init__(self, xs: list, ys: list):
        if len(xs) != len(ys):
            raise ValueError("xs и ys должны быть одинаковой длины")
        
        # Проверяем, что xs отсортирован по возрастанию
        for i in range(1, len(xs)):
            if xs[i] <= xs[i-1]:
                raise ValueError("xs должны быть отсортированы по возрастанию")
        
        self.xs = xs
        self.ys = ys

    def predict(self, xp: float) -> float:
        """Возвращает значение y для заданного x"""
        if xp < self.xs[0] or xp > self.xs[-1]:
            raise ValueError(f"xp={xp} выходит за пределы данных")
        
        # Ищем между какими точками находится xp
        for i in range(len(self.xs) - 1):
            if self.xs[i] <= xp <= self.xs[i + 1]:
                x1 = self.xs[i]
                x2 = self.xs[i + 1]
                y1 = self.ys[i]
                y2 = self.ys[i + 1]
                
                # Формула линейной интерполяции
                y = y1 + (y2 - y1) * (xp - x1) / (x2 - x1)
                return y
        
        return self.ys[-1]