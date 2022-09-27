from memory import memory

def test_memory():
    # returns 4096 bytes by default
    mem = memory()
    assert len(mem) == 4096
