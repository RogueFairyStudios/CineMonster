#!/usr/bin/env bash
# Script for Generate Translation files
# @author: Edward "Toy" Facundo
# requires: pybabel

TRANSLATION_DIR=./
LANGS=("pt_BR" "en") # todo: smarter detection
GENERATED_DIR=./generated
options=("create" "update" "compile" "clean" "quit")
select opt in "${options[@]}"
do
    case $opt in
        "create")
            echo "Creating files"
            pybabel extract -F babel.cfg -o cinemonster.pot ../
            for lang in ${LANGS[@]}; do
                pybabel init -i cinemonster.pot -d "${GENERATED_DIR}" -l ${lang};
            done
            ;;
        "update")
            echo "updating files"
            pybabel update -i cinemonster.pot --previous -d "${GENERATED_DIR}"
            ;;
        "compile")
            echo "compiling files"
            pybabel compile -d "${GENERATED_DIR}"
            ;;
        "clean")
            echo "cleaning files"
            rm -rf "${GENERATED_DIR}"
            rm cinemonster.pot
            ;;
        "quit")
            break
            ;;
        *) echo invalid option;;
    esac
done
