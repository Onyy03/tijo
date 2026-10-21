import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { formatMoney } from '../format.js'

function AccountSummary({ accountId, version }) {
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    api
      .getSummary(accountId)
      .then((data) => active && setSummary(data))
      .catch((err) => active && setError(err.message))
    return () => {
      active = false
    }
  }, [accountId, version])

  if (summary === null) {
    return error ? (
      <p className="message message--error" role="alert">
        {error}
      </p>
    ) : null
  }

  return (
    <dl className="summary" data-testid="account-summary">
      <div className="summary__item">
        <dt>Wpływy</dt>
        <dd className="summary__value summary__value--in">
          {formatMoney(summary.total_incoming)}
        </dd>
      </div>
      <div className="summary__item">
        <dt>Wydatki</dt>
        <dd className="summary__value summary__value--out">
          {formatMoney(summary.total_outgoing)}
        </dd>
      </div>
      <div className="summary__item">
        <dt>Operacje</dt>
        <dd className="summary__value">{summary.operations_count}</dd>
      </div>
    </dl>
  )
}

export default AccountSummary
