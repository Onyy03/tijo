import Icon from '../../components/Icon.jsx'
import { formatMoney } from '../../format.js'
import { MAX_QUANTITY, PRODUCTS } from './products.js'

function CartList({ quantities, onQuantityChange }) {
  return (
    <section className="shop-products" aria-labelledby="products-title">
      <h1 id="products-title" className="shop-title">
        Twoje zakupy
      </h1>
      <ul className="product-list">
        {PRODUCTS.map((product) => {
          const quantity = quantities[product.id] ?? 0
          return (
            <li key={product.id} className="product" data-testid={`product-${product.id}`}>
              <span className="product__swatch" style={{ background: product.swatch }}>
                {product.name[0]}
              </span>
              <span className="product__info">
                <span className="product__name">{product.name}</span>
                <span className="product__details">{product.details}</span>
              </span>
              <span className="product__price mono">{formatMoney(product.priceCents / 100)}</span>
              <span className="stepper">
                <button
                  type="button"
                  className="stepper__button"
                  aria-label={`Odejmij: ${product.name}`}
                  disabled={quantity === 0}
                  onClick={() => onQuantityChange(product.id, -1)}
                >
                  <Icon name="minus" size={16} />
                </button>
                <span className="stepper__value mono" aria-live="polite">
                  {quantity}
                </span>
                <button
                  type="button"
                  className="stepper__button"
                  aria-label={`Dodaj: ${product.name}`}
                  disabled={quantity === MAX_QUANTITY}
                  onClick={() => onQuantityChange(product.id, 1)}
                >
                  <Icon name="plus" size={16} />
                </button>
              </span>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

export default CartList
