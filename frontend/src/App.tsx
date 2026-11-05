import { useEffect, useMemo, useState } from 'react'

type Product = {
  id: number
  name: string
  price: number
  category: string
  image_url: string
}

type CartLine = {
  product_id: number
  name: string
  unit_price: number
  quantity: number
  subtotal: number
}

type CartCalculation = { items: CartLine[]; total: number }
type ProductStyle = { category: string; image: string; tone: string }

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/api/v1'
const fallbackImage =
  'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=700&q=85'
const money = new Intl.NumberFormat('es-CL', {
  style: 'currency',
  currency: 'CLP',
  maximumFractionDigits: 0,
})

const legacyProductStyles: Record<number, ProductStyle> = {
  1: {
    category: 'Café',
    tone: 'bg-[#e8e1d5]',
    image:
      'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=85',
  },
  2: {
    category: 'Hogar',
    tone: 'bg-[#e5e8e3]',
    image:
      'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=700&q=85',
  },
}

function infoFor(product: Product): ProductStyle {
  if (product.image_url) {
    return { category: product.category, tone: 'bg-stone-100', image: product.image_url }
  }
  return legacyProductStyles[product.id] ?? {
    category: product.category,
    tone: 'bg-stone-100',
    image: fallbackImage,
  }
}

function BagIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" className="h-5 w-5" aria-hidden="true">
      <path d="M5 8.5h14l-1 12H6l-1-12Z" />
      <path d="M9 10V7a3 3 0 0 1 6 0v3" />
    </svg>
  )
}

