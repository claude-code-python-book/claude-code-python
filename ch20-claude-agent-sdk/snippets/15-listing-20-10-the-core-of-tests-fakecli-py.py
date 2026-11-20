    async def write(self, data: str) -> None:
        msg = json.loads(data)
        self.sent.append(msg)
        if msg["type"] == "control_request":       # SDK -> CLI request
            if msg["request"]["subtype"] == "initialize":
                self.init_request = msg["request"]
            await self._out.put({"type": "control_response", "response": {
                "subtype": "success", "request_id": msg["request_id"],
                "response": {}}})
        elif msg["type"] == "control_response":    # SDK answers our request
            reply = msg["response"]
            self.answers[reply["request_id"]] = reply
            self._waiting.pop(reply["request_id"], asyncio.Event()).set()
        elif msg["type"] == "user":                # a new turn starts
            task = asyncio.create_task(self._play(self.turns.popleft()))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

    async def _play(self, frames: list[Frame]) -> None:
        for frame in frames:
            if frame["type"] == "_pause":              # test-only: stall
                await asyncio.sleep(frame["seconds"])
            elif frame["type"] == "control_request":
                done = self._waiting[frame["request_id"]] = asyncio.Event()
                await self._out.put(frame)
                await asyncio.wait_for(done.wait(), timeout=5)
            else:
                await self._out.put(frame)
        if self.exit_code and not self.turns:      # the process dies
            await self._out.put(None)
