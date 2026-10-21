import { useRef } from 'react'

const CODE_LENGTH = 6

function BlikCodeInput({ value, onChange, labelledBy, disabled }) {
  const boxes = useRef([])
  const digits = Array.from({ length: CODE_LENGTH }, (_, index) => value[index] ?? '')

  // writes `typed` digits from `index` onwards, so pasting or autofilling all 6 works
  function fillFrom(index, typed) {
    const next = [...digits]
    ;[...typed].slice(0, CODE_LENGTH - index).forEach((digit, offset) => {
      next[index + offset] = digit
    })
    onChange(next.join(''))
    boxes.current[Math.min(index + typed.length, CODE_LENGTH - 1)]?.focus()
  }

  function handleChange(index, rawValue) {
    const typed = rawValue.replace(/\D/g, '')
    if (typed === '') {
      const next = [...digits]
      next[index] = ''
      onChange(next.join(''))
      return
    }
    fillFrom(index, typed.length >= CODE_LENGTH ? typed : typed.slice(-1))
  }

  function handleKeyDown(index, event) {
    if (event.key === 'Backspace' && digits[index] === '' && index > 0) {
      boxes.current[index - 1]?.focus()
    }
  }

  function handlePaste(index, event) {
    const pasted = event.clipboardData.getData('text').replace(/\D/g, '')
    if (pasted !== '') {
      event.preventDefault()
      fillFrom(index, pasted)
    }
  }

  return (
    <div className="code-input" role="group" aria-labelledby={labelledBy}>
      {digits.map((digit, index) => (
        <input
          key={index}
          ref={(element) => {
            boxes.current[index] = element
          }}
          className="code-input__box mono"
          inputMode="numeric"
          autoComplete={index === 0 ? 'one-time-code' : 'off'}
          aria-label={`Cyfra ${index + 1} z ${CODE_LENGTH}`}
          value={digit}
          disabled={disabled}
          onChange={(event) => handleChange(index, event.target.value)}
          onKeyDown={(event) => handleKeyDown(index, event)}
          onPaste={(event) => handlePaste(index, event)}
        />
      ))}
    </div>
  )
}

export default BlikCodeInput
