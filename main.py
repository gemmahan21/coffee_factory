from dotenv import load_dotenv

from src.database import Database

from src.repository import MaterialRepository
from src.service import QueryService
from src.dto import MaterialDto
from src.models import Material


def main():
    load_dotenv()

    try:
        with Database() as db:
            # material_repository = MaterialRepository(db)
            query_service = QueryService(db)

            # production = query_service.find_all_production()
            # print(production)
            production = query_service.find_product_by_production(1)
            print(production)

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
