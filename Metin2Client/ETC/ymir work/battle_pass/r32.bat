:main
@echo OFF
@echo ¯ Bun Venit in R32,By Nytro;
@echo   Esclusiv pentru www.4Metin.ro.
@echo ---


:rename
set OLD=
set /P OLD=Alege vechia extensie a clientului : %=%
if "%OLD%" == "" GOTO error
set NEW=
set /P NEW=Alege noua extensie pentru client   : %=%
if "%NEW%" == "" GOTO error
@ren *.%OLD% *.%NEW%
@echo Fisierele .%OLD% au fost redenumite in .%NEW%
@echo ---
GOTO fine
:errore
@echo Error!
@echo Esti rugat sa alegi o extensie valida!
@echo Reporneste programul,si incearca din nou.
@echo ---
GOTO Iesire
:fine
@echo La cum arata totul,se pare ca ai reusit...
:Iesire
@pause