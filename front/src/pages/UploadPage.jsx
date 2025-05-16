// src/pages/UploadPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './UploadPage.module.css';

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

    </div>
  );
}
