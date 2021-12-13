async function clientSideValidation() {
    document.querySelectorAll('.matching')
    .forEach(m => {
        m.classList.remove('matching')
    })
    document.querySelector('#auto-check').checked = true
    document.querySelector('#auto-check')
    .dispatchEvent(new Event('input'))

    if(!document.querySelector('.wrong')) {
        clearInterval(timer)
        const minutes = document.querySelector('aside span:nth-child(1)').innerText.slice(0, -1).trim()
        const seconds = document.querySelector('aside span:nth-child(2)').innerText.slice(0, -1).trim()
        document.querySelector('#difficulty-val').innerText = window.level
        document.querySelector('#time-val').innerText = `${minutes ? minutes : '0'}:${ (seconds.length < 2) ? '0'+seconds : seconds}`
        const card = document.querySelector('.win')
        card.classList.remove('win')
        card.classList.add('won')
    }
}
