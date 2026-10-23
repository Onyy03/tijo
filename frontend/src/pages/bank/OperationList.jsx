import Icon from '../../components/Icon.jsx'
import { formatDateTime, formatMoney } from '../../format.js'

const TYPE_LABELS = {
  PAYMENT: 'Płatność BLIK',
  TRANSFER_OUT: 'Przelew na telefon',
  TRANSFER_IN: 'Przelew przychodzący',
}

function OperationList({ entries, emptyText = 'Brak operacji na rachunku.' }) {
  if (entries.length === 0) {
    return <p className="operations__empty">{emptyText}</p>
  }

  return (
    <ul className="operations">
      {entries.map((entry) => {
        const isIncoming = Number(entry.amount) > 0
        const direction = isIncoming ? 'in' : 'out'
        return (
          <li key={entry.id} className="operation" data-testid="history-entry">
            <span className={`operation__icon operation__icon--${direction}`}>
              <Icon name={isIncoming ? 'incoming' : 'outgoing'} size={16} />
            </span>
            <span className="operation__text">
              <span className="operation__title">{entry.description}</span>
              <span className="operation__meta">
                {TYPE_LABELS[entry.type]} · {formatDateTime(entry.created_at)}
              </span>
            </span>
            <span className={`operation__amount operation__amount--${direction} mono`}>
              {isIncoming ? '+' : ''}
              {formatMoney(entry.amount)}
            </span>
          </li>
        )
      })}
    </ul>
  )
}

export default OperationList
