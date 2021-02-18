import pytest
from numpy.ma import array, arange
from hypothesis import strategies as st, given

from slicereg.models.section import Section, SliceImage, Plane


cases = [
    ((0, 0), (0., 0., 0.)),
    ((1, 1), (1., -1., 0.)),
    ((2, 3), (3., -2., 0.)),
]
@pytest.mark.parametrize("imcoord, atlascoord", cases)
def test_can_get_3d_position_from_2d_pixel_coordinate_in_section(imcoord, atlascoord):
    section = Section(
        image=SliceImage(
            channels=arange(24).reshape(2, 3, 4),
            pixel_resolution_um=1
        ),
        plane=Plane(x=0, y=0, theta=0),
    )
    i, j = imcoord
    x, y, z = atlascoord
    assert section.pos_from_coord(i=i, j=j) == (x, y, z)



@given(i=st.integers(), j=st.integers())
def test_nonexistent_image_coords_raise_error(i, j):
    section = Section(
        image=SliceImage(
            channels=arange(180).reshape(2, 3, 30),
            pixel_resolution_um=1
        ),
        plane=Plane(x=0, y=0, theta=0),
    )
    if i < 0 or i >= section.image.height or j < 0 or j >= section.image.width:
        with pytest.raises(ValueError):
            section.pos_from_coord(i=i, j=j)
    else:
        assert section.pos_from_coord(i=i, j=j)