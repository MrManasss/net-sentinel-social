"""
Hyperledger Fabric anchoring adapter for Net-Sentinel Social.

This module provides the project-side interface for anchoring the
latest SHA-256 hash-chain entry to Hyperledger Fabric.

The adapter supports:
- mock mode for local development/testing
- a clean interface for future Fabric network integration

The SHA-256 hash-chain remains the source of the audit data.
Fabric is used as the external distributed anchor.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class FabricAnchor:
    """Represents a hash-chain anchor recorded on Fabric."""

    chain_index: int
    entry_hash: str
    anchored_at: str
    transaction_id: str
    network: str
    channel: str
    chaincode: str


class FabricAnchorClient:
    """
    Client interface for Hyperledger Fabric anchoring.

    mock=True is used for local development when a Fabric network
    is not available.
    """

    def __init__(
        self,
        network: str = "net-sentinel",
        channel: str = "audit-channel",
        chaincode: str = "audit-anchor",
        mock: bool = True,
    ):
        self.network = network
        self.channel = channel
        self.chaincode = chaincode
        self.mock = mock

    def anchor_hash(
        self,
        chain_index: int,
        entry_hash: str,
    ) -> FabricAnchor:
        """
        Anchor a hash-chain entry.

        In mock mode, this creates a deterministic project-level
        anchor record without contacting a Fabric network.

        A real Fabric implementation can replace the mock transaction
        section without changing callers of this method.
        """

        if (not entry_hash
            or len(entry_hash) != 64
            or any(char not in "0123456789abcdefABCDEF" for char in entry_hash)):
            raise ValueError(
                "entry_hash must be a 64-character SHA-256 hexadecimal digest"
            )

        if chain_index < 0:
            raise ValueError("chain_index must be non-negative")

        anchored_at = datetime.now(timezone.utc).isoformat()

        if self.mock:
            transaction_id = (
                f"MOCK-TX-{chain_index:06d}-{entry_hash[:16]}"
            )
        else:
            raise NotImplementedError(
                "Real Hyperledger Fabric network integration is not "
                "configured yet."
            )

        return FabricAnchor(
            chain_index=chain_index,
            entry_hash=entry_hash,
            anchored_at=anchored_at,
            transaction_id=transaction_id,
            network=self.network,
            channel=self.channel,
            chaincode=self.chaincode,
        )


def anchor_latest_block(
    chain: list[dict],
    client: Optional[FabricAnchorClient] = None,
) -> FabricAnchor:
    """
    Anchor the latest block of an existing SHA-256 hash chain.
    """

    if not chain:
        raise ValueError("Cannot anchor an empty hash chain")

    client = client or FabricAnchorClient()

    latest_block = chain[-1]

    return client.anchor_hash(
        chain_index=latest_block["index"],
        entry_hash=latest_block["entry_hash"],
    )


if __name__ == "__main__":
    # Small local demonstration.
    demo_chain = [
        {
            "index": 0,
            "entry_hash": "a" * 64,
        },
        {
            "index": 1,
            "entry_hash": "b" * 64,
        },
    ]

    anchor = anchor_latest_block(demo_chain)

    print("NET-SENTINEL SOCIAL - Fabric Anchor Demo")
    print("-----------------------------------------")
    print(f"Network:     {anchor.network}")
    print(f"Channel:     {anchor.channel}")
    print(f"Chaincode:   {anchor.chaincode}")
    print(f"Block index: {anchor.chain_index}")
    print(f"Entry hash:  {anchor.entry_hash}")
    print(f"Timestamp:   {anchor.anchored_at}")
    print(f"Tx ID:       {anchor.transaction_id}")