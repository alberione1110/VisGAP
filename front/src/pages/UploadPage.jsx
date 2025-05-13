// src/pages/UploadPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './UploadPage.module.css';

import gapExample from '../assets/gap-example.png';
import segmentationOriginal from '../assets/segmentation-original.png';
import segmentationMap from '../assets/segmentation-map.png';

export default function UploadPage() {
  const [files, setFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleFileChange = (e) => {
    const selected = Array.from(e.target.files).filter(f => f.type.startsWith('image/'));
    if (selected.length === 0) {
      alert('이미지 파일만 업로드 가능합니다!');
      return;
    }
    setFiles(selected);
    setPreviewUrls(selected.map(f => URL.createObjectURL(f)));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (dropped.length === 0) {
      alert('이미지 파일만 업로드 가능합니다!');
      return;
    }
    setFiles(dropped);
    setPreviewUrls(dropped.map(f => URL.createObjectURL(f)));
  };

  const handleReset = () => {
    setFiles([]);
    setPreviewUrls([]);
  };

  // ✅ [핵심] "측정하기" 버튼 클릭 시 백엔드 요청
  const handleSubmit = async () => {
    if (files.length === 0) {
      alert('파일을 먼저 선택해주세요!');
      return;
    }
// 📦 FormData 생성 및 이미지 파일들 담기
    const formData = new FormData();
    files.forEach(file => formData.append('images', file)); // 백엔드에서 'images' 키로 받아야 함

    try { // 📡 백엔드로 POST 요청 전송 (Flask/FastAPI 등에서 /analyze 엔드포인트 필요)
      const res = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });

      const contentType = res.headers.get('Content-Type') || '';
// 📥 단일 이미지 처리: JSON으로 응답되면 segmentation/gap 결과 표시
      if (contentType.includes('application/json')) {
        const data = await res.json();
        navigate('/result', {
          state: {
            type: 'single',
            segmentationUrl: data.segmentation_url,
            gapUrl: data.gap_url,
            gapValue: data.gap_value,
            time: data.time,
          },
        });
            // 📥 다중 이미지 처리: ZIP 응답 → 자동 다운로드 → 결과 페이지로 이동
      } else if (contentType.includes('application/zip')) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'gap_results.zip';
        a.click();
        a.remove();

        const time = res.headers.get('X-Processing-Time');
        navigate('/result', {
          state: {
            type: 'multiple',
            time: time,
          },
        });
      }
    } catch (err) {
      console.error('서버 요청 실패:', err);
      alert('서버와 통신 중 오류가 발생했습니다.');
    }
  };

  const handleDragOver = (e) => e.preventDefault();
  const handleDragEnter = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = (e) => { e.preventDefault(); setIsDragging(false); };

  useEffect(() => {
    if (location.hash) {
      const id = location.hash.slice(1);
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }, [location]);

  return (
    <div className={styles.uploadContainer}>
      <h2 className={styles.title}>
        세그멘테이션 및 <span className={styles.gap}>GAP</span> 측정을 원하시는<br />
        부품의 사진을 넣어주세요
      </h2>

      <div
        className={`${styles.uploadBox} ${isDragging ? styles.dragOver : ''}`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
      >
        {previewUrls.length > 0 ? (
          <div className={`${styles.previewWrapper} ${styles['count' + previewUrls.length]}`}>
            {previewUrls.map((url, idx) => (
              <img key={idx} src={url} alt={`preview-${idx}`} className={styles.previewImage} />
          ))}
</div>
        ) : (
          <p className={styles.placeholder}>원하는 파일을<br />드래그해서 넣어주세요</p>
        )}
      </div>

      <div className={styles.buttonRow}>
        <label className={styles.grayButton}>
          파일 선택
          <input
            type="file"
            accept="image/*"
            multiple
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </label>
        <button className={styles.grayButton} onClick={handleReset}>파일 초기화</button>
      </div>

      <button className={styles.submitButton} onClick={handleSubmit}>측정하기</button>

      {/* ───────── GAP 설명 ───────── */}
      <section id="gap" className={styles.section}>
        <h3>GAP 측정 설명</h3>
        <p>
          산업용 디바이스 한 면에는 마그넷과 플라스틱 외관 사이에 총 6개의 GAP이 있습니다.<br/>
          상단부 3개, 하단부 3개가 같은 높이로 배열되어 있죠.<br/>
          아래 예시 사진은 실제 촬영된 GAP 영역만 잘라낸 모습입니다.
        </p>
        {/* import 한 변수를 src에 넣어줍니다 */}
        <img src={gapExample} alt="GAP 예시" className={styles.sectionImage} />
        <p>
          이 GAP들을 다양한 선 검출(ex: Hough Transform)과 같은 컴퓨터 비전(ex: OpenCV library)알고리즘을 활용하여,<br/>
          픽셀 단위로 상단부 3개의 GAP높이를 정밀 측정하거나, 또는 하단부 3개의 GAP높이를 측정하고,<br/>
          3개의 측정값 간의 오차를 최소화하는 이미지 처리 및 시각화 프로세스를 구현합니다.
        </p>
      </section>

      {/* ─── 세그멘테이션 설명 ─── */}
      <section id="segmentation" className={styles.section}>
        <h3>세그멘테이션 설명</h3>
        <p>
          이미지에는 의미적으로 구분될 수 있는 전경과 여러 객체들이 존재합니다.<br/>
          이러한 의미적 객체들은 이미지의 각 픽셀들을 포함하는 영역을 가지죠.<br/>
          여기서, 임의의 이미지에 대해 각 픽셀들이 어떤 객체의 영역에 속하는지<br/>
          분할하여 시각화하는 컴퓨터 비전 기술이이 세그멘테이션(Segmentation)입니다.
        </p>
        <div className={styles.segExampleWrapper}>
          {/* 1) 메인 이미지 (full-width) */}
          <img
            src={segmentationOriginal}
            alt="세그멘테이션 원본"
            className={styles.sectionImage}
          />
         </div> 

        <p>
          위의 산업용 이미지에서 붉은 영역내에 있는 마그넷과 이를 둘러싸고 있는 플라스틱 외관 일부영역에 대해 세그멘테이션을 수행합니다.<br/>
          (이미지 내의 몇몇 노이즈들은 정확한 세그멘테이션을 수행하는 데 어려움을 주며, 이를 잘 처리할 수 있는 이미지 처리 및 시각화 프로세스를 구현합니다.)
        </p>

        {/* 2) 맵 이미지 (본문 옆에 작은 예시) */}
        <div className={styles.smallExampleWrapper}>
          <img
            src={segmentationMap}
            alt="세그멘테이션 맵"
            className={styles.smallExampleImage}
          />
          <span className={styles.smallExampleCaption}>세그멘테이션 예시</span>
        </div>
      </section>
    </div>
  );
}
