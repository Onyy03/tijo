import { useState } from 'react'
import { api } from '../api.js'
import { toApiAmount } from '../format.js'

const EMPTY_FORM = { phoneNumber: '', amount: '', title: '' }

function TransferForm({ accountId, onTransferSent }) {
  const [form, setForm] = useState(EMPTY_FORM)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSuccess('')
    setIsSubmitting(true)
    try {
      await api.createTransfer({
        from_account_id: accountId,
        to_phone_number: form.phoneNumber.trim(),
        amount: toApiAmount(form.amount),
        title: form.title.trim(),
      })
      setSuccess('Przelew został wysłany')
      setForm(EMPTY_FORM)
      onTransferSent()
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h3 className="section-title">Przelew na telefon</h3>
      <label className="field">
        <span className="field__label">Numer telefonu odbiorcy</span>
        <input
          name="phoneNumber"
          inputMode="tel"
          maxLength={9}
          value={form.phoneNumber}
          onChange={handleChange}
          placeholder="600200300"
        />
      </label>
      <label className="field">
        <span className="field__label">Kwota (PLN)</span>
        <input
          name="amount"
          inputMode="decimal"
          value={form.amount}
          onChange={handleChange}
          placeholder="50,00"
        />
      </label>
      <label className="field">
        <span className="field__label">Tytuł</span>
        <input name="title" value={form.title} onChange={handleChange} placeholder="np. Obiad" />
      </label>
      <button type="submit" className="button button--primary" disabled={isSubmitting}>
        Wyślij przelew
      </button>
      {success && (
        <p className="message message--success" role="status">
          {success}
        </p>
      )}
      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </form>
  )
}

export default TransferForm
