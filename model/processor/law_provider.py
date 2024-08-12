import pandas as pd
import re

class LawTxetPreProcessor():
    
    def __init__(self, law_texts: list) -> None:
        self._law_texets = law_texts
        self._law_name_df = pd.DataFrame(columns=["law_index", "law_name"])
        self._madeh_df = pd.DataFrame(columns=["law_index", "madeh_index", "madeh_text"])
        self._is_df = False
        
    def build_df(self):
        title_list = []
        madeh_list = []
        madeh_index = []
        law_index = []
        counter = 0
        for text in self._law_texets:
            title = self.title_extractor(text)
            title_list.append(title)
            temp_madeh_list = self.madeh_extractor(text, title == "قانون اساسی جمهوری اسلامی ایران")
            law_index.extend([counter for i in temp_madeh_list])
            madeh_index.extend([i+1  for i in range(len(temp_madeh_list))])
            madeh_list.extend(temp_madeh_list)
            counter += 1
        law_index_list = [i for i in range(counter)]
        self._madeh_df = pd.DataFrame({"law_index": law_index,
                                    "madeh_index": madeh_index,
                                    "madeh_text": madeh_list})
        self._law_name_df = pd.DataFrame({"law_index": law_index_list,
                                          "law_name": title_list})
        
    def title_extractor(self, law_text: str) -> str:
        first_newline_index = law_text.find('\n')
        return law_text[:first_newline_index]
    
    def madeh_extractor(self, law_text: str, is_asl:False)-> list:
        result = []
        pattern = r"(^.{0,1}اصل )" if is_asl else r"(^.{0,1}ماده)"
        removed_regex = r"❯.*\n"
        notvalid_pattern = r"(^.{0,1}ماده.*مکرر\n)"
        cleaned_text = re.sub(removed_regex, "", law_text)
        matches = re.finditer(pattern, cleaned_text, flags=re.MULTILINE)
        not_valid_matches = re.finditer(notvalid_pattern, cleaned_text, flags=re.MULTILINE)
        indices = [match.start() for match in matches]
        not_valid_indices = [match.start() for match in not_valid_matches]
        valid_indices = [item for item in indices if item not in not_valid_indices]
        for i in range(len(valid_indices)):
            start = valid_indices[i]
            if i != len(valid_indices)-1:
                end = valid_indices[i+1]
                result.append(cleaned_text[start:end])
            else:
                result.append(cleaned_text[start:])
        return result
    
    
    def get_df(self) -> pd.DataFrame:
        if not self._is_df:
            self.build_df()
        return self._law_name_df, self._madeh_df 