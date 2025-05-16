// File: src/pages/ExplainPage.jsx
import React from 'react';
import styles from './ExplainPage.module.css';
import gapExample from '../assets/gap-example.png';
import segmentationOriginal from '../assets/segmentation-original.png';
import segmentationMap from '../assets/segmentation-map.png';

export default function ExplainPage() {
  return (
    <div className={styles.explainContainer}>
      <div className={styles.splitContainer}>
        {/* 왼쪽: GAP 측정 설명 */}
        <div className={styles.left}>
          <section id="gap" className={styles.section}>
            <h3>GAP 측정 설명</h3>
            <p>
              산업용 디바이스 한 면에는 마그넷과 플라스틱 외관 사이에 총 6개의 GAP이 있습니다.<br/>
              상단부 3개, 하단부 3개가 같은 높이로 배열되어 있죠.<br/>
              아래 예시 사진은 실제 촬영된 GAP 영역만 잘라낸 모습입니다.
            </p>
            <img
              src={gapExample}
              alt="GAP 예시"
              className={styles.sectionImage}
            />
            <p>
              이 GAP들을 다양한 선 검출(ex: Hough Transform)과 같은 컴퓨터 비전(ex: OpenCV library) 알고리즘을 활용하여,<br/>
              픽셀 단위로 상단부 3개의 GAP 높이를 정밀 측정하거나, 또는 하단부 3개의 GAP 높이를 측정하고,<br/>
              3개의 측정값 간의 오차를 최소화하는 이미지 처리 및 시각화 프로세스를 구현합니다.
            </p>
          </section>
        </div>

        {/* 구분선 */}
        <div className={styles.divider} />

        {/* 오른쪽: 세그멘테이션 설명 */}
        <div className={styles.right}>
          <section id="segmentation" className={styles.section}>
            <h3>세그멘테이션 설명</h3>
            <p>
              이미지에는 의미적으로 구분될 수 있는 전경과 여러 객체들이 존재합니다.<br/>
              이러한 의미적 객체들은 이미지의 각 픽셀들을 포함하는 영역을 가지죠.<br/>
              여기서, 임의의 이미지에 대해 각 픽셀들이 어떤 객체의 영역에 속하는지<br/>
              분할하여 시각화하는 컴퓨터 비전 기술이 세그멘테이션(Segmentation)입니다.
            </p>
            <div className={styles.segExampleWrapper}>
              <img
                src={segmentationOriginal}
                alt="세그멘테이션 원본"
                className={styles.sectionImage}
              />
            </div>
            <p>
              위의 산업용 이미지에서 붉은 영역 내에 있는 마그넷과 이를 둘러싸고 있는 플라스틱 외관 일부 영역에 대해 세그멘테이션을 수행합니다.<br/>
              (이미지 내의 몇몇 노이즈들은 정확한 세그멘테이션을 수행하는 데 어려움을 주며, 이를 잘 처리할 수 있는 이미지 처리 및 시각화 프로세스를 구현합니다.)
            </p>
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
      </div>
    </div>
  );
}
