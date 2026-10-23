import Icon from '../../components/Icon.jsx'
import { formatCountdown, formatMoney } from '../../format.js'
import { secondsUntil } from '../../hooks/useNow.js'

const RESULTS = {
  confirmed: {
    tone: 'success',
    icon: 'check',
    title: 'Dziękujemy za zakupy!',
    text: (orderNumber, amount) => `Zamówienie ${orderNumber} na kwotę ${amount} zostało opłacone.`,
    action: 'Wróć do sklepu',
  },
  rejected: {
    tone: 'error',
    icon: 'close',
    title: 'Płatność odrzucona',
    text: () => 'Płatność została odrzucona w aplikacji banku. Zamówienie nie zostało złożone.',
    action: 'Wróć do koszyka',
  },
  cancelled: {
    tone: 'neutral',
    icon: 'close',
    title: 'Płatność anulowana',
    text: () => 'Płatność została anulowana. Zamówienie nie zostało złożone.',
    action: 'Wróć do koszyka',
  },
  expired: {
    tone: 'error',
    icon: 'clock',
    title: 'Czas na potwierdzenie minął',
    text: () => 'Płatność nie została potwierdzona w ciągu 2 minut. Zamówienie nie zostało złożone.',
    action: 'Wróć do koszyka',
  },
}

function PaymentProgress({ stage, payment, now, onCancel, onBack }) {
  const orderNumber = `KL-${String(payment.id).padStart(6, '0')}`
  const amount = formatMoney(payment.amount)

  if (stage === 'waiting') {
    return (
      <section className="checkout-state checkout-state--waiting">
        <span className="checkout-state__pulse" aria-hidden="true" />
        <h1 className="checkout-state__title" data-testid="shop-status">
          Potwierdź płatność w aplikacji banku
        </h1>
        <p className="checkout-state__text">
          Zamówienie {orderNumber} · <span className="mono">{amount}</span>
        </p>
        <p className="checkout-state__timer">
          Pozostały czas:{' '}
          <span className="mono">{formatCountdown(secondsUntil(payment.expires_at, now))}</span>
        </p>
        <button type="button" className="shop-btn" onClick={onCancel}>
          Anuluj płatność
        </button>
      </section>
    )
  }

  const result = RESULTS[stage]
  return (
    <section className={`checkout-state checkout-state--${result.tone}`}>
      <span className="checkout-state__icon">
        <Icon name={result.icon} size={28} />
      </span>
      <h1 className="checkout-state__title" data-testid="shop-status">
        {result.title}
      </h1>
      <p className="checkout-state__text">{result.text(orderNumber, amount)}</p>
      <button
        type="button"
        className="shop-btn shop-btn--primary"
        onClick={() => onBack(stage === 'confirmed')}
      >
        {result.action}
      </button>
    </section>
  )
}

export default PaymentProgress
