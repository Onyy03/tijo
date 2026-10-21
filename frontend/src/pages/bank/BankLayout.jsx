import { useCallback, useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useParams } from 'react-router'
import { api } from '../../api.js'
import Icon from '../../components/Icon.jsx'
import { formatInitials, formatPhone } from '../../format.js'
import PaymentConfirmation from './PaymentConfirmation.jsx'
import './bank.css'

const TABS = [
  { to: '', label: 'Pulpit', icon: 'dashboard', end: true },
  { to: 'blik', label: 'Kod BLIK', icon: 'blik' },
  { to: 'przelew', label: 'Przelew na telefon', icon: 'transfer' },
  { to: 'historia', label: 'Historia', icon: 'history' },
]

function BankLayout() {
  const { accountId } = useParams()
  const [account, setAccount] = useState(null)
  const [error, setError] = useState('')
  const [version, setVersion] = useState(0)
  // kept here, not in the BLIK tab, so the code survives switching tabs
  const [blikCode, setBlikCode] = useState(null)
  // pages call this after anything that changes the balance
  const refresh = useCallback(() => setVersion((current) => current + 1), [])

  useEffect(() => {
    let active = true
    api
      .getAccount(accountId)
      .then((data) => {
        if (active) {
          setAccount(data)
          setError('')
        }
      })
      .catch((err) => {
        if (active) {
          setAccount(null)
          setError(err.message)
        }
      })
    return () => {
      active = false
    }
  }, [accountId, version])

  if (account === null) {
    return (
      <div className="bank-state">
        {error ? (
          <>
            <p className="notice notice--error">{error}</p>
            <Link className="btn" to="/">
              Wróć do wyboru konta
            </Link>
          </>
        ) : (
          <p className="bank-state__loading">Wczytywanie rachunku…</p>
        )}
      </div>
    )
  }

  return (
    <div className="bank">
      <aside className="bank-sidebar">
        <Link className="bank-brand" to="/">
          <Icon name="bank" size={22} />
          <span>MiniBank</span>
        </Link>
        <nav className="bank-nav" aria-label="Zakładki bankowości">
          {TABS.map((tab) => (
            <NavLink key={tab.label} className="bank-nav__link" to={tab.to} end={tab.end}>
              <Icon name={tab.icon} />
              {tab.label}
            </NavLink>
          ))}
        </nav>
        <div className="bank-user">
          <span className="bank-user__avatar" aria-hidden="true">
            {formatInitials(account.owner_name)}
          </span>
          <span className="bank-user__details">
            <strong>{account.owner_name}</strong>
            <span className="mono">{formatPhone(account.phone_number)}</span>
          </span>
        </div>
        <Link className="bank-nav__link bank-nav__link--logout" to="/">
          <Icon name="logout" />
          Wyloguj
        </Link>
      </aside>
      <main className="bank-main" key={account.id}>
        <Outlet
          context={{
            account,
            refresh,
            version,
            blikCode: blikCode?.accountId === account.id ? blikCode : null,
            setBlikCode,
          }}
        />
      </main>
      <PaymentConfirmation
        key={account.id}
        accountId={account.id}
        // a BLIK code is single-use: once a payment arrives, the shown code is spent
        onPaymentArrived={() => setBlikCode((current) => current && { ...current, used: true })}
        onPaymentDecided={refresh}
      />
    </div>
  )
}

export default BankLayout
