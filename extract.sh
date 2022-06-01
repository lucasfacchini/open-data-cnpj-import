DOWNLOAD_URL=http://200.152.38.155/CNPJ/
DOWNLOAD_DIR=data/download
EXTRACT_DIR=data/output-extract

if [ ! -d $DOWNLOAD_DIR ]; then
    echo "Creating dirs"
    mkdir $DOWNLOAD_DIR $EXTRACT_DIR
fi


if [ -z "$(ls -A $EXTRACT_DIR)" ]; then
    echo "Extracting files"
    unzip $DOWNLOAD_DIR/\*.zip -d $EXTRACT_DIR
else
    echo "Skipping extraction, directory is not empty \n"
fi