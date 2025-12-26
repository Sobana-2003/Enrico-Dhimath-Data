


def rephrase_question(question, category_values_dict):
    """Removes generic words from a given statement."""
    # words = statement.lower()  # Tokenize words (removes punctuation)
    # words = re.findall(r'\w+', statement.lower())
    # words = re.findall(r"\w+", statement.lower())
    question = question.replace("?", " ?")
    question = question.replace(".", " .")
    words = question.split(" ")
    rephrased_question = "" 
    multiple_options = False
    multiple_option_word = []
    num_of_mult_words = 0
    for word in words:
        if word in category_values_dict.keys():
            cols = len(category_values_dict[word])
            if cols > 1:    
                # with st.form(key="value_selection", border = False):    
                filtered_words = f"selected_db_column_{num_of_mult_words} = '{word}'"
                num_of_mult_words = num_of_mult_words + 1
                multiple_options = True
                multiple_option_word.append(word)
            else:
                filtered_words = f"{category_values_dict[word][0]} = '{word}'"
        else:
            filtered_words = word
        rephrased_question = rephrased_question + " " + filtered_words

    # st.write(rephrased_question)
    return rephrased_question, multiple_options, category_values_dict, multiple_option_word, num_of_mult_words
