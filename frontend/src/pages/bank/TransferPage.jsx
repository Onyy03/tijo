import { useEffect, useState } from 'react'
import { useOutletContext } from 'react-router'
import { api } from '../../api.js'
import { formatMoney, formatPhone, toApiAmount } from '../../format.js'

const EMPTY_FORM = { phoneNumber: '', amount: '', title: '' }

function TransferPage() {
  const { account, refresh } = useOutletContext()
  const [form, setForm] = useState(EMPTY_FORM)
  const [recipients, setRecipients] = useState([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    let active = true
    api
      .listAccounts()
      .then((accounts) => active && setRecipients(accounts.filter((item) => item.id !== account.id)))
      .catch(() => active && setRecipients([]))
    return () => {
      active = false
    }
  }, [account.id])

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
        from_account_id: account.id,
        to_phone_number: form.phoneNumber.trim(),
        amount: toApiAmount(form.amount),
        title: form.title.trim(),
      })
      setSuccess('Przelew został wysłany')
      setForm(EMPTY_FORM)
      refresh()
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <header className="bank-page-header">
        <p className="bank-page-header__eyebrow">Przelewy</p>
        <h1>Przelew na telefon</h1>
      </header>

      <div className="transfer-layout">
        <form className="bank-card transfer-form" onSubmit={handleSubmit}>
          <label className="form-row">
            <span className="form-label">Numer telefonu odbiorcy</span>
            <input
              className="input"
              name="phoneNumber"
              inputMode="tel"
              maxLength={16}
              value={form.phoneNumber}
              onChange={handleChange}
              placeholder="600 200 300"
            />
          </label>
          <label className="form-row">
            <span className="form-label">Kwota (PLN)</span>
            <input
              className="input"
              name="amount"
              inputMode="decimal"
              value={form.amount}
              onChange={handleChange}
              placeholder="0,00"
            />
          </label>
          <label className="form-row">
            <span className="form-label">Tytuł</span>
            <input
              className="input"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="np. Obiad"
            />
          </label>
          <p className="transfer-form__limits">
            Dostępne środki: <span className="mono">{formatMoney(account.balance)}</span>
            <br />
            Dzienny limit wydatków: <span className="mono">{formatMoney(1000)}</span>
          </p>
          <button type="submit" className="btn btn--primary" disabled={isSubmitting}>
            Wyślij przelew
          </button>
          {success && (
            <p className="notice notice--success" role="status">
              {success}
            </p>
          )}
          {error && (
            <p className="notice notice--error" role="alert">
              {error}
            </p>
          )}
        </form>

        <section className="bank-card recipients">
          <h2 className="bank-card__title">Odbiorcy</h2>
          <ul className="recipients__list">
            {recipients.map((recipient) => (
              <li key={recipient.id}>
                <button
                  type="button"
                  className="recipient"
                  onClick={() =>
                    setForm((current) => ({ ...current, phoneNumber: recipient.phone_number }))
                  }
                >
                  <span className="recipient__name">{recipient.owner_name}</span>
                  <span className="recipient__phone mono">
                    {formatPhone(recipient.phone_number)}
                  </span>
                </button>
              </li>
            ))}
          </ul>
          <p className="recipients__hint">Kliknij odbiorcę, żeby wpisać jego numer.</p>
        </section>
      </div>
    </>
  )
}

export default TransferPage
