document.addEventListener('DOMContentLoaded', load_correctly)

async function load_correctly(event) {
    try {
        await render()
        await getProblemFromServer(event)
        await displayProblem()
        await selectSquare()
        await selectNum()
    }
    catch(err) {
        console.log('err', err)
        // window.location.reload(true)
    }

    document.addEventListener('keydown', fill_square_keydown)

    document.querySelector('select')
    .addEventListener('change', getProblemFromServer)

    document.querySelector('#reset-puzzle')
    .addEventListener('click', resetProblem)
}
