import hashlib
import pickle
import hmac

import struct 
UNIQUE_CODE = struct.pack( 'ff', 12.05, 19.99 )

txt = 'Turma de redes'

# Cria uma classe Dummy qualquer 
class Dummy:
    import json 
    def __init__( self, whatever : json = json.dumps('') ):
        self.we = whatever
    def __str__(self) -> str:
        print('Dammy class for examples')
obj = Dummy()

# Encoder de objetos - Precisa de um UNIQUE KEY : byte-array
def encode_object( obj : object, separator : str = '\n' ) -> bytes: 
    data = pickle.dumps( obj )
    digest = hmac.new( UNIQUE_CODE, data, hashlib.blake2b ).hexdigest()
    return digest.encode() + separator.encode() + data

# Verifica o checksum de um byte-array 
def check_recv( digest : bytes, data : bytes, __debug : bool = False ) -> object:
    import secrets
    expected_digest = hmac.new( UNIQUE_CODE, data, hashlib.blake2b ).hexdigest()
    if not secrets.compare_digest( digest, expected_digest.encode() ):
        if __debug: 
            print('Invalid signature')
        return False 
    else: 
        if __debug:
            print( 'Right signatures')
        return pickle.loads( data )



# 1º faz o encode do obj Dummy 
data = encode_object( txt )
# 2º Cria um arquivo binário 
with open('temp.txt', 'wb') as output:
    # 3º salva os bytes no arquivo 
    output.write( data )

# ---------------------------------------------------------------------#

# 4º Outra aplicação pode abrir o arquivo binário 
with open('temp.txt', 'rb') as file:
    # 5º Pegar a chave de integridade Checksum   
    digest = file.readline()[:-1]
    # 6º Ler os dados 
    data = file.readline()
# 7º Verifica se os dados batem com o checksum recebido 
data = check_recv( digest, data, True)

# 8º Pode usar o objeto normalmente 
data.__str__() 
