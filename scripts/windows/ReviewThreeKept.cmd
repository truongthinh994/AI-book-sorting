@echo off
setlocal
set "page=%~dp0..\..\data\local\campaign-v4-three-kept-2026-11-12-r07\proposed-02\index.html"
if not exist "%page%" (
  echo Chua co trang review cua ban r07. Xem docs/DATASET_KEPT_SPLIT_R07.md.
  pause
  exit /b 1
)
start "" "%page%"
