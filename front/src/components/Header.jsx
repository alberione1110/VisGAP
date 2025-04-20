import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.css';
import logo from '../assets/Logo.png';

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => setMenuOpen(prev => !prev);

  const handleGoHome = () => {
    setMenuOpen(false);
    navigate('/');
  };

  const goSection = (hash) => {
    setMenuOpen(false);
    navigate(`/${hash}`);  // e.g. "/#segmentation", "/#gap"
  };

  return (
    <header className={styles.header}>
      <img src={logo} alt="KGU Logo" className={styles.logo} />
      <h1 className={styles.title}>G A P</h1>
      <button className={styles.menuButton} onClick={toggleMenu}>☰</button>

      {menuOpen && (
        <div className={styles.sideMenu}>
          <ul>
            <li onClick={handleGoHome}>홈</li>
            <li onClick={() => goSection('#gap')}>갭 측정 설명,예시</li>
            <li onClick={() => goSection('#segmentation')}>세그멘테이션 설명,예시</li>
          </ul>
        </div>
      )}
    </header>
  );
}
