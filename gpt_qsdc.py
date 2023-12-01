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

#Initialize EPR Pairs
N = 10  # Example, total number of EPR pairs
epr_pairs = []

for _ in range(N):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.z(0)
    epr_pairs.append(qc)

#Step 3: Send C-Sequence to Bob and Eavesdropping Check
#Alice sends the C-sequence to Bob. Then, they perform an eavesdropping check.

# Example of eavesdropping check procedure
# In practice, Bob should choose randomly and Alice should measure accordingly
# For simplicity, here we assume they both measure in the Z-basis
qc: QuantumCircuit
for qc in epr_pairs[4:8]:
    qc.measure(0, 0)
    qc.measure(1, 1)
simulator = Aer.get_backend('qasm_simulator')
results = [execute(qc, simulator, shots=100).result().get_counts(qc) for qc in epr_pairs[4:8]]
# Check results for eavesdropping
print("begin c check")
for result in results:
    print(result)
print("end c check")

#Alice encodes the message
message = '0123'  # Example binary message

# Encoding the message
for i, bit_pair in enumerate(message):
    if bit_pair == '0':
        pass
    elif bit_pair == '1':
        epr_pairs[i].z(1)
    elif bit_pair == '2':
        epr_pairs[i].x(1)
    elif bit_pair == '3':
        epr_pairs[i].y(1)
        #epr_pairs[i].s(1)
        #.s(1) applies S-gate, which is phase shift, which is multiply by i

#Transmission and Bob's Measurement
# In Qiskit, we don't have a direct way to perform Bell-basis measurement
# Instead, we can reverse the process of creating a Bell pair and then measure in the computational basis
for qc in epr_pairs:
    qc.z(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

#Simulation
simulator = Aer.get_backend('qasm_simulator')
results = [execute(qc, simulator, shots=100).result().get_counts(qc) for qc in epr_pairs]

# Check results for eavesdropping
for result in results:
    print(result)
    

#Error correction goes here if we want to implement it...