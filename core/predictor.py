import nltk
from nltk.corpus import words
import re

class Predictor:
    def __init__(self):
        try:
            self.word_list = words.words()
        except LookupError:
            print("Downloading NLTK words corpus...")
            nltk.download('words', quiet=True)
            self.word_list = words.words()
            
        # Convert to lowercase and remove very short words or duplicates
        self.word_list = list(set([w.lower() for w in self.word_list if len(w) > 1]))
        self.word_list.sort(key=len)
        
        # Hardcode extremely common words for priority
        self.common_words = ["the", "and", "you", "that", "was", "for", "are", "with", "his", "they", "this", "have", "from"]

    def predict(self, prefix, num_predictions=3):
        """Standard prefix prediction (fallback)"""
        prefix = prefix.lower()
        if not prefix:
            return ["the", "and", "you"]
            
        predictions = []
        for word in self.common_words:
            if word.startswith(prefix) and word not in predictions:
                predictions.append(word)
                if len(predictions) == num_predictions:
                    return predictions

        for word in self.word_list:
            if word.startswith(prefix) and word not in predictions:
                predictions.append(word)
                if len(predictions) == num_predictions:
                    break
        return predictions

    def decode_swype(self, sequence, num_predictions=3):
        """
        AI Swype Decoder: Takes a messy sequence like 'helo' 
        and finds matching words like 'hello' using regex pattern matching.
        """
        sequence = sequence.lower()
        if len(sequence) < 2:
            return self.predict(sequence, num_predictions)
            
        # Build wildcard regex: 'helo' -> '^h.*e.*l.*o$'
        pattern = "^" + sequence[0] + ".*" + ".*".join(list(sequence[1:-1])) + ".*" + sequence[-1] + "$"
        if len(sequence) == 2:
             pattern = "^" + sequence[0] + ".*" + sequence[1] + "$"
             
        try:
            regex = re.compile(pattern)
        except re.error:
            return []
            
        predictions = []
        
        # First check common words
        for word in self.common_words:
            if regex.match(word) and word not in predictions:
                predictions.append(word)
                if len(predictions) == num_predictions:
                    return predictions

        # Check full dictionary
        for word in self.word_list:
            if regex.match(word) and word not in predictions:
                predictions.append(word)
                if len(predictions) == num_predictions:
                    break
                    
        # Fallback to standard prefix if Swype fails
        if not predictions:
            return self.predict(sequence, num_predictions)
            
        return predictions
