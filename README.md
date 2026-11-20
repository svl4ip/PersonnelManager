# Personnel Manager — Windows 10/11 x64

## Included
- Arabic / English interface toggle
- Local SQLite database (offline)
- Personnel, attendance, leave, penalties, commendations, promotions
- Add / edit / delete / search
- CSV export
- Database backup and restore
- Developer credit: Hussein Rahim

## Run from source
1. Install Python 3.10 or newer for Windows (64-bit).
2. Extract this folder.
3. Double-click `run_windows.bat` or run `py app.py`.

## Build the EXE
1. Install Python 3.10+ (64-bit) on Windows.
2. Double-click `build_windows.bat`.
3. The executable will be created at `dist\PersonnelManager.exe`.
4. Copy the EXE to a folder where you want to keep the local database. The database `personnel.db` is created beside the EXE.

## Important security notice
This is a functional starter version, not a Ministry of Defence approved or security-certified system.
It has no user authentication, encryption-at-rest, audit log, role-based access, or secure multi-user synchronization.
Do not store classified, operational, or real sensitive personnel information in this version.
Promotion eligibility dates are entered manually; the program does not calculate legal eligibility rules.
