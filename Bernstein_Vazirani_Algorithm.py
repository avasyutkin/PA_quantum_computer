from qiskit import Aer
from qiskit import QuantumCircuit, assemble

n = 4  # количество кубитов, необходимое для нахождения строки s
s = '1011'  # скрытая двоичная строка, которую мы должны найти

qc = QuantumCircuit(n + 1, n)

# переводим в состояние |->
qc.h(n)
qc.z(n)

for i in range(n):
    qc.h(i)  # применяем вентиль Адамара ко всем кубитам

qc.barrier()

s = s[::-1]  # разворачиваем s для соответствия порядку кубитов
for q in range(n):
    if s[q] == '0':
        qc.i(q)
    else:
        qc.cx(q, n)

qc.barrier()

for i in range(n):
    qc.h(i)

for i in range(n):
    qc.measure(i, i)  # измеряем

print(qc)

qasm_sim = Aer.get_backend('qasm_simulator')
shots = 1024
qobj = assemble(qc)
results = qasm_sim.run(qobj).result()
answer = results.get_counts()

print(answer)