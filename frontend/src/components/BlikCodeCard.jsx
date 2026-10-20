import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { formatCode, formatCountdown } from '../format.js'

const CODE_LIFETIME_SECONDS = 120

function secondsUntil(isoDate) {
  return Math.max(0, Math.ceil((new Date(isoDate).getTime() - Date.now()) / 1000))
}

function BlikCodeCard({ accountId }) {
  const [blikCode, setBlikCode] = useState(null)
  const [secondsLeft, setSecondsLeft] = useState(0)
  const [error, setError] = useState('')

  useEffect(() => {
    if (blikCode === null) {
      return undefined
    }
    const timer = setInterval(() => setSecondsLeft(secondsUntil(blikCode.expires_at)), 1000)
    return () => clearInterval(timer)
  }, [blikCode])

  async function handleGenerate() {
    setError('')
    try {
      const generated = await api.generateCode(accountId)
      setSecondsLeft(secondsUntil(generated.expires_at))
      setBlikCode(generated)
    } catch (err) {
      setError(err.message)
    }
  }

  const isActive = blikCode !== null && secondsLeft > 0
  const isExpired = blikCode !== null && secondsLeft === 0

  return (
    <div className="blik-card">
      {isActive && (
        <>
          <p className="blik-card__code" data-testid="blik-code">
            {formatCode(blikCode.code)}
          </p>
          <div className="blik-card__progress" aria-hidden="true">
            <span style={{ width: `${(secondsLeft / CODE_LIFETIME_SECONDS) * 100}%` }} />
          </div>
          <p className="blik-card__timer">Kod ważny jeszcze {formatCountdown(secondsLeft)}</p>
        </>
      )}
      {isExpired && (
        <p className="message message--error" role="status">
          Kod BLIK wygasł. Wygeneruj nowy kod.
        </p>
      )}
      <button type="button" className="button button--primary" onClick={handleGenerate}>
        {blikCode === null ? 'Generuj kod BLIK' : 'Wygeneruj nowy kod'}
      </button>
      {error && (
        <p className="message message--error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}

export default BlikCodeCard
