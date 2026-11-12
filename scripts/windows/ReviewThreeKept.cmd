@echo off
setlocal
set "page=%~dp0..\..\data\local\campaign-v4-three-kept-2026-11-12-r02\reports\review.html"
if not exist "%page%" (
  echo Chua co trang review cua ban r02. Xem docs/THREE_KEPT_CAMPAIGN.md.
  pause
  exit /b 1
)
start "" "%page%"
