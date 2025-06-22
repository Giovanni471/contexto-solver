import requests
import random
from openai import OpenAI
from wonderwords import RandomWord
import time

key = "YOUR_API_KEY"

checked_words: dict[str, int] = {} #Check the words that are already been seen
checked_words_string: str = ''
nearest_15_words: dict[str, int] = {} #The 5 best words

best_word: tuple[str, int] = tuple()

r = RandomWord()
client = OpenAI(api_key = key)


def get_word_gpt() -> str:
    """Return the word from ollama"""
    global nearest_15_words, checked_words_string

    table_of_nearest = ''

    for k, v in nearest_15_words.items():
        table_of_nearest += f'{k}-{v} \n '

    prompt = f"""
    Task: Generate Semantically Similar Words

        You will receive two inputs and must generate a list of semantically similar words based on specific criteria.
        
        Input 1 - Inspiration Table: A table with 2 columns:
        
        Column 1: words - These are your inspiration words
        Column 2: number - Similarity indices (0-10 scale)
        Numbers closer to 0 = Generate words VERY similar to the inspiration word
        Input 2 - Exclusion List: A list of words that you MUST NOT include in your output.
        
        Instructions:
        
        For each word in the inspiration table, generate semantically similar alternatives
        The similarity level should correspond to the number value:
        0-20: Near synonyms, very close meanings
        20-100: Related concepts, same domain
        100-300: Loosely connected, broader associations
        300-1000: Distant but conceptually linked
        1000+: Not linked at all
        NEVER include any word from the exclusion list
        Generate 3-5 alternatives per inspiration word
        Ensure all generated words are real, valid terms
        Output Format: Return ONLY a comma-separated list of words, like this: word1, word2, word3, word4, word5, 
        DO NOT Return anything else only a list separated by commas. 
        Input 1: 
        { table_of_nearest }

        Input 2: 
        {checked_words_string}
        """

    response = client.responses.create(
    model="gpt-4.1-mini-2025-04-14",
    input=prompt
    )

    return_word = response.output_text

    if "\"" in return_word:
        return_word.replace("\"", "")

    return return_word.lower().strip()

def get_random_words() -> list[str]:
    """Return a random word from dictionary"""
    global r
    return r.random_words(20)

def get_words() -> list[str]:
    """Return the list of words to check"""
    global nearest_15_words, checked_words_string

    if len(nearest_15_words) < 15:
        return get_random_words()
    
    return get_word_gpt().split(',')
    

def execute(game_number: int) -> None:
    """Return the winning string"""
    start_time = time.time()

    print(f"Playing game N.{game_number}! ")
    global checked_words, checked_words_string, nearest_15_words, best_word

    url = f'https://api.contexto.me/machado/en/game/{game_number}'

    distance = float('inf')
    while distance > 0:
        
        # get words
        word_list = get_words()

        # check words       
        print(f"Processing {len(word_list)} words...")
        try:
            for word in word_list:
                distance = min(check_words(url=url, word=word.strip()), distance)

                if distance == 0:
                    print(f"Word found! {word}, for the game N. {game_number}, in {((time.time() - start_time) * 1000) / 60:.2f} minutes")
                    return 
        except Exception as ex:
            print(ex)
        
        print(f"Best word till now: {best_word[0]}, Distance: {best_word[1] + 1}")
    
def check_words(url: str, word: str) -> int:
    """Return the min distance found"""
    global checked_words, checked_words_string, best_word

    if word in checked_words:
        return 10000

    url_word = f'{url}/{word}'
    response = requests.get(url=url_word)

    if response.status_code == 200:
        response_json = response.json()

        distance = response_json['distance']
        lemma = response_json['lemma']

        if distance == 0:
            return 0

        if not checked_words.get(lemma):
            checked_words_string += f'{lemma},'

        checked_words[lemma] = distance

        if best_word:
            if best_word[1] > distance:
                best_word = (lemma, distance)
        else:
            best_word = (lemma, distance)

        check_top_15(lemma, distance)

        return distance
    else:
        return 10000

def check_top_15(word: str, distance: int) -> None:
    """Check and modify the dict to have always the best 5 words inside of it"""
    global nearest_15_words
    
    if distance > 3500:
        return 
    
    if len(nearest_15_words) < 15:
        nearest_15_words[word] = distance
        return
    
    nearest_15_words = dict(sorted(nearest_15_words.items(), key= lambda x: x[1], reverse= True))

    for k, v in nearest_15_words.items():
        if v > distance:
            del nearest_15_words[k]

            nearest_15_words[word] = distance
            return

def clean_values() -> None:
    global nearest_15_words, checked_words, checked_words_string, best_word
    
    nearest_15_words = {}
    checked_words = {}
    checked_words_string = ''
    best_word = ()

def main() -> None:
    while True:
        try:
            clean_values()
            game_number = input("What game you want to play? (Leave blank for random) ")

            if(game_number):
                game_number = int(game_number)
            else:
                game_number = random.randint(0, 1006)

            execute(game_number)
            break
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    main()
