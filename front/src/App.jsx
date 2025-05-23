import { Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import ResultPage from './pages/ResultPage';
import ExplainPage from './pages/ExplainPage';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app-container">
      <Header />
      <main style={{ minHeight: 'calc(100vh - 140px)' }}>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/result" element={<ResultPage />} />
          <Route path="/explain" element={<ExplainPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;