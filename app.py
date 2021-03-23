from bocadillo import App

app = App()

@app.websocket_route("/conversation")
async def converse(ws):
    async for message in ws:
        await ws.send(message)

if __name__ == "__main__":
    app.run()
