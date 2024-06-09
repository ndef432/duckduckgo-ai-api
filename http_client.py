import dataclasses

import aiohttp


@dataclasses.dataclass(kw_only=True)
class HTTPClient:
    base_url: str
    headers: dict[str, str]
    proxy: str | None = None
    session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url,
                                             headers=self.headers)
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(exc_type, exc_val, exc_tb)
        self.session = None

    def _request(self, method, path, kwargs):
        return self.session.request(method, path, proxy=self.proxy, **kwargs)

    def get(self, path, **kwargs):
        return self._request(aiohttp.hdrs.METH_GET, path, kwargs)

    def post(self, path, **kwargs):
        return self._request(aiohttp.hdrs.METH_POST, path, kwargs)
