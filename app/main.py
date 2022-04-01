import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="https://cpppwd.deta.dev/", reload=True)
