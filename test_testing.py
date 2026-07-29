import pytest
from testing import ngetest

def test_ngetest_pas_mendekati_target():
    hasil = ngetest(10.2, 10.0, 0.5)
    assert hasil is True

def test_ngetest_pas_tidak_mendekati_target():
    hasil = ngetest(15.0, 5.0, 0.5)
    assert hasil is False

def test_ngetest_pas_tidak_diisi():
    with pytest.raises(TypeError):
        ngetest()