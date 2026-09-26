import { sha256 } from "./hash";

const GENESIS_HASH = "0".repeat(64);

export async function createAuditEntry(data, previousHash = GENESIS_HASH) {
  const timestamp = new Date().toISOString();

  const dataString = JSON.stringify(data);

  const dataHash = await sha256(dataString);

  const entryContent =
    timestamp + dataHash + previousHash;

  const entryHash = await sha256(entryContent);

  return {
    timestamp,
    data,
    dataHash,
    previousHash,
    entryHash,
  };
}

export async function createAuditChain(records) {
    const chain = [];
  
    let previousHash = GENESIS_HASH;
  
    for (const record of records) {
      const entry = await createAuditEntry(record, previousHash);
  
      chain.push(entry);
  
      previousHash = entry.entryHash;
    }
  
    return chain;
  }

  export async function verifyAuditChain(chain) {
    for (let i = 0; i < chain.length; i++) {
      const entry = chain[i];
  
      // Check that the data still produces the same data hash
      const dataString = JSON.stringify(entry.data);
      const expectedDataHash = await sha256(dataString);
  
      if (entry.dataHash !== expectedDataHash) {
        return {
          valid: false,
          failedIndex: i,
          reason: "Data has been modified",
        };
      }
  
      // Check that this entry points to the correct previous entry
      const expectedPreviousHash =
        i === 0 ? GENESIS_HASH : chain[i - 1].entryHash;
  
      if (entry.previousHash !== expectedPreviousHash) {
        return {
          valid: false,
          failedIndex: i,
          reason: "Previous hash does not match",
        };
      }
  
      // Recalculate this entry's own hash
      const entryContent =
        entry.timestamp +
        entry.dataHash +
        entry.previousHash;
  
      const expectedEntryHash = await sha256(entryContent);
  
      if (entry.entryHash !== expectedEntryHash) {
        return {
          valid: false,
          failedIndex: i,
          reason: "Entry hash has been modified",
        };
      }
    }
  
    return {
      valid: true,
      failedIndex: null,
      reason: "Chain is valid",
    };
  }