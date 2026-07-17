fastapi-template/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── exception.py
│   │   ├── dependency.py
│   │   └── constants.py
│   │
│   ├── common/
│   │   ├── base_model.py
│   │   ├── base_schema.py
│   │   ├── base_repository.py
│   │   ├── base_service.py
│   │   ├── pagination.py
│   │   ├── response.py
│   │   └── utils.py
│   │
│   ├── features/
│   │   ├── auth/
│   │   └── users/
│   │       ├── schema.py
│   │       ├── repository.py
│   │       ├── service.py
│   │       └── router.py
│   │
│   ├── middleware/
│   │
│   ├── main.py
│   └── router.py
│
├── alembic/
├── tests/
├── scripts/
├── docker/
│
├── .env
├── .env.example
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── Dockerfile
└── README.md
