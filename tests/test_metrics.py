from src.metrics import *
import nibabel as nib
import nibabel.streamlines as nibs
import pytest
import numpy as np
import math


@pytest.fixture
def reference_files():
    reference_nii = nib.load("reference.nii.gz")
    left_tck = nibs.load("AF_left.tck")
    right_tck = nibs.load("AF_right.tck")
    vol_L = streamline2volume(left_tck, reference_nii)
    vol_R = streamline2volume(right_tck, reference_nii)
    return (reference_nii, left_tck, right_tck, vol_L, vol_R)


def test_streamline2volume(reference_files):
    reference_nii = reference_files[0]
    left_tck = reference_files[1]
    right_tck = reference_files[2]

    out_left = streamline2volume(left_tck, reference_nii)
    out_right = streamline2volume(right_tck, reference_nii)
    sum_L = np.sum(out_left)
    sum_R = np.sum(out_right)  # checking volume as test

    assert sum_L != sum_R
    assert sum_L == 33278
    assert sum_R == 27163


def test_tract_length(reference_files):
    left_tck = reference_files[1]
    right_tck = reference_files[2]

    out_left = tract_length(left_tck)
    out_right = tract_length(right_tck)

    assert out_left != out_right
    assert math.isclose(out_left, 94.77, rel_tol=10e-3)
    assert math.isclose(out_right, 83.20, rel_tol=10e-3)


def test_tract_span(reference_files):
    left_tck = reference_files[1]
    right_tck = reference_files[2]

    out_left = tract_span(left_tck)
    out_right = tract_span(right_tck)

    assert out_left != out_right
    assert math.isclose(out_left, 43.85, rel_tol=10e-3)
    assert math.isclose(out_right, 52.04, rel_tol=10e-3)


def test_tract_diameter(reference_files):
    left_tck = reference_files[1]
    right_tck = reference_files[2]
    vol_L = reference_files[3]
    vol_R = reference_files[4]

    out_left = tract_diameter(left_tck, vol_L)
    out_right = tract_diameter(right_tck, vol_R)

    assert out_left != out_right
    assert math.isclose(out_left, 21.14, rel_tol=10e-3)
    assert math.isclose(out_right, 20.39, rel_tol=10e-3)


def test_tract_surface_area(reference_files):
    vol_L = reference_files[3]
    vol_R = reference_files[4]

    out_left = tract_surface_area(vol_L)
    out_right = tract_surface_area(vol_R)

    assert out_left != out_right
    assert math.isclose(out_left, 41141, rel_tol=10e1)
    assert math.isclose(out_right, 35243, rel_tol=10e-1)
