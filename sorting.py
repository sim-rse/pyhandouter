import re


def natural_key(s): #used for sorting the file names correctly (the "human way") because else python would just look at the first numbers it encounters: you'd get something like ["file_1", "file_10", "file_2"] 
    # Splits the string into text and number chunks
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]