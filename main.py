import helman 
import a5 



#test a5
cryptpo = a5.A5()
message = "hello world, i love cryptography"
print(message)
cypher = cryptpo.cypher(message)
print(a5.bytes_to_string(cypher))
decypher = cryptpo.decypher(cypher)
print(a5.bytes_to_string(decypher))

#test helman avec echange de clés entre Alice et Bob

bob = a5.A5()
alice = a5.A5()

BobKey = a5.bits_to_int(bob.KEY_INIT)
AliceKey = a5.bits_to_int(alice.KEY_INIT)


p = 73354658883438629681302852888425819414799977307764540519012033294405083679929453038354
58008138016530970254318172965357391199557120543758438497838095839321

g = 3

shared_secret = helman.diffie_hellman(p, g, a=BobKey, b=AliceKey)
print("Bob's key:", BobKey)
print("Alice's key:", AliceKey)
print("Shared secret:", shared_secret)