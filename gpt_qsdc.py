""""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

qr = QuantumRegister(2)  # Quantum register with 2 qubits
cr = ClassicalRegister(2)  # Classical register with 2 bits
circuit = QuantumCircuit(qr, cr)

# Create an EPR pair
circuit.h(qr[0])  # Apply Hadamard gate to Alice's qubit
circuit.cx(qr[0], qr[1])  # CNOT gate with Alice's qubit as control and Bob's as target

# Alice encodes her message
message = '01'  # Example message
if message[0] == '1':
    circuit.z(qr[0])  # Apply Z gate if the first bit of the message is 1

# The second bit can be encoded similarly or using a different quantum gate
circuit.measure(qr, cr)  # Measure the qubits

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, simulator).result()
counts = result.get_counts(circuit)
print(counts)
"""




#Translated from paper:
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import random_unitary
import random
import numpy as np

simulator = Aer.get_backend('qasm_simulator')

#Initialize EPR Pairs
N = 20  # total number of EPR pairs
epr_pairs = []
num_qubits_to_check = 8
# EPR pairs used to check for eavesdropping which cannot contain the message bits, length should be num_qubits_to_check * 2 (check eavesdropping twice)
random_indices = np.random.choice(N, 2 * num_qubits_to_check, replace=False) 

for _ in range(N):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.z(0)
    epr_pairs.append(qc)

#Evil Eve gets a hold of num_qubits_to_eavesdrop qubits and eavesdrops on those (measures those in Bell basis)
#Eavesdropping:
"""
num_qubits_to_eavesdrop = 5
eavesdrop_indices = np.random.choice(N, num_qubits_to_eavesdrop, replace=False)
print("Eavesdropped bit indices:")
print(eavesdrop_indices)
for i in eavesdrop_indices:
    qc = epr_pairs[i]
    qc.z(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
print("begin eavesdropping results")
results = [execute(epr_pairs[i], simulator, shots=100).result().get_counts(epr_pairs[i]) for i in eavesdrop_indices]
for result in results:
    print(result)
print("end eavesdropping results")
"""

# Example of eavesdropping check procedure
# In practice, Bob should choose randomly and Alice should measure accordingly
# For simplicity, here we assume they both measure in the Z-basis
check_indices = random_indices[:len(random_indices)//2]
print("Eavesdrop check indices:")
print(check_indices)
for i in check_indices:
    epr_pairs[i].measure(0, 0)
    epr_pairs[i].measure(1, 1)
results = [execute(epr_pairs[i], simulator, shots=100).result().get_counts(epr_pairs[i]) for i in check_indices]
print("begin c check")
for result in results:
    print(result)
print("end c check")

#Alice does eavesdrop trick (apply Z gate to random bits for simplicity)
check_indices = random_indices[len(random_indices)//2:]
print("Second eavesdrop check indices:")
print(check_indices)
for i in check_indices:
    epr_pairs[i].z(1)

#Alice encodes the message
message = '0123'  # Example binary message
#the length of the message can be up to N - 2 * num_qubits_to_check qubits long
message_indices = [i for i in range(N) if i not in random_indices]
print("Message indices:")
print(message_indices)
# Encoding the message
for i, bit_pair in enumerate(message):
    if bit_pair == '0':
        pass
    elif bit_pair == '1':
        epr_pairs[message_indices[i]].z(1)
    elif bit_pair == '2':
        epr_pairs[message_indices[i]].x(1)
    elif bit_pair == '3':
        epr_pairs[message_indices[i]].y(1)
        #epr_pairs[i].s(1)
        #.s(1) applies S-gate, which is phase shift, which is multiply by i

#Evil Eve gets a hold of num_qubits_to_eavesdrop qubits and eavesdrops on those (measures those in Bell basis)
#Eavesdropping:

num_qubits_to_eavesdrop = 5
eavesdrop_indices = np.random.choice(N, num_qubits_to_eavesdrop, replace=False)
print("Eavesdropped bit indices:")
print(eavesdrop_indices)
for i in eavesdrop_indices:
    qc = epr_pairs[i]
    qc.z(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
print("begin eavesdropping results")
results = [execute(epr_pairs[i], simulator, shots=100).result().get_counts(epr_pairs[i]) for i in eavesdrop_indices]
for result in results:
    print(result)
print("end eavesdropping results")

#Bob checks eavesdropping
for qc in [epr_pairs[i] for i in check_indices]:
    qc.z(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
results = [execute(epr_pairs[i], simulator, shots=100).result().get_counts(epr_pairs[i]) for i in check_indices]
print("begin c check")
for result in results:
    print(result)
print("end c check")

#Transmission and Bob's Measurement
# In Qiskit, we don't have a direct way to perform Bell-basis measurement
# Instead, we can reverse the process of creating a Bell pair and then measure in the computational basis
for qc in [epr_pairs[i] for i in message_indices]:
    qc.z(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

results = [execute(epr_pairs[i], simulator, shots=100).result().get_counts(epr_pairs[i]) for i in message_indices]
print("begin message")
for result in results:
    print(result)
print("end message")

#Error correction goes here if we want to implement it...