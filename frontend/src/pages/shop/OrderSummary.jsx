import { formatMoney } from '../../format.js'
import BlikCodeInput from './BlikCodeInput.jsx'

function OrderSummary({ lines, totalCents, code, onCodeChange, onPay, isSubmitting, error }) {
  const canPay = lines.length > 0 && code.length === 6 && !isSubmitting

  return (
    <aside className="order-summary" aria-labelledby="summary-title">
      <h2 id="summary-title" className="order-summary__title">
        Podsumowanie
      </h2>

      {lines.length === 0 ? (
        <p className="order-summary__empty">Koszyk jest pusty. Dodaj produkty, żeby złożyć zamówienie.</p>
      ) : (
        <ul className="order-lines">
          {lines.map((line) => (
            <li key={line.id} className="order-line">
              <span>
                <span className="mono">{line.quantity} ×</span> {line.name}
              </span>
              <span className="mono">{formatMoney(line.totalCents / 100)}</span>
            </li>
          ))}
        </ul>
      )}

      <div className="order-summary__row">
        <span>Dostawa</span>
        <span>odbiór w sklepie</span>
      </div>
      <div className="order-summary__total">
        <span>Do zapłaty</span>
        <strong className="mono" data-testid="order-total">
          {formatMoney(totalCents / 100)}
        </strong>
      </div>

      <div className="blik-method">
        <span id="blik-method-label" className="blik-method__label">
          Kod BLIK
        </span>
        <p className="blik-method__hint">Wygeneruj kod w aplikacji banku i przepisz go tutaj.</p>
        <BlikCodeInput
          value={code}
          onChange={onCodeChange}
          labelledBy="blik-method-label"
          disabled={isSubmitting}
        />
      </div>

      {error && (
        <p className="shop-notice" role="alert">
          {error}
        </p>
      )}

      <button type="button" className="shop-btn shop-btn--primary" disabled={!canPay} onClick={onPay}>
        Zapłać {formatMoney(totalCents / 100)}
      </button>
    </aside>
  )
}

export default OrderSummary
