"""A tiny Redis client for the tests, speaking the RESP protocol directly.

It implements only the commands notify.delivery uses, with the same return
types as redis-py, so the tests exercise a real Redis server.
"""

import socket


class MiniRedis:
    """Enough of redis.Redis for SET, GET, DEL, LPUSH, LRANGE and TTL."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 15) -> None:
        self._sock = socket.create_connection((host, port), timeout=5)
        self._file = self._sock.makefile("rb")
        self._call("SELECT", str(db))

    def _call(self, *args: str) -> object:
        parts = [f"*{len(args)}\r\n".encode()]
        for arg in args:
            data = arg.encode()
            parts.append(b"$%d\r\n%s\r\n" % (len(data), data))
        self._sock.sendall(b"".join(parts))
        return self._read()

    def _read(self) -> object:
        line = self._file.readline().rstrip(b"\r\n")
        kind, rest = line[:1], line[1:]
        if kind == b"+":
            return rest.decode()
        if kind == b"-":
            raise RuntimeError(rest.decode())
        if kind == b":":
            return int(rest)
        if kind == b"$":
            if rest == b"-1":
                return None
            data = self._file.read(int(rest) + 2)
            return data[:-2]
        if kind == b"*":
            return [self._read() for _ in range(int(rest))]
        raise RuntimeError(f"unexpected reply {line!r}")

    def set(
        self, name: str, value: str, ex: int | None = None, nx: bool = False
    ) -> bool | None:
        args = ["SET", name, value]
        if ex is not None:
            args += ["EX", str(ex)]
        if nx:
            args.append("NX")
        return True if self._call(*args) == "OK" else None

    def get(self, name: str) -> bytes | None:
        reply = self._call("GET", name)
        assert reply is None or isinstance(reply, bytes)
        return reply

    def delete(self, *names: str) -> int:
        reply = self._call("DEL", *names)
        assert isinstance(reply, int)
        return reply

    def lpush(self, name: str, *values: str) -> int:
        reply = self._call("LPUSH", name, *values)
        assert isinstance(reply, int)
        return reply

    def lrange(self, name: str, start: int, end: int) -> list[bytes]:
        reply = self._call("LRANGE", name, str(start), str(end))
        assert isinstance(reply, list)
        return reply

    def ttl(self, name: str) -> int:
        reply = self._call("TTL", name)
        assert isinstance(reply, int)
        return reply

    def flushdb(self) -> None:
        self._call("FLUSHDB")

    def close(self) -> None:
        self._file.close()
        self._sock.close()
