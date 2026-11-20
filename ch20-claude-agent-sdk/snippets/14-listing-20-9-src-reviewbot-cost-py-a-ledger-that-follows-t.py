@dataclass
class CostLedger:
    """Estimates only: total_cost_usd is computed client-side by the SDK."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cost_usd: float = 0.0
    runs: int = 0
    _seen: set[str] = field(default_factory=set, repr=False)

    def observe(self, message: Message) -> None:
        if isinstance(message, AssistantMessage):
            # Parallel tool calls repeat one message id: count it once.
            # Per-step output_tokens is a placeholder, so skip it here.
            mid = message.message_id
            if message.parent_tool_use_id or not mid or mid in self._seen:
                return
            self._seen.add(mid)
            self.input_tokens += (message.usage or {}).get("input_tokens", 0)
        elif isinstance(message, ResultMessage):
            usage = message.usage or {}
            self.output_tokens += usage.get("output_tokens", 0)
            self.cache_read_tokens += usage.get("cache_read_input_tokens", 0)
            self.cost_usd += message.total_cost_usd or 0.0
            self.runs += 1
