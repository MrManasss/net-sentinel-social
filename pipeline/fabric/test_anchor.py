from anchor import FabricAnchorClient, anchor_latest_block


def test_anchor_valid_hash():
    client = FabricAnchorClient(mock=True)

    anchor = client.anchor_hash(
        chain_index=5,
        entry_hash="a" * 64,
    )

    assert anchor.chain_index == 5
    assert anchor.entry_hash == "a" * 64
    assert anchor.transaction_id.startswith("MOCK-TX-")
    assert anchor.network == "net-sentinel"
    assert anchor.channel == "audit-channel"
    assert anchor.chaincode == "audit-anchor"


def test_anchor_latest_block():
    chain = [
        {
            "index": 0,
            "entry_hash": "a" * 64,
        },
        {
            "index": 1,
            "entry_hash": "b" * 64,
        },
    ]

    anchor = anchor_latest_block(chain)

    assert anchor.chain_index == 1
    assert anchor.entry_hash == "b" * 64


def test_reject_invalid_hash():
    client = FabricAnchorClient(mock=True)

    try:
        client.anchor_hash(
            chain_index=0,
            entry_hash="invalid",
        )
        assert False, "Invalid hash should have been rejected"
    except ValueError:
        assert True

def test_reject_non_hex_hash():
    client = FabricAnchorClient(mock=True)

    try:
        client.anchor_hash(
            chain_index=0,
            entry_hash="z" * 64,
        )
        assert False, "Non-hexadecimal hash should have been rejected"
    except ValueError:
        assert True

def test_reject_empty_chain():
    try:
        anchor_latest_block([])
        assert False, "Empty chain should have been rejected"
    except ValueError:
        assert True


if __name__ == "__main__":
    test_anchor_valid_hash()
    test_anchor_latest_block()
    test_reject_invalid_hash()
    test_reject_non_hex_hash()
    test_reject_empty_chain()

    print("ALL FABRIC ANCHOR TESTS PASSED.")