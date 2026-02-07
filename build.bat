@echo off
echo ========================================
echo  Minescript Manager - Build Script
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH!
    echo.
    echo Veuillez telecharger et installer Python depuis:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python est installe
python --version
echo.

REM Créer l'environnement virtuel
echo [ETAPE 1/4] Creation de l'environnement virtuel...
if exist venv (
    echo Environnement virtuel existant trouve, suppression...
    rmdir /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement virtuel cree
echo.

REM Activer l'environnement
echo [ETAPE 2/4] Activation de l'environnement...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement active
echo.

REM Installer PyInstaller
echo [ETAPE 3/4] Installation de PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller installe
echo.

REM Créer l'exécutable
echo [ETAPE 4/4] Creation de l'executable...
pyinstaller --onefile --windowed --name="MinescriptManager" minescript_manager_v2.py
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible de creer l'executable
    pause
    exit /b 1
)
echo.
echo ========================================
echo  BUILD TERMINE AVEC SUCCES!
echo ========================================
echo.
echo Votre executable se trouve dans:
echo %cd%\dist\MinescriptManager.exe
echo.

REM Désactiver l'environnement
deactivate

echo Appuyez sur une touche pour ouvrir le dossier dist...
pause >nul
explorer dist

exit /b 0
