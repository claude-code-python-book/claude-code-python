from fastapi import FastAPI, HTTPException

from .schemas import ReviewRequest, ReviewResponse
from .service import BudgetExhaustedError, ReviewService, UnknownRepoError

app = FastAPI(title="reviewbot")
service = ReviewService.from_env()


@app.post("/reviews")
async def create_review(request: ReviewRequest) -> ReviewResponse:
    try:
        report = await service.review(request.repo, request.base)
    except UnknownRepoError:
        raise HTTPException(status_code=404, detail="unknown repository") from None
    except BudgetExhaustedError:
        raise HTTPException(status_code=429, detail="review budget used up") from None
    except TimeoutError:
        raise HTTPException(status_code=504, detail="review timed out") from None
    return ReviewResponse.from_report(report)
