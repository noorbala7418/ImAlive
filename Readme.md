# Im Alive!
Im Alive is a simple tool for communicate with server that you are not access to SSH.

## API URL:
| Endpoint | Method | Details |
|--|--|--|
| /alive |GET  | Return an string + uptime of server |
| /service/state/<service_name> | GET | Returns status of desired service (Note: This EP need to login with basic login) |
| /run | POST | Executes some simple system commands (need to login)  |
|  |  |  |

### Note:
Please copy and rename `.env.example` to `.env` and change default username & password.