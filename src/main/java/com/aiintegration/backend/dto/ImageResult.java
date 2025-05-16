package com.aiintegration.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter @Setter
public class ImageResult {

    private byte[] gap;
    private byte[] segmentation;
    private List<String> gapText;
    private String duration;

    public ImageResult(byte[] gap, byte[] segmentation, List<String> gapText, String duration) {
        this.gap = gap;
        this.segmentation = segmentation;
        this.gapText = gapText;
        this.duration = duration;
    }
}
