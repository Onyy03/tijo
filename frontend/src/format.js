const moneyFormat = new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN' })
const dateTimeFormat = new Intl.DateTimeFormat('pl-PL', {
  dateStyle: 'short',
  timeStyle: 'medium',
})

export function formatMoney(amount) {
  return moneyFormat.format(Number(amount))
}

export function formatDateTime(isoDate) {
  return dateTimeFormat.format(new Date(isoDate))
}

export function formatCode(code) {
  return `${code.slice(0, 3)} ${code.slice(3)}`
}

export function formatInitials(fullName) {
  return fullName
    .split(' ')
    .map((part) => part[0])
    .join('')
}

export function formatPhone(phoneNumber) {
  return phoneNumber.replace(/(\d{3})(\d{3})(\d{3})/, '$1 $2 $3')
}

export function formatCountdown(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = String(totalSeconds % 60).padStart(2, '0')
  return `${minutes}:${seconds}`
}

// Users type "25,00"; the API expects "25.00".
export function toApiAmount(text) {
  return text.trim().replace(',', '.')
}
