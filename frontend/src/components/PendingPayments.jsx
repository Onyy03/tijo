import { useRef, useState } from 'react'
import { api } from '../api.js'
import { formatMoney } from '../format.js'
import { usePolling } from '../hooks/usePolling.js'

const POLL_INTERVAL_MS = 2000

function PendingPayments({ accountId, onPaymentArrived, onPaymentDecided }) {
  const [payments, setPayments] = useState([])
  const [busyPaymentId, setBusyPaymentId] = useState(null)
  const [error, setError] = useState('')
  const seenPaymentIds = useRef(new Set())

  async function loadPayments() {
    try {
      const pending = await api.listPendingPayments(accountId)
      const hasNewPayment = pending.some((payment) => !seenPaymentIds.current.has(payment.id))
      pending.forEach((payment) => seenPaymentIds.current.add(payment.id))
      setPayments(pending)
      if (hasNewPayment) {
        onPaymentArrived()
      }
    } catch (err) {
      setError(err.message)
    }
  }

  usePolling(loadPayments, POLL_INTERVAL_MS)

  async function decide(paymentId, decision) {
    setError('')
    setBusyPaymentId(paymentId)
    try {
      if (decision === 'confirm') {
        await api.confirmPayment(paymentId)
      } else {
        await api.rejectPayment(paymentId)
      }
      onPaymentDecided()
    } catch (err) {
      setError(err.message)
    }
    setBusyPaymentId(null)
    await loadPayments()
  }

  return (
    <div className="pending">
      <h3 className="pending__title">Płatności do potwierdzenia</h3>
      {payments.length === 0 ? (
        <p className="pending__empty">Brak płatności do potwierdzenia</p>
      ) : (
        <ul className="pending__list">
          {payments.map((payment) => (
            <li key={payment.id} className="pending__item" data-testid="pending-payment">
              <div className="pending__details">
                <strong>{payment.merchant_name}</strong>
                <span className="pending__amount">{formatMoney(payment.amount)}</span>
              </div>
              <div className="pending__actions">
                <button
                  type="button"
                  className="button button--success"
                  disabled={busyPaymentId === payment.id}
                  onClick={() => decide(payment.id, 'confirm')}
                >
                  Zatwierdź
                </button>
                <button
                  type="button"
                  className="button button--secondary"
                  disabled={busyPaymentId === payment.id}
                  onClick={() => decide(payment.id, 'reject')}
                >
                  Odrzuć
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

export default PendingPayments
