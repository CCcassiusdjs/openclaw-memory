# Temporal Data Converter

**Source:** https://docs.temporal.io/dataconversion
**Date:** 2026-03-12
**Status:** read

---

## What is a Data Converter?

SDK components that handle **serialization and encoding** of data entering and exiting a Temporal Service.

## How It Works

### Encoding (Outbound)
1. Application data → Data Converter
2. Data Converter encodes to **Payload**
3. Payload sent to Temporal Service

### Decoding (Inbound)
1. Temporal Server sends encoded Payload to Worker
2. Data Converter decodes Payload
3. Application processes decoded data

**Key insight**: Decoded Workflow results are never persisted back to Temporal Service - stored encoded.

## Payload

A **Payload** represents binary data:
- Input/output from Activities and Workflows
- Binary data + key-value metadata
- Describes data type for custom encoders/converters

## Default Data Converter

Serializes supported type values to Payloads:
- JSON serialization for plain text
- Automatic encoding

## Custom Converters

### Payload Converter
Apply different conversion steps for different types.

### Payload Codec
Additional transformations:
- **Encryption** - protect sensitive data
- **Compression** - reduce payload size

## Security Implication

> **All sensitive data exists in original format only on hosts you control.**

Temporal Service sees encoded (potentially encrypted) data only.

---

## Takeaways

1. **Data Converters handle serialization** - automatic with defaults
2. **Payload = binary data + metadata** - the unit of transfer
3. **Custom codecs for security** - encryption keeps data private from Temporal Service
4. **Decoded results stay local** - never persisted back to Service