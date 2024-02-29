const fastGameWS = new WebSocket('ws://' + location.host + '/fast-game')
fastGameWS.onopen = function () {
    fastGameWS.send(JSON.stringify(
        {
            ms: 'hi'
        }
    ))
}