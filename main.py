from random import randint
import helman 
import a5 

#test a5
print("==========testing A5/1 stream cipher implementation============:")
cryptpo = a5.A5()
message = "hello world, i love cryptography"
print("A5 message:", message)
cypher = cryptpo.cypher(message)
print("A5 cypher:", a5.bytes_to_string(cypher))
decypher = cryptpo.decypher(cypher)
print("A5 decypher:", a5.bytes_to_string(decypher))
print("\n\n")

#test Diffie-Hellman avec échange de clés entre Alice et Bob, et chiffrement du message d'Alice à Bob avec le secret partagé, et déchiffrement du message par Bob
print("==========testing Diffie-Hellman key exchange and A5/1 encryption with shared secret============:")
p = 73354658883438629681302852888425819414799977307764540519012033294405083679929453038354
58008138016530970254318172965357391199557120543758438497838095839321
g = 3
bobKey = randint(1, p-1)
aliceKey = randint(1, p-1)

#simulation de l'échange de clés Diffie-Hellman entre Alice et Bob, ici, on retourne le secret partagé
shared_secret = helman.diffie_hellman(p, g, a=bobKey, b=aliceKey)
print("Bob's key:", bobKey)
print("Alice's key:", aliceKey)
print("Shared secret:", shared_secret)

#Alice chiffre un message pour Bob en utilisant le secret partagé comme clé de chiffrement, et en incrémentant le compteur de trames à chaque caractère
alice = a5.A5(KEY_INIT=a5.string_to_bytes(str(shared_secret)))
bob = a5.A5(KEY_INIT=a5.string_to_bytes(str(shared_secret)))
aliceMessage = "This is a secret message from Alice to Bob"
aliceCypher = alice.cypher(aliceMessage)
print("Alice's message:", aliceMessage)
print("Alice's cypher:", a5.bytes_to_string(aliceCypher))

# Bob décrypte le message d'Alice
bobDecypher = bob.decypher(aliceCypher)
print("Bob's decypher:", a5.bytes_to_string(bobDecypher))
print("\n\n")




# exemple de génération d'un nombre premier et d'un générateur pour le groupe multiplicatif modulo ce nombre premier, utilisé dans l'algorithme de Diffie-Hellman
print("==========testing prime generation and generator finding for Diffie-Hellman============:")
p = helman.generate_premier()
print("Generated prime:", p)
g = helman.find_generator(p)
print("Generator:", g)