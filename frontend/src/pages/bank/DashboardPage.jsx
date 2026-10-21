import { useEffect, useState } from 'react'
import { Link, useOutletContext } from 'react-router'
import { api } from '../../api.js'
import { formatMoney } from '../../format.js'
import OperationList from './OperationList.jsx'

const RECENT_OPERATIONS = 5

function DashboardPage() {
  const { account, version } = useOutletContext()
  const [summary, setSummary] = useState(null)
  const [recent, setRecent] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    Promise.all([api.getSummary(account.id), api.listHistory(account.id)])
      .then(([accountSummary, history]) => {
        if (active) {
          setSummary(accountSummary)
          setRecent(history.slice(0, RECENT_OPERATIONS))
        }
      })
      .catch((err) => active && setError(err.message))
    return () => {
      active = false
    }
  }, [account.id, version])

  return (
    <>
      <header className="bank-page-header">
        <p className="bank-page-header__eyebrow">Rachunek osobisty</p>
        <h1>Pulpit</h1>
      </header>

      <section className="balance-card">
        <span className="balance-card__label">Dostępne środki</span>
        <strong className="balance-card__amount mono" data-testid="balance">
          {formatMoney(account.balance)}
        </strong>
        <div className="balance-card__actions">
          <Link className="btn btn--on-dark" to="blik">
            Kod BLIK
          </Link>
          <Link className="btn btn--on-dark" to="przelew">
            Przelew na telefon
          </Link>
        </div>
      </section>

      {summary && (
        <dl className="stats" data-testid="account-summary">
          <div className="stat">
            <dt>Wpływy</dt>
            <dd className="stat__value stat__value--in mono">
              {formatMoney(summary.total_incoming)}
            </dd>
          </div>
          <div className="stat">
            <dt>Wydatki</dt>
            <dd className="stat__value stat__value--out mono">
              {formatMoney(summary.total_outgoing)}
            </dd>
          </div>
          <div className="stat">
            <dt>Operacje</dt>
            <dd className="stat__value mono">{summary.operations_count}</dd>
          </div>
        </dl>
      )}

      <section className="bank-card">
        <div className="bank-card__header">
          <h2 className="bank-card__title">Ostatnie operacje</h2>
          <Link className="bank-card__link" to="historia">
            Cała historia
          </Link>
        </div>
        <OperationList entries={recent} />
      </section>

      {error && <p className="notice notice--error">{error}</p>}
    </>
  )
}

export default DashboardPage
