import chat
import config


def main():
    deepseek = chat.chat(config.URL, config.MODEL, config.API_KEY, config.context_path)
    print("1")
    print(deepseek.ask("привет, Андрей. Как погулял сегодня?"))
    print("2")
    print(deepseek.ask("Нормально, а ты как?"))
    print("3")
    print(deepseek.ask("Антон, что думаешь о vibe cding?"))



if __name__=="__main__":
    main()