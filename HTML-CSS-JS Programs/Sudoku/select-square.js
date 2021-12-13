window.square = undefined

async function selectSquare() {
    document.querySelectorAll('game-square')
    .forEach(gs => {
        gs.addEventListener('click', event => {
            try {
                document.querySelectorAll('game-square')
                .forEach(e => {
                    e.classList.remove('highlight')
                    e.classList.remove('active')
                    e.classList.add('normal')
                })
                document.querySelectorAll('circle.matching, circle.focus')
                .forEach(c => {
                    c.classList.remove('matching')
                    c.classList.remove('focus')
                })
                gs.parentNode.querySelectorAll('game-square')
                .forEach(related => {
                    related.classList.remove('normal')
                    related.classList.add('highlight')
                })
                document.querySelectorAll(`game-square[data-col="${gs.dataset.col}"], game-square[data-row="${gs.dataset.row}"]`)
                .forEach(related => {
                    related.classList.remove('normal')
                    related.classList.add('highlight')
                })
                gs.classList.remove('normal')
                gs.classList.remove('highlight')
                gs.classList.add('active')
                window.square = gs
            }
            catch(err) {
                console.log(err)
            }
        })
    })
}
