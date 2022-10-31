from ob.storage.compressors import GzCompressor


def test_gz_compressor(rel):
    processor = GzCompressor(compress_level=5)

    with open(rel("data/example.obpy"), "rb") as f:
        res = processor.call(f)
        print(res.read())

    assert False
