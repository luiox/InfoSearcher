import requests


def download_pdf(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print("PDF文件已下载并保存为:", save_path)


url = "https://xxx.com/xxx.pdf"
save_path = "xxx.pdf"
download_pdf(url, save_path)
