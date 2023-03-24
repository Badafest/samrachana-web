clear
echo "building server..."
cd server
npm run build
echo "building frontend..."
cd ../frontend
npm run build
clear
cd ..
echo "copying python and server/package.json..."
cp -rf ./server/src/python ./dist/src/python
cp ./server/package.json ./dist/package.json
echo "cding into dist and installing server packages..."
cd ./dist
npm install --omit=dev
echo "moving fonts to assets..."
cd ./public
mv *.ttf ./assets
cd ..
echo "creating python venv and installing numba..."
python3 -m venv ./.venv
py -m venv ./.venv
.venv/Scripts/activate
pip3 install -r ./src/python/requirements.txt
clear
echo "now starting Samrachana..."
npm start