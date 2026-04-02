import random 
ORANGE_INDEX = [8,10,10]
LFSR_1_TAPS = [18,17,16,13]
LFSR_2_TAPS = [21,20]
LFSR_3_TAPS = [22,21,20]

def xor(a, b):
    return 1 if not a == b else 0

def string_to_bytes(string:str) : 
    return [list(map(int,format(ord(char),'08b'))) for char in string]

def bits_to_int(bits_table) :
    integer = 0
    for bit in bits_table:
        integer = (integer << 1) | (1 if bit else 0)
    return integer


def bytes_to_string(bytes_table) :
    string = ""
    for byte in bytes_table :
        char = 0
        for i in range(8):
            char += byte[i] * (2**(7-i))
        string += chr(char)
    return string

def get_feedback(LFSR, taps):
    feedback = LFSR[taps[0]]
    for v in range(1,len(taps)):
        feedback = xor(LFSR[taps[v]], feedback) 
    return feedback

def inc_counter(counter):
    i = len(counter)-1
    while i >= 0:
        if counter[i] == 0:
            counter[i] = 1
            return counter
        else:
            counter[i] = 0
            i -= 1

class A5: 
    def __init__(self, KEY_INIT=None):
        self.LFSR_1 = [0]*19
        self.LFSR_2= [0]*22
        self.LFSR_3= [0]*23
        self.KEY_INIT = KEY_INIT if KEY_INIT is not None else [random.randint(0, 1) for _ in range(64)]
        self.COUNT =  [0]*22
        self.KEY = []

    def initInternalStates(self):
        # Remise à zéro des LFSR avant chargement de la clé
        self.LFSR_1 = [0]*19
        self.LFSR_2 = [0]*22
        self.LFSR_3 = [0]*23
        self.COUNT = [0]*22

        # Chargement de la clé (64 bits) dans les 3 LFSR
        for i in range(64):
            feedback = xor(get_feedback(self.LFSR_1, LFSR_1_TAPS), self.KEY_INIT[i])
            self.LFSR_1.insert(0, feedback); self.LFSR_1.pop()

            feedback = xor(get_feedback(self.LFSR_2, LFSR_2_TAPS), self.KEY_INIT[i])
            self.LFSR_2.insert(0, feedback); self.LFSR_2.pop()

            feedback = xor(get_feedback(self.LFSR_3, LFSR_3_TAPS), self.KEY_INIT[i])
            self.LFSR_3.insert(0, feedback); self.LFSR_3.pop()

        # Intégration du compteur de trames (22 bits) de la même façon
        for i in range(22):
            feedback = xor(get_feedback(self.LFSR_1, LFSR_1_TAPS), self.COUNT[i])
            self.LFSR_1.insert(0, feedback); self.LFSR_1.pop()

            feedback = xor(get_feedback(self.LFSR_2, LFSR_2_TAPS), self.COUNT[i])
            self.LFSR_2.insert(0, feedback); self.LFSR_2.pop()

            feedback = xor(get_feedback(self.LFSR_3, LFSR_3_TAPS), self.COUNT[i])
            self.LFSR_3.insert(0, feedback); self.LFSR_3.pop()
        
    #Retourne un tableau de taille 3 de 0 et de 1 qui indique quel LFSR est à faire cycler (1 si à cycler sinon 0)
    def get_LFSRs_to_cycle_with_majority(self):
        lfsrs_to_shift = [False]*3
        s = self.LFSR_1[ORANGE_INDEX[0]] + self.LFSR_2[ORANGE_INDEX[1]] + self.LFSR_3[ORANGE_INDEX[2]]
        majority = 1 if s >= 2 else 0        
        if(self.LFSR_1[ORANGE_INDEX[0]] == majority) : lfsrs_to_shift[0] = True
        if(self.LFSR_2[ORANGE_INDEX[1]] == majority) : lfsrs_to_shift[1] = True
        if(self.LFSR_3[ORANGE_INDEX[2]] == majority) : lfsrs_to_shift[2] = True
        return lfsrs_to_shift

    #Permet de faire cycler les LFSR indiqués dans le tableau d'entrée, et d'ajouter le bit de sortie à la clé si append = True
    def shift_LFSRs(self,lfsrs_to_shift, append = False):
        bit_to_append = 0
        for i in range (3):
            if(lfsrs_to_shift[i] == True):
                match i : 
                    case 0 :
                        feedback = get_feedback(self.LFSR_1, LFSR_1_TAPS)
                        self.LFSR_1.insert(0,feedback)
                        bit_to_append = self.LFSR_1.pop()
                    case 1 :
                        feedback = get_feedback(self.LFSR_2, LFSR_2_TAPS)
                        self.LFSR_2.insert(0,feedback)
                        bit_to_append = xor(bit_to_append,self.LFSR_2.pop())
                    case 2 :                 
                        feedback = get_feedback(self.LFSR_3, LFSR_3_TAPS)
                        self.LFSR_3.insert(0,feedback)
                        bit_to_append = xor(bit_to_append,self.LFSR_3.pop())
        if(append == True):
            self.KEY.append(bit_to_append)

    #Fait cycler les LFSR pour générer les 8 prochains bits de la clé de chiffrement
    def cycle_key(self):
        self.KEY = []
        for i in range(8):
            lfsrs_to_shift = self.get_LFSRs_to_cycle_with_majority()
            self.shift_LFSRs(lfsrs_to_shift, True)

    #Chiffre le mot d'entrée en utilisant 8 bits de clé pour chaque caractère, et en incrémentant le compteur de trames à chaque caractère
    def cypher(self, word:str): 
        cypher = []
        self.initInternalStates()
        bytes_table = string_to_bytes(word)

        for byte in bytes_table :
            cypherByte = []
            self.cycle_key()
            for i in range(8):
                cypherByte.append(xor(byte[i], self.KEY[i]))
            cypher.append(cypherByte)
            inc_counter(self.COUNT)
        return cypher
    
    #Déchiffre le mot d'entrée en utilisant 8 bits de clé pour chaque caractère, et en incrémentant le compteur de trames à chaque caractère
    def decypher(self, cypher):
        word = []
        self.initInternalStates()
        for cypherByte in cypher :
            byte = []
            self.cycle_key()
            for i in range(8):
                byte.append(xor(cypherByte[i], self.KEY[i]))
            word.append(byte)
            inc_counter(self.COUNT)
        return word

