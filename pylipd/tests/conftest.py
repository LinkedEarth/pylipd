from pylipd.utils.dataset import available_dataset_names, load_datasets, load_dir
import pytest 
import random

@pytest.fixture
def odp846():
    D = load_datasets('ODP846.Lawrence.2006')
    return D

@pytest.fixture
def multipleLipds(seed = 20):
    names = available_dataset_names()
    random.seed(seed)
    name_rand = random.sample(names,2)
    D = load_datasets(name_rand)
    return D, name_rand

@pytest.fixture
def pages2k():
    D = load_dir('Pages2k')
    return D

@pytest.fixture
def temp12k():
    D = load_dir('Temp12k')
    return D
