function fill_square_keydown(event) {
    if (!window.square) {
        return false
    }
    const number = event.key
    if (parseInt(number) != number) {
        return false
    }
    document.querySelector(`game-numbers div:nth-child(${number})`)
    .dispatchEvent(new Event('click'))
}

async function fill_square_click(event) {
    event.stopPropagation()
    document.querySelectorAll('game-square circle')
    .forEach(e => {
        e.classList.remove('matching')
    })
    if (window.current.positions_available.includes(window.square.id)) {
        const text = window.square.querySelector('text')
        text.textContent = this.querySelector('text').textContent
        const sq = window.square.querySelector('circle')
        sq.classList.remove('empty')
        sq.classList.add('filled')
        const row = parseInt(window.square.id.slice(0,-1)) - 1
        const col = parseInt(window.square.id.slice(-1)) - 1
        if (window.autocheck) {
            if ((text.textContent.trim() == window.current.solution[row][col])) {
                sq.classList.remove('wrong')
                sq.classList.add('focus')
            }
            else {
                sq.classList.remove('focus')
                sq.classList.add('wrong')
            }
        }
        else {
            sq.classList.add('focus')
        }
        document.querySelectorAll('circle.filled:not(.focus):not(.wrong)')
        .forEach(c => {
            if(c.nextElementSibling.textContent.trim() === text.textContent.trim()) {
                c.classList.add('matching')
            }
        })
        if (document.querySelector('.empty') === null) {
            await clientSideValidation()
        }
    }
    else {
        return false
    }
}

async function selectNum() {
    document.querySelectorAll('game-numbers div')
    .forEach(num => {
        num.addEventListener('click', fill_square_click)
    })
    document.querySelector('#auto-check')
    .addEventListener('input', event => {
        window.autocheck = event.target.checked
        localStorage.setItem('autocheck', window.autocheck)
        if (!window.autocheck) {
            document.querySelectorAll('circle.filled.wrong')
            .forEach(w => {
                w.classList.remove('wrong')
            })
        }
        else {
            document.querySelectorAll('circle.filled')
            .forEach(w => {
                const text = w.nextElementSibling.textContent.trim()
                if (text !== '') {
                    const row = parseInt(w.parentNode.parentNode.id.slice(0, 1)) - 1
                    const col = parseInt(w.parentNode.parentNode.id.slice(-1)) - 1
                    if (text != window.current.solution[row][col]) {
                        w.classList.remove('focus')
                        w.classList.remove('matching')
                        w.classList.add('wrong')
                    }
                }
            })
        }
    })
    window.autocheck = localStorage.getItem('autocheck')
    document.querySelector('#auto-check').checked = window.autocheck
}
