#!/bin/bash

# Here is a helper script for running Airflow locally

set -e

# Fonts utils
RED_COLOR="\033[0;31m"
GREEN_COLOR="\033[0;32m"
YELLOW_COLOR="\033[0;33m"
BOLD=$(tput bold)
NC=$(tput sgr0)

start_airflow() {
    mkdir -p ./config
    mkdir -p ./logs
    mkdir -p ./plugins
    docker-compose up -d

    echo -e "${GREEN_COLOR}${BOLD}Airflow is running on http://localhost:8080/${NC}\n"
}

restart_airflow() {
    docker-compose down
    docker-compose up -d

    echo -e "${GREEN_COLOR}${BOLD}Restart Done!, Airflow is running on http://localhost:8080/${NC}\n"
}

delete_airflow() {
    docker-compose down --volumes --rmi local
    rm -rf ./config
    rm -rf ./logs
    rm -rf ./plugins

    echo -e "${YELLOW_COLOR}${BOLD}Your workspace is clean 🙀${NC}\n"
}

main() {
    echo -e "${GREEN_COLOR}"
    echo -e "################################ Local Aiflow #################################"
    echo -e "############# Here is a helper script for running Airflow locally #############"
    echo -e "${NC}"
    echo -e "${GREEN_COLOR} 1. Start Airflow"
    echo -e "${YELLOW_COLOR} 2. Restart Airflow"
    echo -e "${RED_COLOR} 3. Delete Airflow${NC}\n"
    read -p "Enter your option: " option
    if [ $option = "1" ]; then
        start_airflow
    elif [ $option = "2" ]; then
        restart_airflow
    elif [ $option = "3" ]; then
        delete_airflow
    else
        echo -e "${RED_COLOR}Invalid option. Exiting...${NC}"
        exit 1
    fi
}

main
