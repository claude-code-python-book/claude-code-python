"""A stand-in for the company issue tracker's REST API, with per-user access."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

TOKENS = {"trk-alice": "alice@acme.example", "trk-bob": "bob@acme.example"}
PROJECTS = {"alice@acme.example": {"PAY", "WEB"}, "bob@acme.example": {"WEB"}}
ISSUES = {
    "PAY-142": {"key": "PAY-142", "title": "Refunds over 10,000 INR fail",
                "status": "To Do", "description": "Refund API returns 500 above 10k."},
    "WEB-7": {"key": "WEB-7", "title": "Footer links 404", "status": "Done",
              "description": "Two footer links are broken."},
}
COMMENTS: list[dict[str, str]] = []


def caller(request: Request) -> str | None:
    return TOKENS.get(request.headers.get("authorization", "").removeprefix("Bearer "))


async def issue(request: Request) -> JSONResponse:
    user, key = caller(request), request.path_params["key"]
    if user is None:
        return JSONResponse({"error": "unauthorized"}, 401)
    if key.split("-")[0] not in PROJECTS[user]:
        return JSONResponse({"error": "forbidden"}, 403)
    if key not in ISSUES:
        return JSONResponse({"error": "not found"}, 404)
    if request.method == "POST":
        body = (await request.json())["body"]
        COMMENTS.append({"key": key, "author": user, "body": body})
        return JSONResponse({"key": key, "author": user, "id": len(COMMENTS)}, 201)
    return JSONResponse(ISSUES[key])


async def search(request: Request) -> JSONResponse:
    user = caller(request)
    if user is None:
        return JSONResponse({"error": "unauthorized"}, 401)
    q = request.query_params.get("q", "").lower()
    limit = int(request.query_params["limit"])
    hits = [{k: i[k] for k in ("key", "title", "status")} for i in ISSUES.values()
            if i["key"].split("-")[0] in PROJECTS[user] and q in i["title"].lower()]
    return JSONResponse(hits[:limit])


app = Starlette(routes=[
    Route("/api/issues", search),
    Route("/api/issues/{key}", issue, methods=["GET"]),
    Route("/api/issues/{key}/comments", issue, methods=["POST"]),
])
