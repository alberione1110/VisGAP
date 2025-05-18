import { useLocation } from 'react-router-dom';
import styles from './ResultPage.module.css';

export default function ResultPage() {
  const location = useLocation();
  const { type, segUrl, gapUrl, gapValue, time } = location.state || {};

  return (
    <div className={styles.resultContainer}>
      <h2 className={styles.title}>측정 결과</h2>
      <div className={styles.resultContent}>
        {/* 왼쪽: segmentation 결과 */}
        <div className={styles.leftColumn}>
          <h4>segmentation</h4>
          <div className={styles.imageBox}>
            {segUrl && <img src={segUrl} alt="segmentation 결과 이미지" />}
          </div>
        </div>

        {/* 가운데 구분선 */}
        <div className={styles.divider}></div>

        {/* 오른쪽: GAP 결과 */}
        <div className={styles.rightColumn}>
          <h4>gap</h4>
          <div className={styles.imageBox}>
            {gapUrl && <img src={gapUrl} alt="gap 결과 이미지" />}
          </div>
          <div className={styles.imageBoxSmall}>
            {gapValue !== undefined && (
              <div>
                {Array.isArray(gapValue)
                  ? gapValue.map((val, idx) => (
                      <p key={idx}>GAP {idx + 1}: {val}px</p>
                    ))
                  : <p>GAP: {gapValue} px</p>}
              </div>
            )}
          </div>
        </div>
      </div>

      <p style={{ marginTop: '2rem', textAlign: 'center' }}>
        소요 시간: {time}s
      </p>

      {type === 'multiple' && (
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <p>여러 이미지의 결과는 zip 파일로 자동 다운로드되었습니다.</p>
          {time && <p>소요 시간: {time}s</p>}
        </div>
      )}
    </div>
  );
}
