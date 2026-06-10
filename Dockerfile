# bima-mcp — Dockerfile for Glama sandbox build and evaluation
# Glama uses this to run security checks and assign quality/security scores.
#
# Local usage:
#   docker build -t bima-mcp .
#   docker run bima-mcp

FROM python:3.11-slim

LABEL org.opencontainers.image.title="bima-mcp"
LABEL org.opencontainers.image.description="MCP server for Kenya insurance intelligence — NHIF, parametric crop risk, microinsurance"
LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/bima-mcp"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Gabriel Mahia <contact@aikungfu.dev>"

# Non-root for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir bima-mcp

USER mcpuser

# MCP servers use stdio transport
ENTRYPOINT ["bima-mcp"]
