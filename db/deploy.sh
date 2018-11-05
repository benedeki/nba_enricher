#!/bin/bash

for i in "$@"; do
	case "$i" in
		-f)
			#skip over this param
			shift
			shift
			;;
		--file=*)
			#skip over this param
			shift
			;;
		--password=*)
			PWD="${i#*=}"
			shift
			;;
		--help)
			echo "**************************************************************************************************************************"
			echo "Deploys all sql scripts (*.sql files) in the directory and subdirectories."
			echo "Fist the __struct.sql files are executed, then all the others in alphabetical order."
			echo "The very same switches and options are accepted as psql accepts, only the -f/--file one is ignored and not passed to psql."
			echo "This script accepts additional --password parameter"
			echo "**************************************************************************************************************************"
			psql --help
			exit 0
			;;
		*)    # unknown option
			POSITIONAL+=("$i") # save it in an array for later
			shift # past argument
			;;
	esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ "${PWD}" ]]; then
	export PGPASSWORD="${PWD}"
fi

CMD="psql"
find . -name "__schema.sql" -print0 | xargs -0 -I {} $CMD --file={} "$@"
find . -type f \( -iname "*.sql" ! -iname "__schema.sql" \) -print0 |  xargs -0 -I {} $CMD --file={} "$@"
