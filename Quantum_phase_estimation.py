import math
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit import QuantumCircuit


qc = QuantumCircuit(4, 3)
qc.x(3)

for qubit in range(3):
    qc.h(qubit)

repetitions = 1
for counting_qubit in range(3):
    for i in range(repetitions):
        qc.cp(math.pi/4, counting_qubit, 3)
    repetitions *= 2

qc.barrier()


def qft_dagger(qc, n):
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)

    for j in range(n):
        for m in range(j):
            qc.cp(-math.pi/float(2**(j-m)), m, j)
        qc.h(j)


qft_dagger(qc, 3)
qc.barrier()
for n in range(3):
    qc.measure(n, n)

print(qc)

qasm_sim = Aer.get_backend('qasm_simulator')
shots = 1024
t_qc = transpile(qc, qasm_sim)
qobj = assemble(t_qc, shots=shots)
results = qasm_sim.run(qobj).result()
answer = results.get_counts()
print(answer)


### запуск на IBMQ
IBMQ.enable_account('4787fb50663e3a6c8a25cc37f203de3a3fb373d544c597a42a94e47afc2a857b86f29e469dcd37bb48d58634693121b613f08d217e845e44f5f07bcd903935dc')
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
santiago = provider.get_backend('ibmq_santiago')

shots = 1024
t_qc = transpile(qc, santiago, optimization_level=3)
qobj = assemble(t_qc, shots=shots)
job = santiago.run(qobj).result()

print(job.get_counts())