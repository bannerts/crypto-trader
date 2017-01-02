#
#  Digest Class Relations
#	string -> utf-8 -> binary <-> hex <-> hex_bin  
#	B58 <-> int <-> hex
#   Binaries formed from hex cannot usually be decoded into unicode with utf-8
#	Canonical Form: binary  

import binascii

class Digest:
	def __init__(self, value, in_hex = False):
	# value = text | hex | binary | integer | B58 
		self.value = value
		self.in_hex = in_hex
		(self.bin, self.hex) = self.calc_digest()
		self.size = (len(self.hex) + 1) // 2 
		self.num = int(self.hex, 16)

			
	def calc_digest(self, value = None, hex_bin = False):
		# default to self values
		if value == None:
			value = self.value
			in_hex = self.in_hex	
		if isinstance(value, type(b'ab')):
			if in_hex:
				val = value.lower()
				if val[0:2] == b'0x':
					val = val[2:]
				return (binascii.unhexlify(val), val.decode('utf-8'))
			else:
				return (value, binascii.hexlify(value).decode('utf-8'))
		elif isinstance(value, type('abc')):
			if in_hex:
				val = value.lower()
				if val[0:2] == '0x':
					val = val[2:]
				return (bytes.fromhex(val), val)
			else:
				val = value.encode('utf-8')
				return (val, binascii.hexlify(val).decode('utf-8'))		
		elif isinstance(value, type(12)):
			val = hex(value)[2:]
			return (bytes.fromhex(val), val)
		else:
			print("ERROR: Invalid input to Digest Class binary function")
			return (None, None)

	
			
def clean( text ):
	var = "".join(text.lower().split())
	return var
			
			
			
