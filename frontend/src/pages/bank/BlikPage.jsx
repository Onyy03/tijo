import { useState } from 'react'
import { useOutletContext } from 'react-router'
import { api } from '../../api.js'
import { formatCountdown } from '../../format.js'
import { secondsUntil, useNow } from '../../hooks/useNow.js'

const CODE_LIFETIME_SECONDS = 120

function BlikPage() {
  const { account, blikCode, setBlikCode } = useOutletContext()
  const [error, setError] = useState('')
  const now = useNow(1000)

  async function handleGenerate() {
    setError('')
    try {
      const generated = await api.generateCode(account.id)
      setBlikCode({ ...generated, accountId: account.id, used: false })
    } catch (err) {
      setError(err.message)
    }
  }

  const secondsLeft =
    blikCode === null
      ? 0
      : Math.min(CODE_LIFETIME_SECONDS, secondsUntil(blikCode.expires_at, now))
  const isUsed = blikCode !== null && blikCode.used
  const isActive = blikCode !== null && !isUsed && secondsLeft > 0
  const isExpired = blikCode !== null && !isUsed && secondsLeft === 0

  return (
    <>
      <header className="bank-page-header">
        <p className="bank-page-header__eyebrow">Płatności mobilne</p>
        <h1>Kod BLIK</h1>
      </header>

      <section className="bank-card blik-panel">
        {isActive ? (
          <>
            <p className="blik-panel__digits mono" data-testid="blik-code">
              {[...blikCode.code].map((digit, index) => (
                <span key={index} className="blik-panel__digit">
                  {digit}
                </span>
              ))}
            </p>
            <div className="blik-panel__timer">
              <div className="blik-panel__bar" aria-hidden="true">
                <span style={{ width: `${(secondsLeft / CODE_LIFETIME_SECONDS) * 100}%` }} />
              </div>
              <span className="blik-panel__time" data-testid="blik-timer">
                Kod ważny jeszcze <span className="mono">{formatCountdown(secondsLeft)}</span>
              </span>
            </div>
          </>
        ) : (
          <p className="blik-panel__placeholder" role="status">
            {isUsed && 'Kod został użyty w płatności. Do kolejnej płatności wygeneruj nowy.'}
            {isExpired && 'Kod BLIK wygasł. Wygeneruj nowy kod.'}
            {blikCode === null &&
              'Wygeneruj kod, żeby zapłacić w sklepie internetowym lub przy kasie.'}
          </p>
        )}
        <button type="button" className="btn btn--primary" onClick={handleGenerate}>
          {blikCode === null ? 'Generuj kod BLIK' : 'Wygeneruj nowy kod'}
        </button>
        {error && <p className="notice notice--error">{error}</p>}
      </section>

      <section className="bank-card bank-card--quiet">
        <h2 className="bank-card__title">Jak to działa</h2>
        <ol className="steps">
          <li>Wygeneruj kod. Jest ważny przez 2 minuty i działa tylko raz.</li>
          <li>Wpisz go w sklepie przy wyborze płatności BLIK.</li>
          <li>Potwierdź płatność w oknie, które pojawi się w bankowości.</li>
        </ol>
        <p className="blik-panel__warning">
          Nie podawaj kodu przez telefon ani w wiadomościach. Pracownik banku nigdy o niego nie
          prosi.
        </p>
      </section>
    </>
  )
}

export default BlikPage
