#!/bin/bash

readonly PROGRAM_NAME=$(basename $0)

#-------------------------------------------------------------------------------
help() {
#-------------------------------------------------------------------------------
	cat <<HELP
* $PROGRAM_NAME
	* Uso
		$PROGRAM_NAME [ -t titulo ] [ -n ] fichero1 [fichero2 ...]
		$PROGRAM_NAME -h

	* Descripción
		Crea un fichero sec con los apartados fichero1 etc.

		Ejemplo:
		> * $PROGRAM_NAME
		>	* fichero1
		>		<contenido del fichero1>
		>	* fichero2
		>		<contenido del fichero1>
		>	...

	* Opciones
		* -t titulo
			Pone titulo en lugar de $PROGRAM_NAME como el título principal.

		* -n
			No pone como subtítulos los nombres de los ficheros.
			
			Sirve para cuando unimos ficheros que ya tienen el formato
			*.sec.

	* Autor
		Félix Anadón Trigo 
HELP
}
#-------------------------------------------------------------------------------
if [ "$1" == "-h" ]; then
	help
	exit 0
fi

local titulo=$PROGRAM_NAME 
local incluir_fichero=1

while echo "$1" | grep -q '^-'; do
	if [ $1 == "-t" ]; then
		titulo=$2
		shift;shift;
	fi
	if [ $1 == "-n" ]; then
		incluir_fichero=0
		shift;
	fi
done

echo "* $titulo"
for i in $*; do
	if [ "$incluir_fichero" == "1" ]; then
		echo "	* $i"
		cat $i | sed "s/^/\t\t/"
	else
		cat $i | sed "s/^/\t/"
	fi
done
