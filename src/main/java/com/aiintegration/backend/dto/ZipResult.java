package com.aiintegration.backend.dto;

import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class ZipResult {
    private byte[] zipFile;
    private String duration;

    public ZipResult(byte[] zipFile, String duration) {
        this.zipFile = zipFile;
        this.duration = duration;
    }
}
