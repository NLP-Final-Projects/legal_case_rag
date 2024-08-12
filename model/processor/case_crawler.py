import requests
from bs4 import BeautifulSoup
import os
import warnings
from tqdm import tqdm

class Crawler:
    # This is used for vote separating when list of vote concatenation in string 
    vote_splitter = " |split| " 

    def __init__(self, base_url: str, list_url:str , 
                 base_vote_url:str , models_path: str , result_path:str):
        if base_url == "":
            self.base_url ="https://ara.jri.ac.ir/"
        else:
            self.base_url = base_url

        if list_url == "":
            self.list_url ="https://ara.jri.ac.ir/Judge/Index"
        else:
            self.list_url = list_url

        if base_vote_url == "":
            self.base_vote_url ="https://ara.jri.ac.ir/Judge/Text/"
        else:
            self.base_vote_url = base_vote_url
        
        if models_path == "":
            self.models_path ="Models/"
        else:
            self.models_path = models_path    
        self.pos_model_path = os.path.join(models_path, "postagger.model")
        self.chunker_path = os.path.join(models_path, "chunker.model")

        if result_path == "":
            self.result_path = "Resource/"
        else:
            self.result_path = result_path

        self.merges_vote_path = os.path.join(result_path, 'merged_vote.txt')
        self.clean_vote_path = os.path.join(result_path, 'clean_vote.txt')
        self.clean_vote_path_csv = os.path.join(result_path, 'clean_vote.csv')
        self.selected_vote_path = os.path.join(result_path, 'selected_vote.txt')
        self.law_list_path = os.path.join(result_path, 'law_list.txt')
        self.law_clean_list_path = os.path.join(result_path, 'law_clean_list.txt')
        self.vote_stop_path = os.path.join(result_path, "vote_stopwords.txt")
        self.law_stop_path = os.path.join(result_path, "law_stopwords.txt")

    @staticmethod
    def check_valid_vote(html_soup: BeautifulSoup) -> bool:
        # Extract title for detection of non-valid vote
        h1_element = html_soup.find('h1', class_='Title3D')
        if h1_element is None:
            return False
        span_text = h1_element.find('span').text  # Text within the <span> tag
        full_text = h1_element.text  # Full text within the <h1> element
        text_after_span = full_text.split(span_text)[-1].strip()  # Extract text after the </span> tag
        return len(text_after_span) > 0

    @staticmethod
    def html_data_extractor(html_soup: BeautifulSoup, vote_splitter: str) -> str:
        vote_text = html_soup.find('div', id='treeText', class_='BackText')
        title = html_soup.find('h1', class_='Title3D')
        info = html_soup.find('td', valign="top", class_="font-size-small")
        # for separating each vote in file use vote_splitter
        vote_df = str(title) + str(info) + str(vote_text) + vote_splitter
        return vote_df

    def vote_crawler(self, start: int, end: int, separator: int):
        counter = 0  # For counting right votes crawled
        result_list = []
        warnings.filterwarnings("ignore")
        # Loop for sending request to get each vote page
        for i in tqdm(range(start, end)):
            # Save every separator records gotten in .txt format
            if (counter % separator == 0 and counter > 0) or i == end - 1:
                text_file = open(os.path.join(self.result_path, f'vote{i}.txt'), "w", encoding='utf-8')
                text_file.write(''.join(result_list))
                text_file.close()
                result_list = []
            url = self.base_vote_url + f"{i}"
            response = requests.get(url, verify=False)
            # Change format for Persian text
            response.encoding = 'utf-8'
            resp_text = response.text
            html_soup = BeautifulSoup(resp_text, 'html.parser')
            if response.ok and self.check_valid_vote(html_soup):
                counter += 1
                vote_df = self.html_data_extractor(html_soup, self.vote_splitter)
                result_list.append(vote_df)

    def merge_out_txt(self) -> None:

        with open(self.result_path, 'w', encoding='utf-8') as outfile:
            for filename in os.listdir(self.merges_vote_path):
                if filename.startswith("vote") and filename.endswith('.txt'):  # Only merge vote .txt
                    with open(os.path.join(self.merges_vote_path, filename), 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())

if __name__ == "__main__":
    models_path = input("Enter the models path (initial value = https://ara.jri.ac.ir/): ")
    result_path = input("Enter the result path (initial value = https://ara.jri.ac.ir/Judge/Index): ")
    base_url = input("Enter the base URL (initial value = https://ara.jri.ac.ir/Judge/Text/): ")
    list_url = input("Enter the list URL (initial value = Models/ ): ")
    base_vote_url = input("Enter the base vote URL (initial value = Resource/ ): ")

    crawler_instance = Crawler(models_path=models_path, result_path=result_path, base_url=base_url, list_url=list_url, base_vote_url=base_vote_url)
    start = int(input("Enter the start value for vote crawling: "))
    end = int(input("Enter the end value for vote crawling: "))
    separator = int(input("Enter the separator value for vote crawling: "))

    crawler_instance.vote_crawler(start=start, end=end, separator=separator)
    crawler_instance.merge_out_txt()
