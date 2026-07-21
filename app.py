from dotenv import load_dotenv
from src.repository import Database, MaterialRepository


def main():
    load_dotenv()

    try:
        with Database() as db:
            material_repository = MaterialRepository(db)
            list = material_repository.find_all()
            print(list)

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
