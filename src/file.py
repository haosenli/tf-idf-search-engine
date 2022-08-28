import re


class File:
    """
    The File class provides functions for document processing.
    
    Attributes:
        path: A str path to a file.
        words: A dict of normalized words and its 
            term frequency in the file.
    """
    def __init__(self, path: str) -> None:
        """Constructs a File object.
        
        Args:
            path: A str path to a file.
        
        Returns:
            None.
        """
        self.path = path
        self.words = self._process_file(path)

    def term_frequency(self, word: str) -> float:
        """Returns the term frequency for a word.
        
        Args:
            word: A case and punctuation insensitive word.
        
        Returns:
            A float term frequency for the given word, returns 0
            if word does not exist in document.
        """
        word = re.sub(r'\W+', '', word.lower())
        self.words.get(word, 0)

    def get_path(self) -> str:
        """Returns the str path of the document."""
        return self.path

    def get_words(self):
        """Returns a set-like for all normalized words stored in File."""
        return self.words.keys()

    def _process_file(self, path: str) -> dict:
        """Returns a dictionary containing the normalized words in
        the file and its term-frequencies from a given str path."""
        with open(path) as f:
            lines = f.readlines()
            
        words = {}
        # process file
        for line in lines:
            for word in line.split():
                # normalize words
                word = re.sub(r'\W+', '', word.lower())
                # add words to dictionary
                if word not in words:
                    words[word] = 0
                words[word] += 1

        # compute term frequency for each word
        for key, value in words.items():
            words[key] = value / len(words)
        return words