'''from Crypto.Hash import SHA256
h = SHA256.new()
text = b'Hello World! SHA256 is a hash function with an output size of 256 bits. '
h.update(text)
text = b'It is member of the SHA-2 family of hash functions.'
h.update(text)
print(h.hexdigest()) # equivalent to print(h.digest().hex())
print(h.digest())'''
'''
example:	using	HMAC	with SHA256
– create	a	HMAC	object	by	calling	HMAC.new()	with	the	MAC	key	and	the	
hash	function	to	use	as	input	parameters
– call	update()	to	process	an	input	chunk	of	arbitrary	size	
– call	digest()	to	close	down	processing	and	to	produce	the	HMAC	value
– or	call	hexdigest()	to	produce	the	HMAC	value	in	hex	format'''


from Crypto.Hash import HMAC, SHA256
mackey = b'yoursecretMACkey'
mac = HMAC.new(mackey, digestmod=SHA256)
msg = b'Hello World! HMAC is a keyed hash function. '
mac.update(msg)
msg = b'This example uses the SHA256 hash function. '
mac.update(msg)
msg = b'However, you can change this and use another hash function too.'
mac.update(msg)
print(mac.hexdigest()) # equivalent to print(mac.digest().hex())
print(mac.digest())
