class DCS:
    def __init__(self, CR=1.5, P_line=5.0, q_ext=500.0):
        self.CR = CR          # степень сжатия
        self.P_line = P_line  # давление в магистрали, атм
        self.q_ext = q_ext    # сторонний газ, ст.м³/сут

    def P_in(self):
        """Давление на входе в ДКС"""
        if self.CR <= 1.0:
            return self.P_line
        return self.P_line / self.CR