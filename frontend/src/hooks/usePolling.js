import { useEffect, useRef } from 'react'

// Calls `callback` right away and then every `intervalMs`, as long as `enabled` is true.
export function usePolling(callback, intervalMs, enabled = true) {
  const latestCallback = useRef(callback)

  useEffect(() => {
    latestCallback.current = callback
  }, [callback])

  useEffect(() => {
    if (!enabled) {
      return undefined
    }
    latestCallback.current()
    const timer = setInterval(() => latestCallback.current(), intervalMs)
    return () => clearInterval(timer)
  }, [intervalMs, enabled])
}
