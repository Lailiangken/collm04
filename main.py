from functions.autogen_functions import LLMFunction

def main():
    llm_func = LLMFunction()
    result = llm_func("How to implement a binary search tree in Python?")
    print(result)

if __name__ == "__main__":
    main()
