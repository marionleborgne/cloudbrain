Build:
docker build -t publisher -f Dockerfile.publishers .

Run:

Can be run with or without parameters.
~/code/cloudbrain should be changed to match your machine.  
docker run -dt -v ~/code/cloudbrain:/cloudbrain -e PYTHONPATH=/cloudbrain publisher --mock -n muse -i baguette
