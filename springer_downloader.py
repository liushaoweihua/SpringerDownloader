import os
import time
import codecs
import requests
import pandas as pd


class SpringerDownloader:
    
    def __init__(self):
        self.df = [[i[0], i[1].split(";")[0], i[2]] for i in pd.read_excel("free_english_textbook.xlsx")[["Book Title", "Subject Classification", "OpenURL"]].values.tolist()]
        self.current_path = os.getcwd()
    
    def wget(self, url, save_path=None, rename=None):
        file_name = url[url.rfind("/")+1:]
        if not save_path:
            save_path = self.current_path
        if not rename:
            rename = file_name
        save_path = os.path.abspath(os.path.join(save_path, rename))
        try:
            print("[wget]   downloading from {}".format(url))
            start = time.time()
            size = 0
            response = requests.get(url, stream=True)
            chunk_size = 10240
            content_size = int(response.headers["content-length"])
            if response.status_code == 200:
                print("[wget]   file size: %.2f MB" %(content_size / 1024 / 1024))
                with codecs.open(save_path, "wb") as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        size += len(data)
                        print("\r"+"[wget]   %s%.2f%%"
                              %(">"*int(size*50/content_size), float(size/content_size*100)), end="")
            end = time.time()
            print("\n"+"[wget]   complete! cost: %.2fs."%(end-start))
            print("[wget]   save at: %s\n" %save_path)
        except Exception:
            print("[wget]   failed to download from {}, this book is not free.".format(url))
        
    def mkdir(self, file_dir):
        file_dir = os.path.abspath(os.path.join(self.current_path, file_dir))
        os.makedirs(file_dir)
        print("[mkdir]  create directory {}".format(file_dir))
    
    def download(self):
        for _, i in enumerate(self.df):
            print("Downloading 【{}】. \nCurrent #books: {}, total #books: {}".format(i[0], _ + 1, len(self.df)))
            file_name = i[0] + ".pdf"
            classification_dir = os.path.abspath(os.path.join(self.current_path, i[1]))
            if not os.path.exists(classification_dir):
                self.mkdir(classification_dir)
            file_url = "https://link.springer.com/content/pdf/" + requests.get(i[2]).url.split("/")[-1] + ".pdf"
            self.wget(file_url, save_path=classification_dir, rename=file_name)
            
            
if __name__ == "__main__":
    sd = SpringerDownloader()
    sd.download()
