import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
import pandas as pd
from fractions import Fraction
import random
from math import gcd


# U|y> = |ay mod 15>
# возвращает controlled-U элемент для а, повторяющийся power раз
def c_amod15(a, power):
    if a not in [2, 7, 8, 11, 13]:
        raise ValueError("Число 'a' должно быть 2, 7, 8, 11 или 13")
    U = QuantumCircuit(4)
    for iteration in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a == 11:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    c_U = U.control()
    return c_U


# схема QFT (Квантовое преобразование Фурье)
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    return qc


# поиск фазы
def qpe_amod15(a):
    n_count = 8
    qc = QuantumCircuit(4+n_count, n_count)
    for q in range(n_count):
        qc.h(q)  # инициализация расчетных кубитов в состоянии |+>
    qc.x(3+n_count)  #вспомогательные регистры в состоянии |1>
    for q in range(n_count):  # выполнение controlled-U операции
        qc.append(c_amod15(a, 2**q), [q] + [i+n_count for i in range(4)])
    qc.append(qft_dagger(n_count), range(n_count))
    qc.measure(range(n_count), range(n_count))

    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(qc, qasm_sim)
    obj = assemble(t_qc, shots=1)
    result = qasm_sim.run(qobj, memory=True).result()
    readings = result.get_memory()
    phase = int(readings[0], 2)/(2**n_count)

    return phase


n_count = 8
a = 13

qc = QuantumCircuit(n_count + 4, n_count)

# инициализация расчетных кубитов в состоянии |+>
for q in range(n_count):
    qc.h(q)

# вспомогательные регистры в состоянии |1>
qc.x(3 + n_count)

# выполнение controlled-U операции
for q in range(n_count):
    qc.append(c_amod15(a, 2 ** q),
              [q] + [i + n_count for i in range(4)])

# выполнение inverse-QFT
qc.append(qft_dagger(n_count), range(n_count))

# измерение схемы
qc.measure(range(n_count), range(n_count))
print(qc)
print()

# создание симулятора для посмотра результатов измерений
qasm_sim = Aer.get_backend('qasm_simulator')
t_qc = transpile(qc, qasm_sim)
qobj = assemble(t_qc)
results = qasm_sim.run(qobj).result()
counts = results.get_counts()
print(counts)
print()

# вывод результатов
rows, measured_phases = [], []
for output in counts:
    decimal = int(output, 2)  # преобразование из двоичной системы в десятичную
    phase = decimal/(2**n_count)  # поиск значений фаз
    measured_phases.append(phase)
    rows.append([f"{output}(bin) = {decimal:>3}(dec)",
                 f"{decimal}/{2**n_count} = {phase:.2f}"])

headers = ["Выходной регистр", "Фаза"]
df = pd.DataFrame(rows, columns=headers)
print(df)
print()

# вывод результата на основании найденных фаз
rows = []
for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(15)
    rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])

headers = ["Фаза", "Дробь", "Результат угадывания периода"]
df = pd.DataFrame(rows, columns=headers)
print(df)
print()


# поиск простых делителей числа
N = 15
a = 7
factor_found = False
while not factor_found:
    phase = qpe_amod15(a)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    if phase != 0:
        guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
        for guess in guesses:
            if guess not in [1, N] and (N % guess) == 0:  # проверка того, что угаданное число действительно является делителем
                print('Простые делители числа', N, ':', guess)
                factor_found = True