import { useEffect, useState } from 'react'

// Current time in milliseconds, refreshed every `intervalMs`; drives countdowns.
export function useNow(intervalMs) {
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), intervalMs)
    return () => clearInterval(timer)
  }, [intervalMs])

  return now
}

export function secondsUntil(isoDate, now) {
  return Math.max(0, Math.ceil((new Date(isoDate).getTime() - now) / 1000))
}
