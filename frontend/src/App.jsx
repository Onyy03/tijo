import BankApp from './components/BankApp.jsx'
import './App.css'

function App() {
  return (
    <div className="layout">
      <header className="layout__header">
        <h1>MiniBlik</h1>
        <p className="layout__subtitle">Symulator płatności kodem BLIK</p>
      </header>
      <main className="layout__panels">
        <BankApp />
      </main>
    </div>
  )
}

export default App
