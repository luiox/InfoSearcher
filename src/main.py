from src.email_mod.data_parser import DataParser
from src.email_mod.email_163 import EmailUtil


if __name__ == '__main__':
    # 授权码 ZWUXENDBVAWOHIZI
    e = EmailUtil('canrad7@163.com', 'ZWUXENDBVAWOHIZI')
    e.login()
    e.do()
    p = DataParser()
    p.parse()
