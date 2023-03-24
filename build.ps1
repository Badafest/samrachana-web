Clear-Host
Write-Output "building server..."
Set-Location server
npm run build
Write-Output "building frontend..."
Set-Location ../frontend
npm run build
Clear-Host
Set-Location ..
Write-Output "copying python and server/package.json..."
Copy-Item -Recurse -Force ./server/src/python ./dist/src/python
Copy-Item ./server/package.json ./dist/package.json
Write-Output "cding into dist and installing server packages..."
Set-Location ./dist
npm install --omit=dev
Write-Output "moving fonts to assets..."
Set-Location ./public
Move-Item *.ttf ./assets
Set-Location ..
Write-Output "creating python venv and installing numba..."
python3 -m venv ./.venv
py -m venv ./.venv
.venv/Scripts/activate
pip3 install -r ./src/python/requirements.txt
Clear-Host
Write-Output "now starting Samrachana..."
npm start