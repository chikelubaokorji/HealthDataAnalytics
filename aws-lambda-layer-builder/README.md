# AWS Lambda Layer Builder
1. Checker all files have your lambda function python version
2. Change the requirements to the python package you want to create lambda layer dependency
3. Start up docker on your machine
4. Give runner.sh full permission and run
```bash
chmod 744 runner.sh
./runner.sh
```