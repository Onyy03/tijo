import { Navigate, Route, Routes } from 'react-router'
import BankLayout from './pages/bank/BankLayout.jsx'
import BlikPage from './pages/bank/BlikPage.jsx'
import DashboardPage from './pages/bank/DashboardPage.jsx'
import HistoryPage from './pages/bank/HistoryPage.jsx'
import TransferPage from './pages/bank/TransferPage.jsx'
import HomePage from './pages/home/HomePage.jsx'
import ShopPage from './pages/shop/ShopPage.jsx'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/konto/:accountId" element={<BankLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="blik" element={<BlikPage />} />
        <Route path="przelew" element={<TransferPage />} />
        <Route path="historia" element={<HistoryPage />} />
      </Route>
      <Route path="/sklep" element={<ShopPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
