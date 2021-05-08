from qiskit import QuantumCircuit, assemble, Aer
from math import sqrt


### сложение битов
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
print('________________')
print()


### инициализация и измерение битов
qc = QuantumCircuit(1)
qc.initialize([1/sqrt(2), 1j/sqrt(2)], 0)  # инициализируем нулевой кубит как суперпозицию с равной вероятностью нуля и единицы ([1, 0] - |0>, [0, 1] - |1>, [1/sqrt(3), sqrt(2)*1j/sqrt(3)] - 0,33 для нуля и 0,66 - для единицы)
sim = Aer.get_backend('statevector_simulator')  # локальный симулятор

qс_job = assemble(qc)
result = sim.run(qс_job).result()
print(result.get_statevector())  # амплитуды вероятностей состояний кубита
print(result.get_counts())  # вероятности состояний кубита

qc.measure_all()  # измеряем сосояние кубита (измерение разрушает кубит - сбивает состояние)
print(qc)

qс_job = assemble(qc)
result = sim.run(qс_job).result()
print(result.get_statevector())
print(result.get_counts())
print('________________')
print()


### CNOT-Gate (инвертирует первый кубит, если значение второго равно 1)
sim = Aer.get_backend('statevector_simulator')

qc = QuantumCircuit(2)
qc.h(0)  # переводим первый кубит в состояние суперпозиции

qс_job = assemble(qc)
final_state = sim.run(qс_job).result()
print(final_state.get_statevector())  # проверяем, оставив второй без изменений

qc = QuantumCircuit(2)
qc.h(0)  # переводим первый кубит в состояние суперпозиции
qc.cx(0, 1)  # применяем CNOT
print(qc)

qс_job = assemble(qc)
final_state = sim.run(qс_job).result()
print(final_state.get_statevector())  # видим что эта операция привела к запутыванию кубитов
# как это работает:
# |a> = [a[00], a[01], a[10], a[11]]
# CNOT |a> =  [a[00], a[11], a[10], a[01]]

print('________________')
print()

