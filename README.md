# MERN stack as microservice
## MongoDB|Express|Reactjs|Nodejs

Microservice environment to run reactjs web application in one server, nodejs express API in another server and mongodb as database supporting API. Environment also has Jenkins for continues integration and continues deployment.

### Webserver desired state
- Ubuntu
- Nginx
- Lets Encrypt SSL

### Nodejs server desired state
- Ubuntu
- Nginx as Proxy
- Nodejs
- Lets Encrypt SSL

### MongoDB server desired state
- Ubuntu
- MongoDB
- Accessible only from Nodejs server

### Jenkins server
- Ubuntu
- Jenkins
- Some test frameworks (not sure yet)
