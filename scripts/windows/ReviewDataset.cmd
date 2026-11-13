@echo off
setlocal
set "REVIEW_PAGE=%~dp0..\..\data\local\campaign-v2\review-assistant-v3\review.html"
if not exist "%REVIEW_PAGE%" set "REVIEW_PAGE=%~dp0..\..\data\local\campaign-v2\review-assistant-v2\review.html"
if not exist "%REVIEW_PAGE%" set "REVIEW_PAGE=%~dp0..\..\data\local\campaign-v2\review-assistant-v1\review.html"
if not exist "%REVIEW_PAGE%" set "REVIEW_PAGE=%~dp0..\..\data\local\campaign-v2\review-start\review.html"
if not exist "%REVIEW_PAGE%" (
  echo Chua co trang ra dataset tren may nay. Xem docs/LABEL_REVISIONS.md.
  pause
  exit /b 1
)
start "" "%REVIEW_PAGE%"
