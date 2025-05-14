@echo off
echo === REINICIANDO GIT DO PROJETO ===

REM Apaga o histórico Git antigo
rmdir /s /q .git

REM Inicia novo repositório Git
git init

REM Cria arquivo .gitignore padrão
echo node_modules/ > .gitignore
echo dist/ >> .gitignore
echo .DS_Store >> .gitignore

REM Adiciona todos os arquivos (exceto os ignorados)
git add .

REM Faz o commit
git commit -m "Reiniciado projeto sem node_modules e arquivos grandes"

REM Define a branch principal como main
git branch -M main

REM Conecta ao repositório remoto
git remote add origin https://github.com/iart2025/mozart.git

REM Envia o código para o GitHub com força
git push -u --force origin main

echo === FINALIZADO COM SUCESSO ===
pause
