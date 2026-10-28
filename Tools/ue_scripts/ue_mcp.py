import socket
import json
import time

class UnrealMCPClient:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.session_id = None
        self._init_session()

    def _init_session(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        init_body = json.dumps({
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "python-ue-mcp", "version": "1.0"}
            },
            "id": 1
        })
        req = f"POST /mcp HTTP/1.1\r\nHost: {self.host}:{self.port}\r\nContent-Type: application/json\r\nContent-Length: {len(init_body)}\r\n\r\n{init_body}"
        s.sendall(req.encode("utf-8"))

        data = b""
        while b"\r\n\r\n" not in data:
            data += s.recv(1024)
        header_part, rest = data.split(b"\r\n\r\n", 1)
        for line in header_part.decode("utf-8").split("\r\n"):
            if line.lower().startswith("mcp-session-id:"):
                self.session_id = line.split(":", 1)[1].strip()
        s.close()
        # print(f"[MCP] Initialized session: {self.session_id}")

    def call_raw(self, method, params=None, req_id=2, timeout=30.0):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((self.host, self.port))
        body = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": req_id
        })
        req = (
            f"POST /mcp HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            f"Content-Type: application/json\r\n"
            f"Mcp-Session-Id: {self.session_id}\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
            f"{body}"
        )
        s.sendall(req.encode("utf-8"))

        # Read response
        buf = b""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                buf += chunk

                # Check for standard HTTP Content-Length response
                if b"\r\n\r\n" in buf:
                    header_part, body_part = buf.split(b"\r\n\r\n", 1)
                    content_length = None
                    for line in header_part.decode("utf-8", errors="ignore").split("\r\n"):
                        if line.lower().startswith("content-length:"):
                            try:
                                content_length = int(line.split(":", 1)[1].strip())
                            except ValueError:
                                pass
                    if content_length is not None and len(body_part) >= content_length:
                        try:
                            parsed = json.loads(body_part[:content_length].decode("utf-8"))
                            s.close()
                            return parsed
                        except json.JSONDecodeError:
                            pass

                # Check for SSE data line
                if b"\ndata: " in buf or b"\r\ndata: " in buf:
                    text = buf.decode("utf-8", errors="ignore")
                    for line in text.split("\n"):
                        line = line.strip()
                        if line.startswith("data: "):
                            raw_json = line[6:].strip()
                            try:
                                parsed = json.loads(raw_json)
                                s.close()
                                return parsed
                            except json.JSONDecodeError:
                                pass
            except socket.timeout:
                break
        s.close()
        raise TimeoutError(f"Timed out waiting for response to {method}. Received buffer: {buf[:500]}")

    def call_tool(self, tool_name, arguments=None):
        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        res = self.call_raw("tools/call", params)
        if "error" in res:
            raise RuntimeError(f"Tool error: {res['error']}")
        return res.get("result", {})

    def describe_toolset(self, toolset_name):
        return self.call_tool("describe_toolset", {"toolset_name": toolset_name})

    def run_tool(self, toolset_name, tool_name, arguments=None):
        return self.call_tool("call_tool", {
            "toolset_name": toolset_name,
            "tool_name": tool_name,
            "arguments": arguments or {}
        })

if __name__ == "__main__":
    client = UnrealMCPClient()
    print("Testing describe_toolset...")
    res = client.describe_toolset("animation_toolset.toolsets.controlrig.ControlRigTools")
    print("Result:", json.dumps(res, indent=2))
