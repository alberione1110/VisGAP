// src/pages/UploadPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './UploadPage.module.css';

// ↓ src/assets 에 있는 파일을 import
import gapExample from '../assets/gap-example.png';
import segmentationOriginal from '../assets/segmentation-original.png';
import segmentationMap from '../assets/segmentation-map.png';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // 파일 선택
  const handleFileChange = (e) => {
    const sel = e.target.files[0];
    if (sel && sel.type.startsWith('image/')) {
      setFile(sel);
      setPreviewUrl(URL.createObjectURL(sel));
    } else {
      alert('이미지 파일만 업로드 가능합니다!');
    }
  };

  // 초기화
  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
  };

  // 제출
  const handleSubmit = () => {
    if (file) {
      navigate('/result');
    } else {
      alert('파일을 먼저 선택해주세요!');
    }
  };

  // Drag & Drop
  const handleDragOver = (e) => e.preventDefault();
  const handleDragEnter = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = (e) => { e.preventDefault(); setIsDragging(false); };
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const df = e.dataTransfer.files[0];
    if (df && df.type.startsWith('image/')) {
      setFile(df);
      setPreviewUrl(URL.createObjectURL(df));
    } else {
      alert('이미지 파일만 업로드 가능합니다!');
    }
  };

  // 해시(#gap, #segmentation) 변경 시 스크롤
  useEffect(() => {
    if (location.hash) {
      const id = location.hash.slice(1);
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }, [location]);

  return (
    <div className={styles.uploadContainer}>
      {/* 업로드 & 미리보기 */}
      <h2 className={styles.title}>
        세그멘테이션 및 <span className={styles.gap}>GAP</span> 측정을 원하시는<br/>
        부품의 사진을 넣어주세요
      </h2>
      <div
        className={`${styles.uploadBox} ${isDragging ? styles.dragOver : ''}`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
      >
        {previewUrl
          ? <img src={previewUrl} alt="미리보기" className={styles.previewImage} />
          : <p className={styles.placeholder}>원하는 파일을<br/>드래그해서 넣어주세요</p>
        }
      </div>
      <div className={styles.buttonRow}>
        <label className={styles.grayButton}>
          파일 선택
          <input
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </label>
        <button className={styles.grayButton} onClick={handleReset}>
          파일 초기화
        </button>
      </div>
      <button className={styles.submitButton} onClick={handleSubmit}>
        측정하기
      </button>

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
