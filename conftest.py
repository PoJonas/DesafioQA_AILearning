import pytest
from utils.data_generator import gerar_usuario

BASE_URL = "https://compassuol.serverest.dev"

@pytest.fixture
def usuario():
    return gerar_usuario()

@pytest.fixture
def base_url():
    return BASE_URL