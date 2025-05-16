package com.aiintegration.backend.service;

import com.aiintegration.backend.dto.ImageResult;
import com.aiintegration.backend.dto.ZipResult;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

@Service
public class ImageService {
    private static final String AI_SERVER_URL = "http://localhost:8001/process-images";
    private final RestTemplate restTemplate;

    public ImageService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // 단일 이미지 처리
    public ImageResult sendToAiServer(MultipartFile file) throws IOException {
        long startTime = System.currentTimeMillis();

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource());

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);

        try {
            ResponseEntity<ImageResult> response = restTemplate.exchange(
                    AI_SERVER_URL, HttpMethod.POST, entity, ImageResult.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                ImageResult result = response.getBody();
                long duration = System.currentTimeMillis() - startTime;
                return result;
            } else {
                throw new RuntimeException("AI 서버 응답 오류: " + response.getStatusCode());
            }
        } catch (Exception e) {
            throw new RuntimeException("AI 서버 전송 실패", e);
        }
    }

    // 여러 이미지 처리
    public ZipResult processMultipleFiles(List<MultipartFile> files) throws IOException {
        long startTime = System.currentTimeMillis();

        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        ZipOutputStream zipOutputStream = new ZipOutputStream(byteArrayOutputStream);

        for (MultipartFile file : files) {
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", file.getResource());

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);

            try {
                ResponseEntity<byte[]> response = restTemplate.exchange(
                        AI_SERVER_URL, HttpMethod.POST, entity, byte[].class);

                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    byte[] resultImage = response.getBody();
                    String originalName = file.getOriginalFilename();
                    if (originalName == null) originalName = "image";

                    zipOutputStream.putNextEntry(new ZipEntry(originalName + "_result.jpg"));
                    zipOutputStream.write(resultImage);
                    zipOutputStream.closeEntry();
                } else {
                    throw new RuntimeException("AI 서버 응답 오류: " + response.getStatusCode());
                }
            } catch (Exception e) {
                throw new RuntimeException("AI 서버 전송 실패", e);
            }
        }

        zipOutputStream.close();
        long duration = System.currentTimeMillis() - startTime;

        return new ZipResult(byteArrayOutputStream.toByteArray(), duration + "ms");
    }
}
