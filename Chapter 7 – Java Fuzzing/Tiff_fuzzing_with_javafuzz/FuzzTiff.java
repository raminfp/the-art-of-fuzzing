package com.gitlab.javafuzz.examples;

import com.gitlab.javafuzz.core.AbstractFuzzTarget;

import mil.nga.tiff.TiffReader;
import mil.nga.tiff.util.TiffException;


public class FuzzTiff extends AbstractFuzzTarget {

    public void fuzz(byte[] data) {
        try {
                TiffReader.readTiff(data);
        } catch (IllegalStateException | TiffException ignored) {
        }
    }
}