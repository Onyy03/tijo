import { useState } from 'react'
import { Link } from 'react-router'
import { api } from '../../api.js'
import Icon from '../../components/Icon.jsx'
import { useNow } from '../../hooks/useNow.js'
import { usePolling } from '../../hooks/usePolling.js'
import CartList from './CartList.jsx'
import OrderSummary from './OrderSummary.jsx'
import PaymentProgress from './PaymentProgress.jsx'
import { INITIAL_CART, MAX_QUANTITY, MERCHANT_NAME, PRODUCTS } from './products.js'
import './shop.css'

const STATUS_POLL_INTERVAL_MS = 2000

function paymentStage(payment, now) {
  if (payment.status === 'CONFIRMED') {
    return 'confirmed'
  }
  if (payment.status === 'REJECTED') {
    return 'rejected'
  }
  if (payment.status === 'CANCELLED') {
    return 'cancelled'
  }
  return new Date(payment.expires_at).getTime() <= now ? 'expired' : 'waiting'
}

function ShopPage() {
  const [quantities, setQuantities] = useState(INITIAL_CART)
  const [code, setCode] = useState('')
  const [payment, setPayment] = useState(null)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const now = useNow(1000)

  const lines = PRODUCTS.filter((product) => (quantities[product.id] ?? 0) > 0).map(
    (product) => ({
      ...product,
      quantity: quantities[product.id],
      totalCents: product.priceCents * quantities[product.id],
    }),
  )
  const totalCents = lines.reduce((sum, line) => sum + line.totalCents, 0)
  const itemCount = lines.reduce((sum, line) => sum + line.quantity, 0)
  const stage = payment === null ? 'cart' : paymentStage(payment, now)

  usePolling(
    async () => {
      try {
        setPayment(await api.getPayment(payment.id))
      } catch (err) {
        setError(err.message)
      }
    },
    STATUS_POLL_INTERVAL_MS,
    stage === 'waiting',
  )

  function changeQuantity(productId, delta) {
    setQuantities((current) => {
      const quantity = Math.min(MAX_QUANTITY, Math.max(0, (current[productId] ?? 0) + delta))
      return { ...current, [productId]: quantity }
    })
  }

  async function handlePay() {
    setError('')
    setIsSubmitting(true)
    try {
      const created = await api.createPayment({
        code,
        amount: (totalCents / 100).toFixed(2),
        merchant_name: MERCHANT_NAME,
      })
      setPayment(created)
    } catch (err) {
      setError(err.message)
      setCode('')
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleCancel() {
    try {
      setPayment(await api.cancelPayment(payment.id))
    } catch (err) {
      setError(err.message)
    }
  }

  function backToShop(startNewOrder) {
    setPayment(null)
    setCode('')
    setError('')
    if (startNewOrder) {
      setQuantities(INITIAL_CART)
    }
  }

  return (
    <div className="shop">
      <header className="shop-header">
        <Link className="shop-brand" to="/">
          <span className="shop-brand__mark" aria-hidden="true">
            K
          </span>
          <span className="shop-brand__text">
            <strong>{MERCHANT_NAME}</strong>
            <small>pieczywo · kawa · spiżarnia</small>
          </span>
        </Link>
        <span className="shop-header__cart">
          <Icon name="cart" />
          Koszyk <span className="shop-header__count mono">{itemCount}</span>
        </span>
      </header>

      <main className="shop-main">
        {stage === 'cart' ? (
          <div className="shop-columns">
            <CartList quantities={quantities} onQuantityChange={changeQuantity} />
            <OrderSummary
              lines={lines}
              totalCents={totalCents}
              code={code}
              onCodeChange={setCode}
              onPay={handlePay}
              isSubmitting={isSubmitting}
              error={error}
            />
          </div>
        ) : (
          <PaymentProgress
            stage={stage}
            payment={payment}
            now={now}
            onCancel={handleCancel}
            onBack={backToShop}
          />
        )}
      </main>

      <footer className="shop-footer">
        Sklep demonstracyjny projektu MiniBlik. Zamówienia nie są realizowane.
      </footer>
    </div>
  )
}

export default ShopPage
