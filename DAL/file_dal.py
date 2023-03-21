class FileDAL:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, 'r') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return None

    def write(self, data):
        with open(self.filename, 'w') as file:
            file.write(data)