function App() {
  const [products, setProducts] = useState<Product[]>([])
  const [cart, setCart] = useState<Record<number, number>>({})
  const [calculation, setCalculation] = useState<CartCalculation | null>(null)
  const [category, setCategory] = useState('Todo')
  const [loadingProducts, setLoadingProducts] = useState(true)
  const [calculating, setCalculating] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const controller = new AbortController()
    fetch(`${API_URL}/products`, { signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error('No se pudo cargar el catálogo.')
        return response.json() as Promise<Product[]>
      })
      .then(setProducts)
      .catch((reason: unknown) => {
        if ((reason as Error).name !== 'AbortError') {
          setError('No pudimos cargar los productos. Verifica que la API esté activa.')
        }
      })
      .finally(() => setLoadingProducts(false))
    return () => controller.abort()
  }, [])

  const cartItems = useMemo(
    () => products.filter((product) => cart[product.id]),
    [products, cart],
  )
  const itemCount = Object.values(cart).reduce((sum, quantity) => sum + quantity, 0)
  const categories = [
    'Todo',
    ...Array.from(new Set(products.map((product) => infoFor(product).category))),
  ]
  const filteredProducts = category === 'Todo'
    ? products
    : products.filter((product) => infoFor(product).category === category)

  useEffect(() => {
    const items = Object.entries(cart).map(([product_id, quantity]) => ({
      product_id: Number(product_id), quantity,
    }))
    if (!items.length) return
    const controller = new AbortController()
    setCalculating(true)
    fetch(`${API_URL}/cart/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items }),
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) throw new Error('No se pudo actualizar el carrito.')
        return response.json() as Promise<CartCalculation>
      })
      .then((result) => { setCalculation(result); setError('') })
      .catch((reason: unknown) => {
        if ((reason as Error).name !== 'AbortError') {
          setError('No pudimos actualizar el total. Inténtalo de nuevo.')
        }
      })
      .finally(() => setCalculating(false))
    return () => controller.abort()
  }, [cart])

  const changeQuantity = (id: number, delta: number) => setCart((current) => {
    const nextQuantity = (current[id] ?? 0) + delta
    if (nextQuantity <= 0) {
      const { [id]: _removed, ...rest } = current
      return rest
    }
    return { ...current, [id]: nextQuantity }
  })

  return (
    <main className="min-h-screen bg-[#f8f7f4] text-[#20241f] selection:bg-[#cad6c9]">
      <header className="border-b border-[#dedfd9] bg-[#f8f7f4]/95 px-6 py-5 lg:px-12">
        <div className="mx-auto flex max-w-[1480px] items-center justify-between">
          <a className="font-serif text-2xl tracking-[-0.06em]" href="#inicio">oliva.</a>
          <nav className="hidden gap-8 text-[11px] font-semibold uppercase tracking-[0.17em] text-[#61665e] sm:flex">
            <a className="text-[#20241f]" href="#tienda">Tienda</a>
            <a href="#coleccion">Colección</a>
            <a href="#historia">Historia</a>
          </nav>
          <a href="#carrito" className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.15em]" aria-label={`Carrito, ${itemCount} productos`}>
            <BagIcon /><span>Bolsa</span>
            <span className="rounded-full bg-[#20241f] px-1.5 py-0.5 text-[10px] text-white">{itemCount}</span>
          </a>
        </div>
      </header>

      <section id="inicio" className="border-b border-[#dedfd9] px-6 py-12 lg:px-12 lg:py-16">
        <div className="mx-auto max-w-[1480px]">
          <p className="mb-4 text-[10px] font-bold uppercase tracking-[0.22em] text-[#6e786c]">Objetos para el ritual diario</p>
          <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <h1 className="max-w-2xl font-serif text-5xl leading-[0.93] tracking-[-0.065em] sm:text-6xl lg:text-7xl">Pequeños detalles,<br />grandes momentos.</h1>
            <p className="max-w-xs text-sm leading-6 text-[#6b706a]">Una selección honesta de objetos cotidianos, pensados para acompañarte con calma.</p>
          </div>
        </div>
      </section>

      <div className="mx-auto grid max-w-[1480px] lg:grid-cols-[minmax(0,1fr)_390px]">
        <section id="tienda" className="min-w-0 px-6 py-9 lg:border-r lg:border-[#dedfd9] lg:px-12 lg:py-12">
          <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
            <h2 className="font-serif text-3xl tracking-[-0.05em]">La selección</h2>
            <div className="flex rounded-full border border-[#d9dbd5] p-1 text-[10px] font-bold uppercase tracking-[0.12em]">
              {categories.map((item) => (
                <button key={item} onClick={() => setCategory(item)} className={`rounded-full px-3 py-2 transition ${category === item ? 'bg-[#20241f] text-white' : 'text-[#737870] hover:text-[#20241f]'}`}>
                  {item}
                </button>
              ))}
            </div>
          </div>

          {loadingProducts ? <p className="py-16 text-sm text-[#70756d]">Cargando selección…</p> : (
            <div className="grid grid-cols-1 gap-x-5 gap-y-9 sm:grid-cols-2 xl:grid-cols-3">
              {filteredProducts.map((product) => {
                const style = infoFor(product)
                return (
                  <article key={product.id} className="group">
                    <div className={`relative aspect-[4/5] overflow-hidden ${style.tone}`}>
                      <img src={style.image} alt={product.name} onError={(event) => { event.currentTarget.src = fallbackImage }} className="h-full w-full object-contain p-8 transition duration-500 group-hover:scale-[1.04]" />
                      <button onClick={() => changeQuantity(product.id, 1)} className="absolute bottom-3 right-3 grid h-10 w-10 place-items-center rounded-full bg-[#f8f7f4] text-xl font-light shadow-sm transition hover:bg-[#20241f] hover:text-white sm:translate-y-2 sm:opacity-0 sm:group-hover:translate-y-0 sm:group-hover:opacity-100" aria-label={`Añadir ${product.name}`}>+</button>
                    </div>
                    <div className="flex items-start justify-between gap-3 pt-4">
                      <div><h3 className="text-sm font-medium">{product.name}</h3><p className="mt-1 text-xs text-[#777c75]">{style.category}</p></div>
                      <span className="text-sm">{money.format(product.price)}</span>
                    </div>
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <aside id="carrito" className="bg-[#f1f0eb] px-6 py-9 lg:sticky lg:top-0 lg:h-screen lg:px-8 lg:py-12">
          <div className="flex items-baseline justify-between border-b border-[#d8d9d2] pb-6">
            <h2 className="font-serif text-3xl tracking-[-0.05em]">Tu bolsa</h2>
            <span className="text-[10px] font-bold uppercase tracking-[0.15em] text-[#737870]">{itemCount} {itemCount === 1 ? 'artículo' : 'artículos'}</span>
          </div>

          <div className="divide-y divide-[#d8d9d2]">
            {cartItems.length === 0 ? <p className="py-10 text-sm text-[#70756d]">Tu bolsa está esperando algo especial.</p> : cartItems.map((product) => {
              const style = infoFor(product)
              const line = calculation?.items.find((item) => item.product_id === product.id)
              return (
                <div className="flex gap-4 py-5" key={product.id}>
                  <img src={style.image} alt="" className="h-20 w-16 object-cover" />
                  <div className="flex min-w-0 flex-1 flex-col">
                    <div className="flex justify-between gap-2">
                      <div><h3 className="text-sm font-medium">{product.name}</h3><p className="mt-1 text-xs text-[#777c75]">{style.category}</p></div>
                      <span className="text-sm">{money.format(line?.subtotal ?? product.price * cart[product.id])}</span>
                    </div>
                    <div className="mt-auto flex items-center justify-between">
                      <div className="flex items-center border border-[#d3d5ce] text-xs">
                        <button onClick={() => changeQuantity(product.id, -1)} className="grid h-7 w-7 place-items-center hover:bg-white" aria-label="Restar cantidad">−</button>
                        <span className="grid w-6 place-items-center">{cart[product.id]}</span>
                        <button onClick={() => changeQuantity(product.id, 1)} className="grid h-7 w-7 place-items-center hover:bg-white" aria-label="Sumar cantidad">+</button>
                      </div>
                      <button onClick={() => changeQuantity(product.id, -cart[product.id])} className="text-[10px] font-bold uppercase tracking-[0.12em] text-[#7c8179] underline underline-offset-4 hover:text-[#20241f]">Quitar</button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="mt-4 border-t border-[#d8d9d2] pt-5">
            <div className="flex justify-between text-sm">
              <span className="text-[#6e736c]">Subtotal {calculating && <span className="text-xs">· actualizando</span>}</span>
              <span>{money.format(cartItems.length ? calculation?.total ?? 0 : 0)}</span>
            </div>
            <p className="mt-2 text-xs leading-5 text-[#777c75]">Impuestos y envío se calculan en el siguiente paso.</p>
            {error && <p role="alert" className="mt-3 text-xs leading-5 text-[#9b3d32]">{error}</p>}
            <button disabled={!cartItems.length || calculating} className="mt-6 w-full bg-[#20241f] px-5 py-4 text-[11px] font-bold uppercase tracking-[0.17em] text-white transition hover:bg-[#465044] disabled:cursor-not-allowed disabled:opacity-40">Finalizar compra · {money.format(cartItems.length ? calculation?.total ?? 0 : 0)}</button>
            <p className="mt-4 text-center text-[10px] font-semibold uppercase tracking-[0.12em] text-[#858a82]">Pago seguro · Envío en 2–4 días</p>
          </div>
        </aside>
      </div>
    </main>
  )
}

export default App
