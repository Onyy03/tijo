import { useEffect, useState } from 'react'
import { useOutletContext } from 'react-router'
import { api } from '../../api.js'
import OperationList from './OperationList.jsx'

const FILTERS = [
  { id: 'all', label: 'Wszystkie', matches: () => true },
  { id: 'incoming', label: 'Wpływy', matches: (entry) => Number(entry.amount) > 0 },
  { id: 'outgoing', label: 'Wydatki', matches: (entry) => Number(entry.amount) < 0 },
]

function HistoryPage() {
  const { account, version } = useOutletContext()
  const [entries, setEntries] = useState([])
  const [filterId, setFilterId] = useState('all')
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    api
      .listHistory(account.id)
      .then((history) => active && setEntries(history))
      .catch((err) => active && setError(err.message))
    return () => {
      active = false
    }
  }, [account.id, version])

  const filter = FILTERS.find((item) => item.id === filterId)

  return (
    <>
      <header className="bank-page-header">
        <p className="bank-page-header__eyebrow">Rachunek osobisty</p>
        <h1>Historia operacji</h1>
      </header>

      <section className="bank-card">
        <div className="segmented" role="group" aria-label="Rodzaj operacji">
          {FILTERS.map((item) => (
            <button
              key={item.id}
              type="button"
              className="segmented__option"
              aria-pressed={item.id === filterId}
              onClick={() => setFilterId(item.id)}
            >
              {item.label}
              <span className="segmented__count mono">{entries.filter(item.matches).length}</span>
            </button>
          ))}
        </div>
        <OperationList
          entries={entries.filter(filter.matches)}
          emptyText={
            filterId === 'all' ? 'Brak operacji na rachunku.' : 'Brak operacji tego rodzaju.'
          }
        />
        {error && <p className="notice notice--error">{error}</p>}
      </section>
    </>
  )
}

export default HistoryPage
