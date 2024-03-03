const fastGameWS = new WebSocket('ws://' + location.host + '/fast-game')
fastGameWS.onopen = function () {
    fastGameWS.send(JSON.stringify(
        {
            ms: 'hi'
        }
    ))
}
fastGameWS.onmessage = function (event) {
    const data = JSON.parse(event.data)
    console.log(data)
    switch (data.type) {
        case 'search.redirect':
            const url =window.location.protocol + "//" + window.location.host + data.relative_url;
            console.log(url)
            window.location.href = url
    }
}