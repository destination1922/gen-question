from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
DISTRIBUTION = env.str("DISTRIBUTION")
ADD = env.str("ADD")

START_TEXT = "Assalomu alaykum!\nBotimizga xush kelibsiz!"



def generate_numbers(array: list, n: int) -> list:
    questions = []
    i = 0
    while len(questions) * n - len(array) < 0:
        questions.append(array[i:i+n])
        i += n
    return questions