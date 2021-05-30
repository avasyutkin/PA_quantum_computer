from numpy import pi
from qiskit import QuantumCircuit, transpile, assemble, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor


def qft_rotations(circuit, n):
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    qft_rotations(circuit, n)


qc = QuantumCircuit(4)
qft_rotations(qc, 4)
print(qc)


def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit


def qft(circuit, n):
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


def inverse_qft(circuit, n):
    qft_circ = qft(QuantumCircuit(n), n)
    invqft_circ = qft_circ.inverse()
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose()


nqubits = 3
number = 5

qc = QuantumCircuit(nqubits)
for qubit in range(nqubits):
    qc.h(qubit)

qc.p(number*pi/4, 0)
qc.p(number*pi/2, 1)
qc.p(number*pi, 2)
print(qc)

qc = inverse_qft(qc, nqubits)
qc.measure_all()
print(qc)

### запуск на IBMQ
IBMQ.enable_account('4787fb50663e3a6c8a25cc37f203de3a3fb373d544c597a42a94e47afc2a857b86f29e469dcd37bb48d58634693121b613f08d217e845e44f5f07bcd903935dc')
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= nqubits
                                                         and not x.configuration().simulator
                                                         and x.status().operational==True))

shots = 1024
transpiled_qc = transpile(qc, backend, optimization_level=3)
qobj = assemble(transpiled_qc, shots=shots)
job = backend.run(qobj)
job_monitor(job)
counts = job.result().get_counts()
print(counts)