import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { formatDateTime, formatMoney } from '../format.js'

const ENTRY_TYPE_LABELS = {
  PAYMENT: 'Płatność BLIK',
  TRANSFER_OUT: 'Przelew wychodzący',
  TRANSFER_IN: 'Przelew przychodzący',
}

function History({ accountId, version }) {
  const [entries, setEntries] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    api
      .listHistory(accountId)
      .then((list) => active && setEntries(list))
      .catch((err) => active && setError(err.message))
    return () => {
      active = false
    }
  }, [accountId, version])

  return (
    <div className="history">
      <h3 className="section-title">Historia operacji</h3>
      {entries.length === 0 ? (
        <p className="history__empty">Brak operacji na koncie</p>
      ) : (
        <table className="history__table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Opis</th>
              <th className="history__amount">Kwota</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry) => (
              <tr key={entry.id} data-testid="history-entry">
                <td>{formatDateTime(entry.created_at)}</td>
                <td>
                  <span className="history__type">{ENTRY_TYPE_LABELS[entry.type]}</span>
                  {entry.description}
                </td>
                <td
                  className={`history__amount history__amount--${
                    Number(entry.amount) < 0 ? 'out' : 'in'
                  }`}
                >
                  {formatMoney(entry.amount)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

export default History
