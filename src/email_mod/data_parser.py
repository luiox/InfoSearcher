import csv
import os
import re


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
        transactions = re.findall(r'(\d{8})\s+(\d{8})\s+(\d{4})\s+(.*?)\s+(.*?)\s+([\d.-]+/CNY)\s+([\d.-]+/CNY)', content)

        # 写入CSV文件
        with open('detail.csv', 'w', newline='', encoding='utf-16') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(
                ['交易日', '入账日期', '卡号后四位', '交易摘要', '交易地点', '交易金额/币种', '入账金额/币种'])
            for transaction in transactions:
                csvwriter.writerow(transaction)


