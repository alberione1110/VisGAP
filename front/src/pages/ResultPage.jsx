import styles from './ResultPage.module.css';

export default function ResultPage() {
  return (
    <div className={styles.resultContainer}>
      <h2 className={styles.title}>측정 결과</h2>
      <div className={styles.resultContent}>
        {/* 왼쪽 - segmentation */}
        <div className={styles.leftColumn}>
          <h4>segmentation</h4>
          <div className={styles.imageBox}></div>
        </div>

        {/* 가운데 세로선 */}
        <div className={styles.divider}></div>

        {/* 오른쪽 - gap */}
        <div className={styles.rightColumn}>
          <h4>gap</h4>
          <div className={styles.imageBox}></div>
          <div className={styles.imageBoxSmall}></div>
        </div>
      </div>
    </div>
  );
}
