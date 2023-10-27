import os


class DataParser:
    def parse(self):
        directory = 'email_context'
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    # 将每个文件解析
                    self.parse_file(content)

    def parse_file(self, content):
        print(content)


