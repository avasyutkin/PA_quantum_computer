from qiskit import QuantumCircuit, Aer, assemble
from numpy.random import randint
import numpy as np


def encode_message(bits, bases):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if bases[i] == 0:
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else:
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message


def measure_message(message, bases):
    backend = Aer.get_backend('qasm_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0:
            message[q].measure(0, 0)
        if bases[q] == 1:
            message[q].h(0)
            message[q].measure(0, 0)
        qasm_sim = Aer.get_backend('qasm_simulator')
        qobj = assemble(message[q], shots=1, memory=True)
        result = qasm_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements


def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            good_bits.append(bits[q])
    return good_bits


def sample_bits(bits, selection):
    sample = []
    for i in selection:
        i = np.mod(i, len(bits))
        sample.append(bits.pop(i))
    return sample


np.random.seed(seed=0)
n = 100


###   ШАГ 1   ###
# Алиса генерирует биты
alice_bits = randint(2, size=n)
print('Сообщение Алисы:', alice_bits)


###   ШАГ 2   ###
# Алиса генерирует массив bases, чтобы закодировать кубиты
alice_bases = randint(2, size=n)
print('Массив bases Алисы:', alice_bases)

message = encode_message(alice_bits, alice_bases)  # кодируем сообщение


"""
###   ПЕРЕХВАТ   ### 
eve_bases = randint(2, size=n)
intercepted_message = measure_message(message, eve_bases)
print(intercepted_message)
"""


###   ШАГ 3   ###
# Боб генерирует массив для измерения закодированных битов
bob_bases = randint(2,  size=n)
print('Массив bases Боба:', bob_bases)

bob_results = measure_message(message, bob_bases)
print('Сообщение, декодированное Бобом:', bob_results)


###   ШАГ 4   ###
# После того, как Алиса и Боб обменялись bases, они формируют свои секретные ключи (одинаковые), отбрасывая несовпадающие биты в bases
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)

print('Секретный ключ Алисы:', alice_key)
print('Секретный ключ Боба:', bob_key)


###   ШАГ 5   ###
# Алиса и Боб выбирают некоторое количество битов из секретных ключей и, обмениваясь, сравнивают их, после чего эти биты удаляются из ключа, так как уже не являются секретными
bit_selection = randint(n, size=15)

bob_sample = sample_bits(bob_key, bit_selection)
alice_sample = sample_bits(alice_key, bit_selection)

print('Биты Алисы для проверки:', str(alice_sample))
print('Биты Боба для проверки:', str(bob_sample))

if alice_key == bob_key:
    print('Общий секретный ключ равен:', alice_key)
else:
    print('Секретные ключи не совпадают. Было обнаружено вмешательство Евы.')