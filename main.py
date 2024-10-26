import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.primitives import BaseSamplerV2

class CustomSampler(BaseSamplerV2):
    def run(self, pubs, *, shots=None):
        if shots is None:

            shots = 1024
        results = []

        for pub in pubs:

            trans_circ = transpile(pub, backend=Aer.get_backend('qasm_simulator'))


            job = Aer.get_backend('qasm_simulator').run(trans_circ, shots=shots)

            results.append(job.result())


        return results
 
message = input("Enter Message: ")
n_bits = min(8 * len(message), 100)   

 
alice_bases = np.random.randint(2, size=n_bits)
bob_bases = np.random.randint(2, size=n_bits)

 
alice_bits = np.random.randint(2, size=n_bits)

 
qubits = []
for i in range(n_bits):
    qc = QuantumCircuit(1, 1)
    if alice_bits[i] == 1:
        qc.x(0)
    if alice_bases[i] == 1:
        qc.h(0)
    qc.measure(0, 0)
    qubits.append(qc)

 
sampler = CustomSampler()
results = sampler.run(qubits, shots=1024) # to get stable value

 
final_res = []
for result in results:
    counts = result.get_counts()

    measurement_result = int(max(counts, key=counts.get))

    final_res.append(measurement_result)
 
bob_m = []
for i in range(n_bits):
    if bob_bases[i] == 1:
        bob_m.append((final_res[i] + 1) % 2)

    else:
        bob_m.append(final_res[i])

#  key sifting
key_bits = []
for i in range(n_bits):
    if alice_bases[i] == bob_bases[i]:


        key_bits.append(bob_m[i])

 
mess_bits = ''.join(format(ord(char), '08b') for char in message)

print("\nMessage in binary:", mess_bits)


key_length = len(key_bits)
enc_bits = [
    int(mess_bits[i]) ^ key_bits[i % key_length]
    for i in range(len(mess_bits))
]

 
enc_mess = ''.join(map(str, enc_bits))

print("encrypted message in binary:", enc_mess)
 
dec_bits = [
    enc_bits[i] ^ key_bits[i % key_length]

    for i in range(len(enc_bits))
]
 
dec_mess = ''.join(
    chr(int(''.join(map(str, dec_bits[i:i + 8])), 2))

    for i in range(0, len(dec_bits), 8)
)

print("Decrypted message:", dec_mess)
print("Alice's bits:", alice_bits)
print("Alice's bases:", alice_bases)
print("Bob's bases:", bob_bases)
print("Bob's measurements:", bob_m)
print("Final key bits:", key_bits)
