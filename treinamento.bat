@echo off
chcp 65001
title TREINAMENTO HAAR CASCADE - TUMORES PULMONARES

echo ========================================
echo    TREINAMENTO HAAR CASCADE
echo ========================================
echo.

:: Navegar para pasta do projeto
cd /d "C:\Users\Guilherme\Desktop\Computer_Vision_For_Health\Computer-vision-for-health"

echo 📁 Pasta atual: %cd%
echo.

:: Verificar e criar pasta classifier
if not exist "classifier" (
    mkdir classifier
    echo ✅ Pasta classifier criada
)

:: 1. Criar arquivo .vec
echo [1/3] Criando arquivo positives.vec...
"C:\opencv\build\x64\vc15\bin\opencv_createsamples.exe" -info info.dat -num 50 -w 24 -h 24 -vec positives.vec

if not exist "positives.vec" (
    echo ❌ Erro: positives.vec não foi criado
    pause
    exit /b 1
)

echo ✅ positives.vec criado com sucesso!
echo.

:: 2. Treinar classificador (COM PERMISSÕES)
echo [2/3] Iniciando treinamento...
echo ⏳ Este processo pode demorar...
echo.
echo 🔧 Executando como administrador...
runas /user:Administrator "C:\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data classifier -vec positives.vec -bg bg.txt -numPos 50 -numNeg 200 -numStages 3 -w 24 -h 24 -featureType HAAR"

:: Esperar e verificar resultado
timeout /t 10 /nobreak >nul

:: 3. Verificar resultado
if exist "classifier\cascade.xml" (
    echo.
    echo 🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!
    echo 📁 Classificador salvo em: classifier\cascade.xml
) else (
    echo.
    echo ❌ Treinamento falhou - tentando método alternativo...
    call :metodo_alternativo
)

pause
exit /b 0

:metodo_alternativo
echo.
echo 🔄 Tentando método alternativo...
:: Usar pasta temporária com mais permissões
mkdir C:\temp_classifier 2>nul
"C:\opencv\build\x64\vc15\bin\opencv_traincascade.exe" -data C:\temp_classifier -vec positives.vec -bg bg.txt -numPos 50 -numNeg 200 -numStages 3 -w 24 -h 24

if exist "C:\temp_classifier\cascade.xml" (
    copy "C:\temp_classifier\cascade.xml" "classifier\cascade.xml" >nul
    echo ✅ Classificador copiado para classifier\cascade.xml
    rmdir /s /q C:\temp_classifier
)
exit /b 0