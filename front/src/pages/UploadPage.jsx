import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './UploadPage.module.css';

const API_BASE = 'http://localhost:8080';

export default function UploadPage() {
  const [files, setFiles] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = e => {
    const imgs = Array.from(e.target.files).filter(f => f.type.startsWith('image/'));
    if (!imgs.length) return alert('이미지 파일만 업로드 가능합니다!');
    setFiles(imgs);
    setPreviewUrls(imgs.map(f => URL.createObjectURL(f)));
    setCurrentIndex(0);
  };

  const handleDrop = e => {
    e.preventDefault();
    setIsDragging(false);
    const imgs = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (!imgs.length) return alert('이미지 파일만 업로드 가능합니다!');
    setFiles(imgs);
    setPreviewUrls(imgs.map(f => URL.createObjectURL(f)));
    setCurrentIndex(0);
  };

  const handleReset = () => {
    setFiles([]);
    setPreviewUrls([]);
    setIsDragging(false);
    setCurrentIndex(0);
  };

  const handleSubmit = async () => {
    if (!files.length) return alert('파일을 먼저 선택해주세요!');

    const formData = new FormData();
    if (files.length === 1) {
      formData.append('file', files[0]);
    } else {
      files.forEach(f => formData.append('files', f));
    }

    const endpoint = files.length === 1
      ? `${API_BASE}/api/upload`
      : `${API_BASE}/api/upload-multiple`;

    try {
      const res = await fetch(endpoint, { method: 'POST', body: formData });
      const ct = res.headers.get('Content-Type') || '';

      if (ct.includes('application/json')) {
        const data = await res.json();
        navigate('/result', {
          state: {
            segUrl: data.segmentationUrl,
            gapUrl: data.gapUrl,
            gapValue: data.gapValue,
            time: data.time
          }
        });
      } else if (ct.includes('application/zip')) {
        const processingTime = res.headers.get('X-Processing-Time');
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'results.zip';
        a.click();
        URL.revokeObjectURL(url);
        alert(`결과 ZIP 파일이 다운로드되었습니다.\n소요 시간: ${processingTime}s`);
      } else {
        throw new Error('알 수 없는 응답 타입입니다.');
      }
    } catch (err) {
      console.error(err);
      alert('서버와 통신 중 오류가 발생했습니다.');
    }
  };

  const handlePrev = () => setCurrentIndex(i => Math.max(0, i - 1));
  const handleNext = () => setCurrentIndex(i => Math.min(previewUrls.length - 1, i + 1));

  return (
    <div className={styles.uploadContainer}>
      <h2 className={styles.title}>
        세그멘테이션 및 <span className={styles.gap}>GAP</span> 측정을 원하시는<br />
        부품의 사진을 넣어주세요
      </h2>

      <div className={styles.uploadBoxWrapper}>
        <div
          className={`${styles.uploadBox} ${isDragging ? styles.dragOver : ''}`}
          onDragOver={e => e.preventDefault()}
          onDrop={handleDrop}
          onDragEnter={e => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={e => { e.preventDefault(); setIsDragging(false); }}
        >
          {previewUrls.length ? (
            <img
              src={previewUrls[currentIndex]}
              alt={`preview-${currentIndex}`}
              className={styles.previewImage}
            />
          ) : (
            <p className={styles.placeholder}>
              원하는 파일을<br />드래그해서 넣어주세요
            </p>
          )}
        </div>

        {previewUrls.length > 1 && (
          <>
            <button className={`${styles.arrowButton} ${styles.leftArrow}`} onClick={handlePrev} disabled={currentIndex === 0}>
  ‹
</button>
<button className={`${styles.arrowButton} ${styles.rightArrow}`} onClick={handleNext} disabled={currentIndex === previewUrls.length - 1}>
  ›
</button>
          </>
        )}
      </div>

      <div className={styles.buttonRow}>
        <label htmlFor="fileInput" className={styles.grayButton}>
          파일 선택
        </label>
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          multiple
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
        <button className={styles.grayButton} onClick={handleReset}>
          파일 초기화
        </button>
      </div>

      <button className={styles.submitButton} onClick={handleSubmit}>
        측정하기
      </button>
    </div>
  );
}