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
    // FormData 생성 및 이미지 파일들 담기
    const formData = new FormData();
    files.forEach((file) => formData.append('images', file));

    // 단일 / 다중 업로드 URL 분기
    const endpoint =
      files.length === 1
        ? 'http://localhost:8080/api/upload'
        : 'http://localhost:8080/api/upload-multiple';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      const contentType = res.headers.get('Content-Type') || '';
      // 단일 업로드 응답 처리 (JSON)
      if (contentType.includes('application/json')) {
        const data = await res.json();

        // ✅ 단일 이미지 다운로드 처리
        handleDownload(data.segmentation_url, 'segmentation_result.png');
        handleDownload(data.gap_url, 'gap_result.png');

        navigate('/result', {
          state: {
            type: 'single',
            segmentationUrl: data.segmentation_url,
            gapUrl: data.gap_url,
            gapValue: data.gap_value,
            time: data.time,
          },
        });
      }
      // 다중 업로드 응답 처리 (ZIP)
      else if (contentType.includes('application/zip')) {
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

  // ✅ 다운로드 함수: 자동으로 다운로드 실행
  const handleDownload = (url, filename) => {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename; // 파일명 지정
    a.click();
    a.remove();
  };

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
          <div className={`${styles.previewWrapper} ${styles[`count${previewUrls.length}`]}`}>
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
