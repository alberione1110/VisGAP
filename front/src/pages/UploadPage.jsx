import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './UploadPage.module.css';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
    } else {
      alert('이미지 파일만 업로드 가능합니다!');
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
  };

  const handleSubmit = () => {
    if (file) {
      // TODO: 업로드 상태 저장/전달이 필요하면 여기서 처리
      navigate('/result');
    } else {
      alert('파일을 먼저 선택해주세요!');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      const droppedFile = droppedFiles[0];
      if (droppedFile.type.startsWith('image/')) {
        setFile(droppedFile);
        setPreviewUrl(URL.createObjectURL(droppedFile));
      } else {
        alert('이미지 파일만 업로드 가능합니다!');
      }
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  return (
    <div className={styles.uploadContainer}>
      <h2 className={styles.title}>
        세그맨테이션 및 <span className={styles.gap}>GAP</span> 측정을 원하시는<br />
        부품의 사진을 넣어주세요
      </h2>

      <div
        className={`${styles.uploadBox} ${isDragging ? styles.dragOver : ''}`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
      >
        {previewUrl ? (
          <img src={previewUrl} alt="미리보기" className={styles.previewImage} />
        ) : (
          <p className={styles.placeholder}>
            원하시는 파일을<br />드래그해서 넣어주세요
          </p>
        )}
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
    </div>
  );
}
