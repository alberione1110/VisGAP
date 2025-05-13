// src/pages/ResultPage.jsx
import { useLocation } from 'react-router-dom';
import styles from './ResultPage.module.css';

export default function ResultPage() {
  // ✅ UploadPage에서 navigate로 전달된 백엔드 응답 데이터를 받는 부분
  const location = useLocation();
  const { type, segmentationUrl, gapUrl, gapValue, time } = location.state || {};

  return (
    <div className={styles.resultContainer}>
      <h2 className={styles.title}>측정 결과</h2>
      <div className={styles.resultContent}>
        {/* 왼쪽 - segmentation */}
        <div className={styles.leftColumn}>
          <h4>segmentation</h4>
          <div className={styles.imageBox}>
             {/* ✅ 백엔드에서 받은 segmentation 이미지 URL 렌더링 */}
            {type === 'single' && segmentationUrl && (
              <img src={segmentationUrl} alt="segmentation" />
            )}
          </div>
        </div>

        {/* 가운데 세로선 */}
        <div className={styles.divider}></div>

        {/* 오른쪽 - gap */}
        <div className={styles.rightColumn}>
          <h4>gap</h4>
          <div className={styles.imageBox}>
              {/* ✅ 백엔드에서 받은 gap 이미지 URL 렌더링 */}
            {type === 'single' && gapUrl && (
              <img src={gapUrl} alt="gap" />
            )}
          </div>
          <div className={styles.imageBoxSmall}>
            {/* ✅ 백엔드에서 받은 gap 수치 텍스트 렌더링 */}
            {type === 'single' && gapValue && <p>GAP: {gapValue}</p>}
          </div>
        </div>
      </div>
      {/* ✅ 백엔드에서 전달된 처리 시간 텍스트 출력 */}
      <p style={{ marginTop: '2rem', textAlign: 'center' }}>
        소요 시간: {time}
      </p>
      {/* ✅ 다중 이미지 업로드 시 zip 파일이 자동 다운로드되었음을 안내 */}
      {type === 'multiple' && (
        <p style={{ marginTop: '1rem', textAlign: 'center' }}>
          여러 이미지의 결과는 zip 파일로 자동 다운로드되었습니다.
        </p>
      )}
    </div>
  );
}
