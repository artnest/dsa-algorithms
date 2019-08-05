class RSADSA:
    def __init__(self, n):
        self.n = n

    def sign(self, hash_function, message, private):
        hash = int(hash_function(message).hexdigest(), 16)
        return {'message': message, 'signature': pow(hash, private, self.n)}

    def verify(self, hash_function, signature, public):
        message = signature['message']
        hash = int(hash_function(message).hexdigest(), 16)
        decrypted_hash = pow(signature['signature'], public, self.n)
        return decrypted_hash == hash
