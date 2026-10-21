import { Route, Routes } from 'react-router'
import BankApp from './components/BankApp.jsx'
import MerchantTerminal from './components/MerchantTerminal.jsx'
import BankLayout from './pages/bank/BankLayout.jsx'
import DashboardPage from './pages/bank/DashboardPage.jsx'
import './App.css'

function TwoPanelDemo() {
  return (
    <div className="layout">
      <header className="layout__header">
        <h1>MiniBlik</h1>
        <p className="layout__subtitle">Symulator płatności kodem BLIK</p>
      </header>
      <main className="layout__panels">
        <BankApp />
        <MerchantTerminal />
      </main>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/konto/:accountId" element={<BankLayout />}>
        <Route index element={<DashboardPage />} />
      </Route>
      <Route path="*" element={<TwoPanelDemo />} />
    </Routes>
  )
}

export default App
