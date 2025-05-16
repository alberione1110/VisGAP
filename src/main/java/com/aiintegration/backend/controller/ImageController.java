package com.aiintegration.backend.controller;

import com.aiintegration.backend.dto.ImageResult;
import com.aiintegration.backend.dto.ZipResult;
import com.aiintegration.backend.service.ImageService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api")
public class ImageController {

    private final ImageService imageService;

    public ImageController(ImageService imageService) {
        this.imageService = imageService;
    }

    // 단일 이미지 업로드 처리
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<ImageResult> handleSingleUpload(@RequestParam("file") MultipartFile file) {
        try {
            ImageResult result = imageService.sendToAiServer(file);

            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    // 다중 이미지 업로드 처리
    @PostMapping(value = "/upload-multiple", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<byte[]> handleMultipleFilesUpload(@RequestParam("files") List<MultipartFile> files) {
        try {
            ZipResult zipResult = imageService.processMultipleFiles(files);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
            headers.setContentDispositionFormData("attachment", "processed_images.zip");
            headers.add("X-Processting-Duration", zipResult.getDuration());

            return new ResponseEntity<>(zipResult.getZipFile(), headers, HttpStatus.OK);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
