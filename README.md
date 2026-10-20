# MiniBlik – symulator płatności BLIK

[![CI](https://github.com/Onyy03/tijo/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Onyy03/tijo/actions/workflows/ci.yml)

## Nazwa kursu

Testowanie i Jakość Oprogramowania II. Akademia Tarnowska, Wydział Politechniczny, Katedra Informatyki,
rok 4, semestr zimowy 2026/2027.

## Autor

Norbert Armatys, nr indeksu 37664, grupa PT2

## Temat projektu

MiniBlik – symulator płatności kodem BLIK

## Opis projektu

MiniBlik odtwarza w uproszczeniu płatność kodem BLIK. Użytkownik generuje w aplikacji bankowej
6-cyfrowy kod, sprzedawca wpisuje go w terminalu razem z kwotą, a użytkownik zatwierdza albo odrzuca
płatność w aplikacji. Oprócz tego można wysłać przelew na numer telefonu i przejrzeć historię operacji.

Aplikacja ma dwa panele, które działają obok siebie w przeglądarce:

- **Aplikacja bankowa**:
  - wybór konta i saldo,
  - generowanie kodu BLIK z odliczaniem ważności,
  - zatwierdzanie i odrzucanie płatności,
  - przelew na numer telefonu,
  - historia operacji.
- **Terminal sklepu**: płatność kodem BLIK i podgląd jej statusu (oczekuje, zatwierdzona, odrzucona,
  czas minął).

### Reguły biznesowe

| ID | Reguła |
|---|---|
| R1 | Kod ma dokładnie 6 cyfr i jest losowany kryptograficznie bezpiecznym generatorem (`secrets`). |
| R2 | Kod jest ważny 120 sekund od wygenerowania. |
| R3 | Konto ma najwyżej jeden aktywny kod. Wygenerowanie nowego kodu anuluje poprzedni. |
| R4 | Kod jest jednorazowy. Po użyciu w terminalu nie da się nim zapłacić drugi raz. |
| R5 | Kwota musi być większa od zera, mieć najwyżej 2 miejsca po przecinku i nie przekraczać 5 000,00 PLN. |
| R6 | Płatność czeka na potwierdzenie najwyżej 120 sekund. Po tym czasie nie da się jej zatwierdzić. |
| R7 | Zatwierdzenie wymaga wystarczających środków. Przy ich braku saldo się nie zmienia, a płatność dalej czeka. |
| R8 | Zatwierdzić lub odrzucić można tylko płatność, która czeka na decyzję. |
| R9 | Przelew wymaga istniejącego odbiorcy i wystarczających środków. Nie można wysłać przelewu na własny numer. Kwota według R5. |
| R10 | Każda zmiana salda dodaje wpis do historii operacji. |

### Konta demonstracyjne

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
