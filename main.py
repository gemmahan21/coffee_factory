from dotenv import load_dotenv

from src.database import Database


def main():
    load_dotenv()

    try:
        with Database() as db:
            pass

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
