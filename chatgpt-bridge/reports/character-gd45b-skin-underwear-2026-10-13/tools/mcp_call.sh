#!/bin/bash
# mcp_call.sh <json-rpc body> : POST to the editor's MCP server with the stored session id; prints the response body
N="Saved/Codex/GD45_Promote_20261013"; SID=$(cat "$N/data/mcp_sid.txt"); curl -s -m 120 -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: $SID" -X POST http://127.0.0.1:8000/mcp -d "$1"
