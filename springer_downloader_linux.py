import os
import time
import codecs
import requests
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s-%(message)s")


class SpringerDownloader:
    
    def __init__(self):
        self.df = [[i[0], i[1], i[2].split(";")[0], i[3]] for i in pd.read_excel("free_english_textbook.xlsx")[["Book Title", "Author", "Subject Classification", "OpenURL"]].values.tolist()]
        self.current_path = os.getcwd()
    
    def wget(self, url, save_path=None, rename=None):
        file_name = url[url.rfind("/")+1:]
        if not save_path:
            save_path = self.current_path
        if not rename:
            rename = file_name
        save_path = os.path.abspath(os.path.join(save_path, rename))
        logging.info("[wget]   downloading from {}".format(url))
        start = time.time()
        size = 0
        response = requests.get(url, stream=True)
        if response.headers.get("content-length") is not None:
            chunk_size = 128
            content_size = int(response.headers["content-length"])
            if not self.check_if_exists(save_path, content_size):
                if response.status_code == 200:
                    logging.info("[wget]   file size: %.2f MB" %(content_size / 1024 / 1024))
                    with codecs.open(save_path, "wb") as f:
                        for data in response.iter_content(chunk_size=chunk_size):
                            f.write(data)
                            size += len(data)
                end = time.time()
                logging.info("\n"+"[wget]   complete! cost: %.2fs."%(end-start))
                logging.info("[wget]   save at: %s\n" %save_path)
        else:
            logging.info("[wget]   failed to download from {}, this book is not free.".format(url))
        
    def mkdir(self, file_dir):
        file_dir = os.path.abspath(os.path.join(self.current_path, file_dir))
        os.makedirs(file_dir)
        logging.info("[mkdir]  create directory {}".format(file_dir))
        
    def check_if_exists(self, file_path, content_size):
        if not os.path.exists(file_path):
            return False
        else:
            if os.path.getsize(file_path) < content_size:
                return False
            else:
                return True
    
    def download(self):
        for _, i in enumerate(self.df):
            logging.info("Downloading 【{}】. \nCurrent #books: {}, total #books: {}".format(i[0], _ + 1, len(self.df)))
            file_name = i[0] + "|" + i[1] + ".pdf"
            file_name = file_name.replace("/", "_")
            classification_dir = os.path.abspath(os.path.join(self.current_path, i[2]))
            if not os.path.exists(classification_dir):
                self.mkdir(classification_dir)
            file_url = "https://link.springer.com/content/pdf/" + requests.get(i[3]).url.split("/")[-1] + ".pdf"
            self.wget(file_url, save_path=classification_dir, rename=file_name)

            
if __name__ == "__main__":
    sd = SpringerDownloader()
    sd.download()
