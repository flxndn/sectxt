#!/bin/bash

readonly PROGRAM_NAME=$(basename $0)

#-------------------------------------------------------------------------------
help() {
#-------------------------------------------------------------------------------
	cat <<HELP
* $PROGRAM_NAME
	* Usage
		$PROGRAM_NAME [ -t title ] [ -n ] file1 [file2 ...]
		$PROGRAM_NAME -h

	* Description
		Make a new sec file with the sections of the file1, file2, etc.

		Exampl:
		> * $PROGRAM_NAME
		>	* file1
		>		<contents of file1>
		>	* file2
		>		<contents of file1>
		>	...

	* Options
		* -t title
			Use title no $PROGRAM_NAME as de main title.

		* -n
			Do not use filenames as section titles.
			
			Usefull for joning sec files.

	* Author
		Félix Anadón Trigo 
HELP
}
#-------------------------------------------------------------------------------
if [ "$1" == "-h" ]; then
	help
	exit 0
fi

title=$PROGRAM_NAME 
include_file=1

while echo "$1" | grep -q '^-'; do
	if [ $1 == "-t" ]; then
		title=$2
		shift;shift;
	fi
	if [ "$1" == "-n" ]; then
		include_file=0
		shift;
	fi
done

echo "* $title"
IFS=$'\n'
for i in $*; do
	if [ "$include_file" == "1" ]; then
		echo "	* $i"
		cat $i | sed "s/^/\t\t/"
	else
		cat $i | sed "s/^/\t/"
	fi
done
