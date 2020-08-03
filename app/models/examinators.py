class Examinator:
    def __init__(self, name: str, damage: int, health: int, defence: int, rank: str, power: int):
        self.name = name
        self.damage = damage
        self.health = health
        self.defence = defence
        self.rank = rank
        self.power = power


exam0 = Examinator('Экзаминатор(F)', 5, 10, 10, 'F', 100)
exam1 = Examinator('Экзаминатор(E)', 10, 20, 20, 'E', 400)
exam2 = Examinator('Экзаминатор(D)', 17, 35, 35, 'D', 1190)
exam3 = Examinator('Экзаминатор(C)', 30, 60, 60, 'C', 3600)
exam4 = Examinator('Экзаминатор(B)', 50, 100, 100, 'B', 10000)
exam5 = Examinator('Экзаминатор(A)', 80, 150, 150, 'A', 24000)
exam6 = Examinator('Экзаминатор(S)', 125, 250, 250, 'S', 62500)

exams = [exam0, exam1, exam2, exam3, exam4, exam5, exam6]