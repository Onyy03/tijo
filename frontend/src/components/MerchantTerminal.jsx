import { useState } from 'react'
import { api } from '../api.js'
import { formatMoney, toApiAmount } from '../format.js'
import { usePolling } from '../hooks/usePolling.js'

const STATUS_POLL_INTERVAL_MS = 2000
const EMPTY_FORM = { merchantName: '', amount: '', code: '' }

function describePayment(payment) {
  if (payment.status === 'CONFIRMED') {
    return { kind: 'success', text: 'Płatność zatwierdzona' }
  }
  if (payment.status === 'REJECTED') {
    return { kind: 'error', text: 'Płatność odrzucona' }
  }
  if (new Date(payment.expires_at) <= new Date()) {
    return { kind: 'error', text: 'Czas na potwierdzenie minął' }
  }
  return { kind: 'pending', text: 'Oczekuje na potwierdzenie w aplikacji bankowej…' }
}

function MerchantTerminal() {
  const [form, setForm] = useState(EMPTY_FORM)
  const [payment, setPayment] = useState(null)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const description = payment && describePayment(payment)
  const isWaiting = description?.kind === 'pending'

  usePolling(
    async () => {
      try {
        setPayment(await api.getPayment(payment.id))
      } catch (err) {
        setError(err.message)
      }
    },
    STATUS_POLL_INTERVAL_MS,
    isWaiting,
  )

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const created = await api.createPayment({
        code: form.code.trim(),
        amount: toApiAmount(form.amount),
        merchant_name: form.merchantName.trim(),
      })
      setPayment(created)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  function handleNewPayment() {
    setPayment(null)
    setError('')
    setForm((current) => ({ ...EMPTY_FORM, merchantName: current.merchantName }))
  }

  return (
    <section className="panel" aria-labelledby="terminal-title">
      <h2 id="terminal-title" className="panel__title">
        Terminal sklepu
      </h2>

      {payment === null ? (
        <form className="form" onSubmit={handleSubmit}>
          <label className="field">
            <span className="field__label">Nazwa sklepu</span>
            <input
              name="merchantName"
              value={form.merchantName}
              onChange={handleChange}
              placeholder="np. Żabka"
            />
          </label>
          <label className="field">
            <span className="field__label">Kwota (PLN)</span>
            <input
              name="amount"
              inputMode="decimal"
              value={form.amount}
              onChange={handleChange}
              placeholder="25,00"
            />
          </label>
          <label className="field">
            <span className="field__label">Kod BLIK</span>
            <input
              name="code"
              inputMode="numeric"
              autoComplete="off"
              maxLength={6}
              value={form.code}
              onChange={handleChange}
              placeholder="000000"
            />
          </label>
          <button type="submit" className="button button--primary" disabled={isSubmitting}>
            Zapłać
          </button>
        </form>
      ) : (
        <div className={`terminal-status terminal-status--${description.kind}`}>
          <p className="terminal-status__amount">{formatMoney(payment.amount)}</p>
          <p className="terminal-status__merchant">{payment.merchant_name}</p>
          <p className="terminal-status__text" role="status" data-testid="terminal-status">
            {description.text}
          </p>
          {!isWaiting && (
            <button type="button" className="button button--secondary" onClick={handleNewPayment}>
              Nowa płatność
            </button>
          )}
        </div>
      )}

      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </section>
  )
}

export default MerchantTerminal
