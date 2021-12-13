document.querySelector('#new')
.addEventListener('click', newGame)

async function newGame(event) {
    const msg = document.querySelector('.won')
    msg.classList.add('win')
    msg.classList.remove('won')
    await getProblemFromServer(event)
}
