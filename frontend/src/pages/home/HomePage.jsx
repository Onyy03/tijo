import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { api } from '../../api.js'
import Icon from '../../components/Icon.jsx'
import { formatInitials, formatMoney, formatPhone } from '../../format.js'
import './home.css'

function HomePage() {
  const [accounts, setAccounts] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .listAccounts()
      .then(setAccounts)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="home">
      <section className="home__half home__half--bank" aria-labelledby="home-bank-title">
        <p className="home__brand">
          <Icon name="bank" size={22} />
          MiniBank
        </p>
        <h1 id="home-bank-title" className="home__title">
          Zaloguj się do bankowości
        </h1>
        <p className="home__lead">
          Wybierz klienta. Każde konto ma własny adres, np. <span className="mono">/konto/1</span>.
        </p>
        <ul className="home-accounts">
          {accounts.map((account) => (
            <li key={account.id}>
              <Link className="home-account" to={`/konto/${account.id}`}>
                <span className="home-account__avatar" aria-hidden="true">
                  {formatInitials(account.owner_name)}
                </span>
                <span className="home-account__who">
                  <strong>{account.owner_name}</strong>
                  <span className="mono">{formatPhone(account.phone_number)}</span>
                </span>
                <span className="home-account__balance mono">{formatMoney(account.balance)}</span>
                <Icon name="arrowRight" size={18} />
              </Link>
            </li>
          ))}
        </ul>
        {error && <p className="notice notice--error">{error}</p>}
      </section>

      <section className="home__half home__half--shop" aria-labelledby="home-shop-title">
        <p className="home__brand home__brand--shop">
          <span className="home__shop-mark" aria-hidden="true">
            K
          </span>
          Delikatesy Kłos
        </p>
        <h2 id="home-shop-title" className="home__title home__title--serif">
          Zrób zakupy i zapłać <span className="home__nowrap">BLIK-iem</span>
        </h2>
        <p className="home__lead">
          Sklep internetowy czeka na kod BLIK wygenerowany w bankowości. Adres sklepu to{' '}
          <span className="mono">/sklep</span>.
        </p>
        <Link className="home__shop-link" to="/sklep">
          Przejdź do sklepu
          <Icon name="arrowRight" size={18} />
        </Link>
        <p className="home__tip">
          Otwórz konto i sklep w dwóch oknach obok siebie, tak jak telefon i komputer przy
          prawdziwej płatności.
        </p>
      </section>
    </div>
  )
}

export default HomePage
