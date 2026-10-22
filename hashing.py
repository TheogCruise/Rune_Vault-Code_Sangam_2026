import hashlib

class HashBlock:

    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()       #Call object.hash to get the hash of the object

    def calculate_hash(self):

        data_string = f"{self.timestamp}-{self.data}-{self.previous_hash}"
        h256 = hashlib.sha256()
        h256.update(data_string.encode("utf-8"))
        hashed_string = h256.hexdigest()

        return hashed_string

#TESTING /////////////

test1 = HashBlock("10.22.26:7.36", "This was the last data", "Test")
test2 = HashBlock("10.22.26:7.40", "This is some data", "This was the last data")

print(test1.hash)
print(test2.hash)