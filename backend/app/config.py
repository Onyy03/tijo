class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///miniblik.db"

    API_TITLE = "MiniBlik API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_JSON_PATH = "openapi.json"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/"
    API_SPEC_OPTIONS = {
        "info": {
            "description": (
                "API symulatora płatności BLIK. Aplikacja bankowa generuje kod "
                "(`POST /api/accounts/{account_id}/blik-codes`), terminal sklepu tworzy nim "
                "płatność (`POST /api/payments`), a aplikacja bankowa ją zatwierdza "
                "lub odrzuca.\n\n"
                'Kwoty są przesyłane jako tekst z dwoma miejscami po przecinku, np. `"25.00"`. '
                'Daty są w UTC. Błędy mają postać `{"code": ..., "message": ...}`, '
                "a błędy walidacji (400) dodatkowo pole `errors`."
            )
        }
    }


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
