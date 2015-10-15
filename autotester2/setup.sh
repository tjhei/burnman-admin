rm -rf burnman
git clone https://github.com/geodynamics/burnman.git
docker build -t tjhei/burnman docker-burnman/
