REM TODO: Podria hacer un txt con el orden y leerlo y hacer un batch generico
REM Ojo que esta creando el lib una carpeta arriba.

type popego-context.js > ..\embedder-lib.js
type popego-utilsext.js >> ..\embedder-lib.js
type popego-widgetmanager.js >> ..\embedder-lib.js
type popego-popcardmanager.js >> ..\embedder-lib.js