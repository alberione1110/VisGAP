import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Header.module.css';
import logo from '../assets/Logo.png';

export default function Header() {
  const navigate = useNavigate();
  const handleGoHome = () => navigate('/');
  const handleGoExplain = () => navigate('/explain');

  return (
    <header className={styles.header}>
      <img
        src={logo}
        alt='LOGO'
        className={styles.logo}
      />
      <h1 className={styles.title}>G A P</h1>
      <nav className={styles.nav}>
        <ul>
          <li className={styles.link} onClick={handleGoHome}>홈</li>
          <li className={styles.separator}>•</li>
          <li className={styles.link} onClick={handleGoExplain}>설명</li>
        </ul>
      </nav>
    </header>
  );
}