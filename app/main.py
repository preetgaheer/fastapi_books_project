import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="cpppwd.deta.dev", port=8000, reload=True)
