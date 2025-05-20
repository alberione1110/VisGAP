import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './UploadPage.module.css';

export default function UploadPage() {
  const [files, setFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleFileChange = (e) => {
    const selected = Array.from(e.target.files).filter(f => f.type.startsWith('image/'));
    if (!selected.length) {
      alert('이미지 파일만 업로드 가능합니다!');
      return;
    }
    setFiles(selected);
    setPreviewUrls(selected.map(f => URL.createObjectURL(f)));
    setCurrentIndex(0);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (!dropped.length) {
      alert('이미지 파일만 업로드 가능합니다!');
      return;
    }
    setFiles(dropped);
    setPreviewUrls(dropped.map(f => URL.createObjectURL(f)));
    setCurrentIndex(0);
  };

  const handleReset = () => {
    setFiles([]);
    setPreviewUrls([]);
    setCurrentIndex(0);
  };

  const handlePrev = () => setCurrentIndex(i => Math.max(i - 1, 0));
  const handleNext = () => setCurrentIndex(i => Math.min(i + 1, previewUrls.length - 1));

  const handleSubmit = async () => {
    if (!files.length) {
      alert('파일을 먼저 선택해주세요!');
      return;
    }
    const formData = new FormData();
    files.forEach(file => formData.append('images', file));
    const endpoint = files.length === 1
      ? 'http://localhost:8080/api/upload'
      : 'http://localhost:8080/api/upload-multiple';
    try {
      const res = await fetch(endpoint, { method: 'POST', body: formData });
      const contentType = res.headers.get('Content-Type') || '';
      if (contentType.includes('application/json')) {
        const data = await res.json();
        navigate('/result', { state: { type: 'single', segmentationUrl: data.segmentation_url, gapUrl: data.gap_url, gapValue: data.gap_value, time: data.time } });
      } else if (contentType.includes('application/zip')) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url; a.download = 'gap_results.zip'; a.click(); a.remove();
        const time = res.headers.get('X-Processing-Time');
        navigate('/result', { state: { type: 'multiple', time } });
      }
    } catch (err) {
      console.error('서버 요청 실패:', err);
      alert('서버와 통신 중 오류가 발생했습니다.');
    }
  };

  const handleDragOver = e => e.preventDefault();
  const handleDragEnter = e => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = e => { e.preventDefault(); setIsDragging(false); };

  useEffect(() => {
    if (location.hash) {
      const el = document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }, [location]);

  return (
    <div className={styles.uploadContainer}>
      <h2 className={styles.title}>
        세그멘테이션 및 <span className={styles.gap}>GAP</span> 측정을 원하시는<br />
        부품의 사진을 넣어주세요
      </h2>

      <div className={styles.uploadBoxWrapper}>
        <div
          className={`${styles.uploadBox} ${isDragging ? styles.dragOver : ''}`}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
        >
          {previewUrls.length > 1 ? (
            <div className={styles.singlePreview}>
              <img src={previewUrls[currentIndex]} alt={`preview-${currentIndex}`} className={styles.previewImage} />
            </div>
          ) : previewUrls.length === 1 ? (
            <div className={styles.singlePreview}>
              <img src={previewUrls[0]} alt="preview-0" className={styles.previewImage} />
            </div>
          ) : (
            <p className={styles.placeholder}>원하는 파일을<br />드래그해서 넣어주세요</p>
          )}
        </div>
        {previewUrls.length > 1 && (
          <> 
            <button
              className={`${styles.arrowButton} ${styles.leftArrow}`} 
              onClick={handlePrev} 
              disabled={currentIndex === 0}
            >‹</button>
            <button
              className={`${styles.arrowButton} ${styles.rightArrow}`} 
              onClick={handleNext} 
              disabled={currentIndex === previewUrls.length - 1}
            >›</button>
          </>
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
    </div>
  );
}