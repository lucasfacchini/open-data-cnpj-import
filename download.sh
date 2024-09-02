FILES_URL=http://200.152.38.155/CNPJ/dados_abertos_cnpj/
LAST_MONTH=$(curl -s $FILES_URL | sed -n 's/.*href="\([^"]*\).*/\1/p' | awk 'END{print}')

DOWNLOAD_URL=$FILES_URL$LAST_MONTH
DOWNLOAD_DIR=data/download
EXTRACT_DIR=data/output-extract

if [ ! -d $DOWNLOAD_DIR ]; then
    echo "Creating dirs"
    mkdir $DOWNLOAD_DIR $EXTRACT_DIR
fi

if [ -z "$(ls -A $DOWNLOAD_DIR)" ]; then
    echo "Downloading files"
    wget --execute="robots = off" --mirror --convert-links --no-parent $DOWNLOAD_URL -A '*.zip' -P $DOWNLOAD_DIR -nd
else
    echo "Skipping download, directory is not empty \n"
fi

if [ -z "$(ls -A $EXTRACT_DIR)" ]; then
    echo "Extracting files"
    unzip $DOWNLOAD_DIR/\*.zip -d $EXTRACT_DIR
else
    echo "Skipping extraction, directory is not empty \n"
fi
