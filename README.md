# MiniBlik – symulator płatności BLIK

Projekt zaliczeniowy z kursu **Testowanie i Jakość Oprogramowania**.

## Temat projektu

MiniBlik – symulator płatności kodem BLIK.

## Opis projektu

Aplikacja ma dwa panele, które działają obok siebie w przeglądarce:

- **Aplikacja bankowa**:
  - wybór konta i saldo,
  - generowanie 6-cyfrowego kodu BLIK ważnego 120 sekund,
  - zatwierdzanie i odrzucanie płatności,
  - przelew na numer telefonu,
  - historia operacji.
- **Terminal sklepu**: płatność kodem BLIK i podgląd jej statusu (oczekuje, zatwierdzona, odrzucona).

Przy pierwszym uruchomieniu tworzą się konta demonstracyjne:

| Właściciel | Telefon | Saldo |
|---|---|---|
| Jan Kowalski | 500100200 | 500,00 PLN |
| Anna Nowak | 600200300 | 1 500,00 PLN |
| Piotr Zieliński | 700300400 | 0,00 PLN |

## Uruchomienie projektu

Wymagania: Python 3.12+ i Node.js 22+.

Backend (API na porcie 5001):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app app run --port 5001
```

Frontend (w drugim terminalu):

```bash
cd frontend
npm install
npm run dev
```

| Adres | Co jest pod nim |
|---|---|
| http://localhost:5173 | aplikacja |
| http://localhost:5001/api/docs | dokumentacja API (Swagger UI) |

Baza SQLite leży w `backend/instance/miniblik.db`. Żeby wrócić do danych startowych, usuń ten plik
i uruchom backend ponownie.

## Testy

```bash
cd backend
pytest          # testy
ruff check .    # analiza statyczna (m.in. nieużywane importy)
```

```bash
cd frontend
npm run lint    # oxlint
```

## Technologie użyte w projekcie

- Backend: Python, Flask, Flask-SQLAlchemy (SQLite), flask-smorest (OpenAPI / Swagger UI)
- Frontend: React, Vite
- Testy i jakość: pytest, ruff, oxlint
