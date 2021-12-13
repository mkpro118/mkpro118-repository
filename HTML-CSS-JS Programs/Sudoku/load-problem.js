window.current = {
    problem: undefined,
    solution: undefined,
    positions_available: [],
}

async function getProblemFromServer(event) {
    level = localStorage.getItem('level')
    if (level && event.type === 'DOMContentLoaded') {
        window.level = level
        try {
            document.querySelector('select').value = window.level

        }
        catch(err) {
            console.log(err)
            alert('There was an error loading the page.\nPlease reload the page')
        }
    }
    else {
        window.level = document.querySelectorAll('option:checked')[0].value
        localStorage.setItem('level', window.level)
    }
    const response = await fetch('./test-sudoku.json')
    const res_text = await response.text()
    const data = JSON.parse(res_text)
    window.current.problem = data[window.level].problem
    window.current.solution = data[window.level].solution
    await displayProblem()
    gameTimer()
}

async function displayProblem() {
    window.current.positions_available = []
    for (let row = 1; row < 10; row++) {
        for (let col = 1; col < 10; col++) {
            const cur = window.current.problem[row-1][col-1]
            const content =  cur == 0 ? ' ' : cur
            const num_container = document.querySelector(`game-square[id="${row}${col}"]`)
            const circle = num_container.querySelector('circle')
            if (content !== ' ') {
                circle.classList.remove('empty')
                circle.classList.add('filled')
            }
            else {
                circle.classList.remove('filled')
                circle.classList.add('empty')
                window.current.positions_available.push(num_container.id)
            }
            circle.classList.remove('matching')
            circle.classList.remove('wrong')
            num_container.querySelector('text').textContent = `${content}`
        }
    }
}

async function resetProblem() {
    document.querySelectorAll('game-square')
    .forEach(gs => {
        gs.querySelector('text').textContent = ''
    })
    await displayProblem()
    gameTimer()
}
