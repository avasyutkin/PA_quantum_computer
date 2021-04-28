from qiskit import QuantumCircuit, assemble, Aer

sim = Aer.get_backend('qasm_simulator')  # локальный симулятор
qc = QuantumCircuit(4, 2)  # схема с четырьмя кубитами и двумя выходами

qc.x(0)  # инвертируем нулевой кубит (NOT)
qc.x(1)

qc.cx(0, 2)  # XOR нулевого кубита со вторым, результат записывается во второй (CNOT)
qc.cx(1, 2)
qc.ccx(0, 1, 3)  # AND нулевого кубита с первым, результат записывается в третий (CCNOT)

qc.measure(2, 0)  # результат XOR записывается в нулевой кубит
qc.measure(3, 1)  # AND - в первый

print(qc)  # принт схемы

qс_job = assemble(qc)  # преобразование схемы в объект, который сможем запустить в бэкэнде
counts = sim.run(qс_job).result()  # запуск эксперимента
print(counts.get_counts())  # результаты
