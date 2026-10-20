import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { formatMoney } from '../format.js'
import BlikCodeCard from './BlikCodeCard.jsx'

function BankApp() {
  const [accounts, setAccounts] = useState([])
  const [accountId, setAccountId] = useState(null)
  const [account, setAccount] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .listAccounts()
      .then((list) => {
        setAccounts(list)
        setAccountId(list[0]?.id ?? null)
      })
      .catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    if (accountId === null) {
      return undefined
    }
    let active = true
    api
      .getAccount(accountId)
      .then((data) => {
        if (active) {
          setAccount(data)
          setError('')
        }
      })
      .catch((err) => active && setError(err.message))
    return () => {
      active = false
    }
  }, [accountId])

  return (
    <section className="panel" aria-labelledby="bank-app-title">
      <h2 id="bank-app-title" className="panel__title">
        Aplikacja bankowa
      </h2>

      <label className="field">
        <span className="field__label">Konto</span>
        <select
          value={accountId ?? ''}
          onChange={(event) => setAccountId(Number(event.target.value))}
        >
          {accounts.map((item) => (
            <option key={item.id} value={item.id}>
              {item.owner_name} ({item.phone_number})
            </option>
          ))}
        </select>
      </label>

      {account && (
        <div className="balance">
          <span className="balance__label">Dostępne środki</span>
          <strong className="balance__amount" data-testid="balance">
            {formatMoney(account.balance)}
          </strong>
        </div>
      )}

      {accountId !== null && <BlikCodeCard key={accountId} accountId={accountId} />}

      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </section>
  )
}

export default BankApp
