import { useRef, useState } from 'react'
import { api } from '../../api.js'
import { formatCountdown, formatMoney } from '../../format.js'
import { secondsUntil, useNow } from '../../hooks/useNow.js'
import { usePolling } from '../../hooks/usePolling.js'

const POLL_INTERVAL_MS = 2000

function PaymentConfirmation({ accountId, onPaymentArrived, onPaymentDecided }) {
  const [payments, setPayments] = useState([])
  const [isBusy, setIsBusy] = useState(false)
  const [error, setError] = useState('')
  const seenPaymentIds = useRef(new Set())
  const now = useNow(1000)

  async function loadPayments() {
    try {
      const pending = await api.listPendingPayments(accountId)
      const hasNewPayment = pending.some((payment) => !seenPaymentIds.current.has(payment.id))
      pending.forEach((payment) => seenPaymentIds.current.add(payment.id))
      setPayments(pending)
      if (hasNewPayment) {
        setError('')
        onPaymentArrived()
      }
    } catch (err) {
      setError(err.message)
    }
  }

  usePolling(loadPayments, POLL_INTERVAL_MS)

  const payment = payments[0]
  if (payment === undefined) {
    return null
  }

  async function decide(decision) {
    setError('')
    setIsBusy(true)
    try {
      if (decision === 'confirm') {
        await api.confirmPayment(payment.id)
      } else {
        await api.rejectPayment(payment.id)
      }
      onPaymentDecided()
    } catch (err) {
      setError(err.message)
    }
    setIsBusy(false)
    await loadPayments()
  }

  const secondsLeft = secondsUntil(payment.expires_at, now)

  return (
    <div className="confirm-overlay">
      <section
        className="confirm-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        data-testid="payment-confirmation"
      >
        <p className="confirm-dialog__eyebrow">Płatność BLIK</p>
        <h2 id="confirm-title" className="confirm-dialog__title">
          Potwierdź płatność
        </h2>
        <dl className="confirm-dialog__details">
          <div>
            <dt>Odbiorca</dt>
            <dd data-testid="confirmation-merchant">{payment.merchant_name}</dd>
          </div>
          <div>
            <dt>Kwota</dt>
            <dd className="confirm-dialog__amount mono" data-testid="confirmation-amount">
              {formatMoney(payment.amount)}
            </dd>
          </div>
        </dl>
        <p className="confirm-dialog__time">
          {secondsLeft > 0 ? (
            <>
              Czas na decyzję: <span className="mono">{formatCountdown(secondsLeft)}</span>
            </>
          ) : (
            'Czas na potwierdzenie minął'
          )}
        </p>
        {error && (
          <p className="notice notice--error" role="alert">
            {error}
          </p>
        )}
        <div className="confirm-dialog__actions">
          <button
            type="button"
            className="btn btn--danger"
            disabled={isBusy}
            onClick={() => decide('reject')}
          >
            Odrzuć
          </button>
          <button
            type="button"
            className="btn btn--primary"
            disabled={isBusy || secondsLeft === 0}
            onClick={() => decide('confirm')}
            autoFocus
          >
            Zatwierdź
          </button>
        </div>
        {payments.length > 1 && (
          <p className="confirm-dialog__queue">Kolejne płatności czekające: {payments.length - 1}</p>
        )}
      </section>
    </div>
  )
}

export default PaymentConfirmation
