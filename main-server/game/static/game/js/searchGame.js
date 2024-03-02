const fastGameWS = new WebSocket('ws://' + location.host + '/fast-game')
fastGameWS.onopen = function () {
    fastGameWS.send(JSON.stringify(
        {
            ms: 'hi'
        }
    ))
}
fastGameWS.onmessage = function (event){
    const data = JSON.parse(event.data)
    console.log(data)
}