let time = 0
let timer

function gameTimer() {
    clearInterval(timer)
    time = 0
    timer_container = document.querySelector('aside')
    timer = setInterval(() => {
        time++
        const minutes = Math.floor(time / 60)
        const seconds = time % 60
        if (minutes > 0) {
            timer_container.querySelector('span:nth-child(1)').innerText = `${minutes} M`
            timer_container.querySelector('span:nth-child(2)').innerText = `${seconds} S`
        }
        else {
            timer_container.querySelector('span:nth-child(1)').innerText = ``
            timer_container.querySelector('span:nth-child(2)').innerText = `${seconds} S`
        }
    }, 1000)
}


