export class ApiError extends Error {
  constructor(code, message) {
    super(message)
    this.code = code
  }
}

// Validation errors carry per-field messages, which say more than the general one.
function describeError(body) {
  const fieldMessages = Object.values(body?.errors?.json ?? {}).flat()
  return fieldMessages.length > 0 ? fieldMessages.join(' ') : body?.message
}

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch {
    throw new ApiError('NETWORK_ERROR', 'Brak połączenia z serwerem')
  }
  const body = await response.json().catch(() => null)
  if (!response.ok) {
    const message = describeError(body) ?? 'Nieoczekiwany błąd serwera'
    throw new ApiError(body?.code ?? 'UNKNOWN_ERROR', message)
  }
  return body
}

function post(path, data) {
  const body = data === undefined ? undefined : JSON.stringify(data)
  return request(path, { method: 'POST', body })
}

export const api = {
  listAccounts: () => request('/accounts'),
  getAccount: (accountId) => request(`/accounts/${accountId}`),
  generateCode: (accountId) => post(`/accounts/${accountId}/blik-codes`),
  listPendingPayments: (accountId) => request(`/accounts/${accountId}/pending-payments`),
  listHistory: (accountId) => request(`/accounts/${accountId}/history`),
  getSummary: (accountId) => request(`/accounts/${accountId}/summary`),
  createPayment: (payment) => post('/payments', payment),
  getPayment: (paymentId) => request(`/payments/${paymentId}`),
  confirmPayment: (paymentId) => post(`/payments/${paymentId}/confirm`),
  rejectPayment: (paymentId) => post(`/payments/${paymentId}/reject`),
  cancelPayment: (paymentId) => post(`/payments/${paymentId}/cancel`),
  createTransfer: (transfer) => post('/transfers', transfer),
}
