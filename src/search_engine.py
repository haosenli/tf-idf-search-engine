from src.file import File
from operator import itemgetter
import math
import os
import re


class SearchEngine:
    """SearchEngine provides a searching function for a corpus of files.
    
    Attributes:
        index: A dict of words as keys and list of Files as values.
        size: An int number of files used by SearchEngine.
    """

    def __init__(self, dir_path: str) -> None:
        """Constructs a SearchEngine.
        
        Args:
            dir_path: A str directory path.
            
        Returns:
            None.
        """
        files = os.listdir(dir_path)
        self.index: dict[str, list[File]] = {}
        self.size: int = len(files)
        # build File objects and index
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            file = File(file_path)
            for word in file.get_words():
                if word not in self.index.keys():
                    self.index[word] = []
                self.index[word].append(file)

    def search(self, query: str) -> list[str]:
        """Return a list of str file paths sorted by relevancy.
        
        Args:
            query: A str query to search from.
            
        Returns:
            A list of sorted file paths, from highest to lowest relevance.
        """
        relevance = {}
        for term in query.split():
            term = re.sub(r'\W+', '', term.lower())
            # skip if word does not exist
            if term not in self.index:
                continue
            files_list = self.index[term]
            for file in files_list:
                path = file.get_path()
                if path not in relevance.keys():
                    relevance[path] = 0
                relevance[path] += file.term_frequency(term) * \
                    self._calculate_idf(term)

        rel_list = sorted(relevance.items(), key=itemgetter(1), reverse=True)
        return [rel[0] for rel in rel_list]

    def _calculate_idf(self, word: str):
        """Calculates the inverse document frequency of a word.
        
        Args:
            word: A str word.
        
        Returns:
            Returns a float inverse document frequency for the word.
        """
        if word not in self.index:
            return 0
        return math.log(self.size / len(self.index[word]))